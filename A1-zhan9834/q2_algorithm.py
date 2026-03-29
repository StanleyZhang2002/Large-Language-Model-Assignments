# Student name: Shilin Zhang
# Student number: 1007065532
# UTORid: zhan9834

'''
This code is provided solely for the personal and private use of students
taking the CSC485H/2501H course at the University of Toronto. Copying for
purposes other than this use is expressly prohibited. All forms of
distribution of this code, including but not limited to public repositories on
GitHub, GitLab, Bitbucket, or any other online platform, whether as given or
with any changes, are expressly prohibited.

Authors: Zixin Zhao, Jinman Zhao, Jingcheng Niu, Zhewei Sun

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 University of Toronto
'''

import typing as T
from math import inf

import torch
from torch.nn.functional import pad
from torch import Tensor
import einops


def is_projective(heads: T.Iterable[int]) -> bool:
    """
    Determines whether the dependency tree for a sentence is projective.

    Args:
        heads: The indices of the heads of the words in sentence. Since ROOT
          has no head, it is not expected to be part of the input, but the
          index values in heads are such that ROOT is assumed in the
          starting (zeroth) position. See the examples below.

    Returns:
        True if and only if the tree represented by the input is
          projective.

    Examples:
        The projective tree from the assignment handout:
        >>> is_projective([2, 5, 4, 2, 0, 7, 5, 7])
        True

        The non-projective tree from the assignment handout:
        >>> is_projective([2, 0, 2, 2, 6, 3, 6])
        False
    """
    projective = True
    # *** ENTER YOUR CODE BELOW *** #
    dependecies = [(index + 1, heads[index]) for index in range(len(heads))]
    for i in range(len(dependecies)):
        for j in range(len(dependecies)):
            if i != j:
                first_word_in_dependency_i = min(dependecies[i][0], dependecies[i][1])
                second_word_in_dependency_i = max(dependecies[i][0], dependecies[i][1])
                first_word_in_dependency_j = min(dependecies[j][0], dependecies[j][1])
                second_word_in_dependency_j = max(dependecies[j][0], dependecies[j][1])
                if first_word_in_dependency_i < first_word_in_dependency_j < second_word_in_dependency_i < second_word_in_dependency_j:
                    return False
                if first_word_in_dependency_j < first_word_in_dependency_i < second_word_in_dependency_j < second_word_in_dependency_i:
                    return False
    return projective


def is_single_root(heads: Tensor, lengths: Tensor) -> Tensor:
    """
    Determines whether the selected arcs for a sentence constitute a tree with
    a single root word.

    Remember that index 0 indicates the ROOT node. A tree with "a single root
    word" has exactly one outgoing edge from ROOT.

    If you like, you may add helper functions to this file for this function.

    This file already imports the function `pad` for you. You may find that
    function handy. Here's the documentation of the function:
    https://pytorch.org/docs/stable/generated/torch.nn.functional.pad.html

    Args:
        heads (Tensor): a Tensor of dimensions (batch_sz, sent_len) and dtype
            int where the entry at index (b, i) indicates the index of the
            predicted head for vertex i for input b in the batch

        lengths (Tensor): a Tensor of dimensions (batch_sz,) and dtype int
            where each element indicates the number of words (this doesn't
            include ROOT) in the corresponding sentence.

    Returns:
        A Tensor of dtype bool and dimensions (batch_sz,) where the value
        for each element is True if and only if the corresponding arcs
        constitute a single-root-word tree as defined above

    Examples:
        Valid trees from the assignment handout:
        >>> is_single_root(torch.tensor([[2, 5, 4, 2, 0, 7, 5, 7],\
                                              [2, 0, 2, 2, 6, 3, 6, 0]]),\
                                torch.tensor([8, 7]))
        tensor([True, True])

        Invalid trees (the first has a cycle; the second has multiple roots):
        >>> is_single_root(torch.tensor([[2, 5, 4, 2, 0, 8, 6, 7],\
                                              [2, 0, 2, 2, 6, 3, 6, 0]]),\
                                torch.tensor([8, 8]))
        tensor([False, False])
    """
    # *** ENTER YOUR CODE BELOW *** #
    def check_tree_structure(heads_row, sentence_length):
        root_vertex = 0
        graph = [[] for _ in range(sentence_length + 1)]
        root_edge_count = 0
        for index in range(sentence_length):
            head = heads_row[index].item()
            if head == root_vertex:
                root_edge_count += 1
            graph[head].append(index + 1)
        if root_edge_count != 1:
            return False
        visited = [False] * (sentence_length + 1)
        parent = [None] * (sentence_length + 1)

        def dfs(node):
            visited[node] = True
            for child in graph[node]:
                if not visited[child]:
                    parent[child] = node
                    if dfs(child):
                        return True
                elif parent[node] != child:
                    return True
            return False
        
        contains_cycle = dfs(0)
        connectedness = all(visited)
        num_edges = sum(len(child_list) for child_list in graph)
        
        return not contains_cycle and connectedness and num_edges == sentence_length

    tree_single_root = torch.ones_like(heads[:, 0], dtype=torch.bool)
    for index, sentence in enumerate(heads):
        tree_single_root[index] = check_tree_structure(sentence[:lengths[index]], lengths[index])
    return tree_single_root


