# Student Name: Shilin Zhang
# Student Number: 1007065532
# UTORid: zhan9834

'''
This code is provided solely for the personal and private use of students
taking the CSC485H/2501H course at the University of Toronto. Copying for
purposes other than this use is expressly prohibited. All forms of
distribution of this code, including but not limited to public repositories on
GitHub, GitLab, Bitbucket, or any other online platform, whether as given or
with any changes, are expressly prohibited.

Authors: Jinman Zhao, Jingcheng Niu, Gerald Penn

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 University of Toronto
'''

import typing as T
from string import punctuation

from nltk.corpus import stopwords, wordnet as wn
from nltk.tokenize import word_tokenize


def deepest():
    """Find and print the synset with the largest maximum depth along with its
    depth on each of its hyperonym paths.

    Returns:
        None
    """
    ### YOUR CODE STARTS HERE
    max_depth = float('-inf')
    deepest_synset = None
    for synset in wn.all_synsets():
        if synset.max_depth() > max_depth:
            max_depth = synset.max_depth()
            deepest_synset = synset
    print(f"Deepest Synset {deepest_synset} with Max Depth {max_depth}")
    deepest_hypernym_paths = deepest_synset.hypernym_paths()
    for index in range(len(deepest_hypernym_paths)):
        hypernym_path = deepest_hypernym_paths[index]
        print(f"Path {index + 1}:")
        for depth in range(len(hypernym_path)):
            print(f"  {hypernym_path[depth]} (Depth: {depth})")



def superdefn(synset: str) -> T.List[str]:
    """Get the "superdefinition" of a synset. (Yes, superdefinition is a
    made-up word. All words are made up.)

    We define the superdefinition of a synset to be the list of word tokens,
    here as produced by word_tokenize, in the definitions of the synset, its
    hyperonyms, and its hyponyms.

    Args:
        synset (str): The name of the synset to look up

    Returns:
        list of str: The list of word tokens in the superdefinition of s

    Examples:
        >>> superdefn('toughen.v.01')
        ['make', 'tough', 'or', 'tougher', 'gain', 'strength', 'make', 'fit']
    """
    ### YOUR CODE STARTS HERE
    synset = wn.synset(synset)
    tokens = []
    tokens.extend(word_tokenize(synset.definition()))
    tokens.extend([token for hyperonym in synset.hypernyms() for token in word_tokenize(hyperonym.definition())])
    tokens.extend([token for hyponym in synset.hyponyms() for token in word_tokenize(hyponym.definition())])
    return tokens

def stop_tokenize(s: str) -> T.List[str]:
    """Word-tokenize and remove stop words and punctuation-only tokens.

    Args:
        s (str): String to tokenize

    Returns:
        list[str]: The non-stopword, non-punctuation tokens in s

    Examples:
        >>> stop_tokenize('The Dance of Eternity, sir')
        ['Dance', 'Eternity', 'sir']
    """
    ### YOUR CODE STARTS HERE
    tokens = word_tokenize(s)
    stop_words = stopwords.words('english')
    return_words = []
    for token in tokens:
        if token.lower() not in punctuation and token.lower() not in stop_words:
            return_words.append(token) 
    return return_words

if __name__ == '__main__':
    import doctest
    doctest.testmod()
