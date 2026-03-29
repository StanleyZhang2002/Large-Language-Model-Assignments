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
lan(zh).
question(q1).

% Type Feature Structure

% Do not modify lines 25-39.
bot sub [cat, sem, agr, cl_types, list].
    sem sub [n_sem, v_sem].
        n_sem sub [student, wolf, sheep] intro [quantity:quantity].
        v_sem sub [chase, see] intro [subj:sem, obj:sem].

    cl_types sub [ge, ming, zhi, pi].

    cat sub [nominal, verbal] intro [agr:agr, sem:sem].
        nominal sub [n, np, clp, num, cl] intro [sem:n_sem].
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
    agr intro [classifier:classifier].
        classifier sub [cl_types].
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
yi ---> (num, sem:quantity:one).
liang ---> (num, sem:quantity:two).
san ---> (num, sem:quantity:three).
xuesheng ---> (n, sem:student, agr:classifier:ge).
xuesheng ---> (n, sem:student, agr:classifier:ming).
lang ---> (n, sem:wolf, agr:classifier:zhi).
lang ---> (n, sem:wolf, agr:classifier:pi).
yang ---> (n, sem:sheep, agr:classifier:zhi).
zhuizhu ---> (v, sem:chase, subcat:[
    (Obj, np),
    (Subj, np)
]).
kanjian ---> (v, sem:see, subcat:[
    (Obj, np),
    (Subj, np)
]).
ge ---> (cl, agr:classifier:ge).
ming ---> (cl, agr:classifier:ming).
zhi ---> (cl, agr:classifier:zhi).
pi ---> (cl, agr:classifier:pi).
% ======================


% Rules

% Hint: Your rules should look something like this: 

% rule_name rule
% (product_type, feature3:value3) ===>
% cat> (type1, feature1:value1),
% cat> (type2, feature2:value2).

% === Your Code Here ===
clp rule
(clp, sem:quantity:Sem, agr:Agr) ===>
cat> (num, sem:quantity:Sem),
sem_head> (cl, agr:Agr).

np rule
(np, sem:Sem, agr:Agr, sem:quantity:Numsem) ===>
cat> (clp, agr:Agr, sem:quantity:Numsem),
sem_head> (n, agr:Agr, sem:Sem).

vp rule
(vp, sem:Verbsem, sem:obj:Objsem, subcat:(Rest, [_|_])) ===>
sem_head> (v, sem:Verbsem, subcat:[Obj|Rest]),
cat> (Obj, sem:Objsem).

s rule
(s, sem:Verbsem, sem:obj:Objsem, sem:subj:Subjsem, subcat:([], Rest)) ===>
cat> (Subj, sem:Subjsem),
sem_head> (vp, sem:Verbsem, sem:obj:Objsem, subcat:[Subj|Rest]).
% ======================