def mst_single_root(arc_tensor: Tensor, lengths: Tensor) -> Tensor:
    """
    Finds the maximum spanning tree (more technically, arborescence) for the
    given sentences such that each tree has a single root word.

    Remember that index 0 indicates the ROOT node. A tree with "a single root
    word" has exactly one outgoing edge from ROOT.

    If you like, you may add helper functions to this file for this function.

    This file already imports the function `pad` for you. You may find that
    function handy. Here's the documentation of the function:
    https://pytorch.org/docs/stable/generated/torch.nn.functional.pad.html

    Args:
        arc_tensor (Tensor): a Tensor of dimensions (batch_sz, x, y) and dtype
            float where x=y and the entry at index (b, i, j) indicates the
            score for a candidate arc from vertex j to vertex i.

        lengths (Tensor): a Tensor of dimensions (batch_sz,) and dtype int
            where each element indicates the number of words (this doesn't
            include ROOT) in the corresponding sentence.

    Returns:
        A Tensor of dtype int and dimensions (batch_sz, x) where the value at
        index (b, i) indicates the head for vertex i according to the
        maximum spanning tree for the input graph.

    Examples:
        >>> mst_single_root(torch.tensor(\
            [[[0, 0, 0, 0],\
              [12, 0, 6, 5],\
              [4, 5, 0, 7],\
              [4, 7, 8, 0]],\
             [[0, 0, 0, 0],\
              [1.5, 0, 4, 0],\
              [2, 0.1, 0, 0],\
              [0, 0, 0, 0]],\
             [[0, 0, 0, 0],\
              [4, 0, 3, 1],\
              [6, 2, 0, 1],\
              [1, 1, 8, 0]]]),\
            torch.tensor([3, 2, 3]))
        tensor([[0, 0, 3, 1],
                [0, 2, 0, 0],
                [0, 2, 0, 2]])
    """
    # I read the Chu-Liu Edmonds Algorithm description on https://wendy-xiao.github.io/posts/2020-07-10-chuliuemdond_algorithm/ then implemented my version of the algorithm
    # *** ENTER YOUR CODE BELOW *** #
    def find_mst(graph, root_node):
        inverted_graph = {}
        max_score_graph = {}
        expanded_graph = {}
        in_virtual_index = {}
        out_virtual_index = {}
        vertices = graph.keys()
        cycle = None
        inverted_graph[root_node] = {}
        for head in graph.keys():
            for dependent in graph[head].keys():
                if dependent not in inverted_graph.keys():
                    inverted_graph[dependent] = {}
                inverted_graph[dependent][head] = graph[head][dependent]
        for dependent in (node for node in inverted_graph if node != root_node):
            max_weight = float('-inf')
            max_src = None
            for head in inverted_graph[dependent]:
                if inverted_graph[dependent][head] > max_weight:
                    max_weight = inverted_graph[dependent][head]
                    max_src = head
            max_score_graph[dependent] = {max_src: max_weight}
        for starting_node in max_score_graph.keys():
            visited_nodes = []
            stack = [starting_node]
            while stack:
                current_node = stack.pop()
                if current_node in visited_nodes:
                    cycle = []
                    while current_node not in cycle:
                        cycle.append(current_node)
                        current_node = list(max_score_graph[current_node].keys())[0]
                    break
                visited_nodes.append(current_node)
                if current_node in max_score_graph.keys():
                    stack.extend(list(max_score_graph[current_node].keys()))
            if cycle is not None:
                break
        if cycle is None:
            transformed_dict = {}
            for dependent, heads in max_score_graph.items():
                for head, w in heads.items():
                    if head not in transformed_dict:
                        transformed_dict[head] = {}
                    transformed_dict[head][dependent] = w
            return transformed_dict
        virtual_node = max(vertices) + 1
        for head in vertices:
            for dependent in graph[head].keys():
                if (head in cycle) and (dependent not in cycle):
                    if virtual_node not in expanded_graph:
                        expanded_graph[virtual_node] = {}
                    weight = graph[head][dependent]
                    if (dependent not in expanded_graph[virtual_node]) or (weight > expanded_graph[virtual_node][dependent]):
                        expanded_graph[virtual_node][dependent] = weight
                        out_virtual_index[dependent] = head
                elif (head not in cycle) and (dependent in cycle):
                    if head not in expanded_graph:
                        expanded_graph[head] = {}
                    weight = graph[head][dependent] - [value for value in max_score_graph[dependent].values()][0]
                    if (virtual_node not in expanded_graph[head]) or (weight > expanded_graph[head][virtual_node]):
                        expanded_graph[head][virtual_node] = weight
                        in_virtual_index[head] = dependent
                elif(head not in cycle) and (dependent not in cycle):
                    if head not in expanded_graph:
                        expanded_graph[head] = {}
                    expanded_graph[head][dependent] = graph[head][dependent]
        maximum_tree = find_mst(expanded_graph, root_node)
        all_nodes_max_tree = list(maximum_tree.keys())
        for head in all_nodes_max_tree:
            if head == virtual_node:
                for node_in_cycle in list(maximum_tree[head].keys()):
                    original_out = out_virtual_index[node_in_cycle]
                    if original_out not in maximum_tree:
                        maximum_tree[original_out] = {}
                    maximum_tree[original_out][node_in_cycle] = graph[original_out][node_in_cycle]
            else:
                for dependent in list(maximum_tree[head].keys()):
                    if dependent == virtual_node:
                        original_in = in_virtual_index[head]
                        maximum_tree[head][original_in] = graph[head][original_in]
                        del maximum_tree[head][dependent]
        maximum_tree.pop(virtual_node, None)
        for node in cycle:
            if node != original_in:
                source = list(max_score_graph[node].keys())[0]
                if source not in maximum_tree:
                    maximum_tree[source] = {}
                maximum_tree[source][node] = max_score_graph[node][source]
        return maximum_tree
    
    best_arcs = arc_tensor.argmax(-1)
    optimal_arcs = []
    for index in range(arc_tensor.size(0)):
        heads = [0] * (lengths[index] + 1)
        graph = {}
        score_mapping = arc_tensor[index, :lengths[index]+1, :lengths[index]+1]
        for row_index in range(score_mapping.size(0)):
            graph[row_index] = {}
            for col_index in range(score_mapping.size(1)):
                if col_index != row_index and col_index != 0:
                    graph[row_index][col_index] = score_mapping[col_index, row_index].item()
        mst = find_mst(graph, 0)
        root_count = len(mst.get(0, {}))
        if root_count != 1:
            best_score_so_far = float('-inf')
            best_mst = mst
            for possible_root in range(1, lengths[index].item() + 1):
                graph_with_possible_root = {i: j.copy() for i, j in graph.items() if i != 0}
                possible_mst = find_mst(graph_with_possible_root, possible_root)
                score = sum(weight for dep_map in possible_mst.values() for weight in dep_map.values()) + graph[0][possible_root]
                possible_mst[0] = {possible_root: graph[0][possible_root]}
                if score > best_score_so_far:
                    best_score_so_far = score
                    best_mst = possible_mst
            mst = best_mst
        for head, dep_map in mst.items():
            for dependent in dep_map.keys():
                heads[dependent] = head
        optimal_arcs.append(heads)
    optimal_arcs = [arc + [0] * (max(map(len, optimal_arcs)) - len(arc)) for arc in optimal_arcs]
    best_arcs = torch.tensor(optimal_arcs, device=arc_tensor.device)
    return best_arcs


if __name__ == '__main__':
    import doctest
    doctest.testmod()
