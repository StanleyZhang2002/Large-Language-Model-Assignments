% Student name: Shilin Zhang
% Student number: 1007065532
% UTORid: zhan9834

% This code is provided solely for the personal and private use of students
% taking the CSC485H/2501H course at the University of Toronto. Copying for
% purposes other than this use is expressly prohibited. All forms of
% distribution of this code, including but not limited to public repositories on
% GitHub, GitLab, Bitbucket, or any other online platform, whether as given or
% with any changes, are expressly prohibited.

% Authors: Ken Shi, Jingcheng Niu and Gerald Penn

% All of the files in this directory and all subdirectories are:
% Copyright (c) 2024 University of Toronto

:- ensure_loaded(csc485).
:- ale_flag(pscompiling, _, parse_and_gen).
lan(en).
question(q2).

% Type Feature Structure

% Do not modify.
bot sub [cat, sem, list, logic, func, qs, gap_struct].
    cat sub [q, det, gappable, has_sem] intro [logic:logic, qstore:list].
        has_sem sub [n, gappable] intro [sem:sem].
            gappable sub [np, verbal] intro [gap:gap_struct].
                verbal sub [v, vp, s] intro [subcat:list].

    gap_struct sub [none, np].

    sem sub [student, course, take].

    list sub [e_list, ne_list].
        ne_list intro [hd:bot, tl:list].

    logic sub [free, scopal].
        scopal sub [lambda, quant] intro [bind:logic, body:logic].
            quant sub [exists, forall] intro [bind:qvar].
        free sub [op, app, qvar].
            op sub [and, imply] intro [lhs:logic, rhs:logic].
            app intro [f:func, args:list].
    func sub [lambda, sem].

    qs intro [l:logic, x:logic].


% Recommended implementation strategy:
% 
% 1. Implement the grammar rules for parsing.
%    At this stage, you don't need to specify the logic feature.  Make sure that
%    subcategorization and gap are properly implemented.  All the grammatical
%    sentences should get a correct parse, and all the ungrammatical ones should
%    be rejected.
% 
% 2. Implement the surface quantifier scope reading.
%    When you are confident that your syntactic rules are correct.  You can move
%    on to quantifier scope.  Specify the logic form of each lexical entry with
%    the macros provided.  Then, for the rules, implement the beta reduction rules
%    to get the surface reading.  You won't need the quantifier actions 
%    (`store`, `retrieve`, `qaction`) yet.
% 
% 3. Implement quantifier storage.
%    When you can get the correct surface readings, you can implement the
%    quantifier storage to model the ambiguity.  You will need to augment the
%    grammar rules with the quantifier actions.  Make sure that quantifier storage
%    does not break your previous progress.
% 
% 4. Evaluate with translation.
%    Translation should be the final step.  If all your previous steps are
%    correct, you should get a smooth translation.

% Lexicon

every ---> (q, 
    % === Your Code ===
    logic:
        @lambda(F, 
                @lambda(P, 
                    @forall(Y, 
                        @apply(F, [Y]),
                        @apply(P, [Y])))),
    % === ========= ===
    qstore:[]).

a ---> (q,
    % === Your Code ===
    logic:
        @lambda(F, 
                @lambda(P,
                    @exists(Y, 
                        @apply(F, [Y]),
                        @apply(P, [Y])))),
    % === ========= ===
    qstore:[]).

course ---> (n,
    sem:(course, Course),
    % === Your Code ===
    logic: @lambda(X, @apply(course, [X])),
    % === ========= ===
    qstore:[]).

student ---> (n,
    sem:(student, Student),
    % === Your Code ===
    logic: @lambda(X, @apply(student, [X])),
    % === ========= ===
    qstore:[]).

takes ---> (v,
    sem:(take, Take),
    % === Your Code ===
    logic:
        @lambda(Q, 
                @lambda(Z, 
                    @apply(Q, [
                        @lambda(X, 
                            @apply(take, [Z, X]))
                    ]))),
    subcat:[
        (Obj, sem:course),
        (Subj, sem:student)
    ],
    % === ========= ===
    qstore:[]).


% Rules

np rule
    % (np, ...) ===>
    % cat> (q, ...),
    % sem_head> (n, ...),
    % goal> ... Hint: How many goals should we have?
    % === Your Code ===
    (np, sem:Sem, logic:NPLogic, qstore:NPQStore, gap:none) ===>
    cat> (q, logic:QLogic, qstore:QQstore),
    sem_head> (n, sem:Sem, logic:NLogic, qstore:NQstore),
    goal> (beta_normalize(@apply(QLogic, [NLogic]), NewLogic)),
    goal> (qaction(NewLogic, NQstore, NPLogic, NPQStore)).
    % === ========= ===

