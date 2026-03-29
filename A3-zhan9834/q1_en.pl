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

:- ale_flag(pscompiling, _, parse_and_gen).
:- ensure_loaded(csc485).
lan(en).
question(q1).

% Type Feature Structure

% Do not modify lines 25-37.
bot sub [cat, sem, agr, list].
    sem sub [n_sem, v_sem].
        n_sem sub [student, wolf, sheep] intro [quantity:quantity].
        v_sem sub [chase, see] intro [subj:sem, obj:sem].

    cat sub [nominal, verbal] intro [agr:agr, sem:sem].
        nominal sub [n, np, det, num] intro [sem:n_sem].
        verbal sub [v, vp, s] intro [sem:v_sem, subcat:list].

    quantity sub [one, two, three].

    list sub [e_list, ne_list].
        ne_list intro [hd:bot, tl:list].

    % Define the type `agr` for agreement.

    % Hint: it should look something like this: 
    % agr intro [your_agr_feature_1:your_agr_type_1, ...].
    %     your_agr_type_1 sub [...].
    %     ...

    % === Your Code Here ===
    agr intro [number:number].
        number sub [singular, plural].
    % ======================


% Specifying the semantics for generation.
% Do not modify.
semantics sem1.
sem1(sem:S, S) if true.

% Lexicon

% Hint: Your lexical entries should look something like this: 
% token ---> (type,
%    feature_name_1:feature_type_1,
%    feature_name_2:feature_type_2, ...). 

% === Your Code Here ===
a ---> (det, sem:quantity:one, agr:number:singular).
one ---> (num, sem:quantity:one, agr:number:singular).
two ---> (num, sem:quantity:two, agr:number:plural).
three ---> (num, sem:quantity:three, agr:number:plural).
student ---> (n, sem:student, agr:number:singular).
students ---> (n, sem:student, agr:number:plural).
wolf ---> (n, sem:wolf, agr:number:singular).
wolves ---> (n, sem:wolf, agr:number:plural).
sheep ---> (n, sem:sheep, agr:number:singular).
sheep ---> (n, sem:sheep, agr:number:plural).
see ---> (v, sem:see, agr:number:plural, subcat:[
    (Obj, np),
    (Subj, np)
]).
sees ---> (v, sem:see, agr:number:singular, subcat:[
    (Obj, np),
    (Subj, np)
]).
saw ---> (v, sem:see, agr:number:plural, subcat:[
    (Obj, np),
    (Subj, np)
]).
saw ---> (v, sem:see, agr:number:singular, subcat:[
    (Obj, np),
    (Subj, np)
]).
chase ---> (v, sem:chase, agr:number:plural, subcat:[
    (Obj, np),
    (Subj, np)
]).
chases ---> (v, sem:chase, agr:number:singular, subcat:[
    (Obj, np),
    (Subj, np)
]).
chased ---> (v, sem:chase, agr:number:plural, subcat:[
    (Obj, np),
    (Subj, np)
]).
chased ---> (v, sem:chase, agr:number:singular, subcat:[
    (Obj, np),
    (Subj, np)
]).
% ======================


% Rules

% Hint: Your rules should look something like this: 

% rule_name rule
% (product_type, feature3:value3) ===>
% cat> (type1, feature1:value1),
% cat> (type2, feature2:value2).

% === Your Code Here ===
detnp rule
(np, sem:Sem, agr:Agr, sem:quantity:Detsem) ===>
cat> (det, agr:Agr, sem:quantity:Detsem),
sem_head> (n, agr:Agr, sem:Sem).

numnp rule
(np, sem:Sem, agr:Agr, sem:quantity:Numsem) ===>
cat> (num, agr:Agr, sem:quantity:Numsem),
sem_head> (n, agr:Agr, sem:Sem).

vp rule
(vp, sem:Verbsem, sem:obj:Objsem, agr:Agr, subcat:(Rest, [_|_])) ===>
sem_head> (v, sem:Verbsem, agr:Agr, subcat:[Obj|Rest]),
cat> (Obj, sem:Objsem).

s rule
(s, agr:Agr, sem:Verbsem, sem:obj:Objsem, sem:subj:Subjsem, subcat:([], Rest)) ===>
cat> (Subj, sem:Subjsem, agr:Agr),
sem_head> (vp, sem:Verbsem, sem:obj:Objsem, agr:Agr, subcat:[Subj|Rest]).
% ======================