vp rule
    % (vp, ...) ===>
    % sem_head> (v, ...),
    % cat> (np, ...),
    % goal> ...
    % === Your Code ===
    (vp, sem:VSem, subcat:Rest, logic:NewLogic, qstore:NPQStore, gap:Gap) ===>
    sem_head> (v, sem:VSem, subcat:[Obj|Rest], logic:VLogic),
    cat> (np, Obj, logic:NPLogic, qstore:NPQStore, gap:Gap),
    goal> (beta_normalize(@apply(VLogic, [NPLogic]), NewLogic)).
    % === ========= ===

s rule
    % (s, ...) ===>
    % cat> (np, ...),
    % sem_head> (vp, ...),
    % goal> ...
    % === Your Code ===
    (s, sem:VPSem, logic:SLogic, qstore:SQstore, subcat:(Rest, []), gap:(Gap, none)) ===>
    cat> (np, Subj, logic:NPLogic, qstore:(NPQstore, [])),
    sem_head> (vp, sem:VPSem, gap:Gap, subcat:[Subj|Rest], logic:VPLogic, qstore:VPQStore),
    goal> (beta_normalize(@apply(NPLogic, [VPLogic]), NewLogic)),
    goal> (retrieve(VPQStore, NewLogic, SQstore, SLogic)).
    % === ========= ===

s_gap rule
    % (s, ...) ===>
    % cat> (Gap),
    % cat> (np, ...),
    % sem_head> (vp, ...),
    % goal> ...
    % === Your Code ===
    (s, sem:VPSem, gap:none, subcat:(Rest, []), logic:SLogic, qstore:SQstore) ===>
    cat> (Gap),
    cat> (np, Subj, logic:NPLogic, qstore:(NPQStore, [])),
    sem_head> (vp, sem:VPSem, logic:VPLogic, qstore:VPQstore, subcat:[Subj|Rest], gap:Gap),
    goal> (beta_normalize(@apply(NPLogic, [VPLogic]), NewLogic)),
    goal> (retrieve(VPQstore, NewLogic, SQstore, SLogic)).
    % === ========= ===

% The empty category:
empty (np, sem:Sem, logic:Logic, qstore:QStore,
    gap:(sem:Sem, logic:Logic, qstore:QStore, gap:none)).

% Macros
lambda(X, Body) macro (lambda, bind:X, body:Body).
forall(X, Restr, Body) macro (forall, bind:X, body:(imply, lhs:Restr, rhs:Body)).
exists(X, Restr, Body) macro (exists, bind:X, body:(and, lhs:Restr, rhs:Body)).
apply(F, Args) macro (app, f:F, args:Args).

% Helper goals
append([],Xs,Xs) if true.
append([H|T1],L2,[H|T2]) if append(T1,L2,T2).
is_empty([]) if true.

% Beta normalization goals
beta_normalize((lambda,Lambda),Lambda) if !,true.
beta_normalize((Input,bind:Bind,body:Body),(Output,bind:Bind,body:BetaBody)) if
    bn_quant(Input,Output),
    beta_normalize(Body,BetaBody).
beta_normalize((Input,lhs:LHS,rhs:RHS),(Output,lhs:BetaLHS,rhs:BetaRHS)) if
    bn_op(Input,Output),
    beta_normalize(LHS,BetaLHS),
    beta_normalize(RHS,BetaRHS).
beta_normalize(@apply(@lambda(X,Body),[X]),Beta) if 
    !,beta_normalize(Body,Beta).
beta_normalize((app,Apply),Apply) if true.

bn_quant(exists,exists) if true.
bn_quant(forall,forall) if true.
bn_op(and,and) if true.
bn_op(imply,imply) if true.

% Quantifier actions
store(Logic, QStore, @lambda(F, @apply(F,[X])), 
                     [(l:Logic, x:X)|QStore]) if true.

qaction(Logic, QStore, Logic, QStore) if true.
qaction(Logic, QStore, NewLogic, NewQStore) if
    store(Logic, QStore, NewLogic, NewQStore).

retrieve((Empty, []), Logic, Empty, Logic) if true.
retrieve([(l:QLogic, x:X)|T], Logic, T, NewLogic) if 
    beta_normalize(@apply(QLogic, [@lambda(X, Logic)]), NewLogic).

% Specifying the semantics for generation.
semantics sem1.
sem1(logic:S, S) if true.
sem1(sem:S, S) if true.

% Some example shortcut helper functions
rec_test :- rec[a,student,takes,every,course].
prect_test :- prec([a,student,takes,every,course]).
translate_test :- translate([a,student,takes,every,course]).
translate_test2 :- translate([every,student,takes,a,course]).
q :- halt.
r :- compile_gram(q2_en).
