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

from collections import Counter
from typing import *

from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset

import numpy as np
from numpy.linalg import norm

from q0 import stop_tokenize
from wsd import evaluate, load_eval, load_word2vec, WSDToken


def mfs(sent: Sequence[WSDToken], w_index: int) -> Synset:
    """Most frequent sense of a word.

    **IMPORTANT**: when looking up the word in WordNet, make sure you use the
    lemma of the word, *not* the wordform. See the WSDToken class in wsd.py
    for the relevant class attributes.

    Args:
        sent (list of WSDToken): The sentence containing the word to be
            disambiguated.
        w_index (int): The index of the target word in the sentence.

    Returns:
        Synset: The most frequent sense for the given word.
    """
    ### YOUR CODE STARTS HERE
    lemma = sent[w_index].lemma
    synsets = wn.synsets(lemma)
    return synsets[0] if synsets else None

def overlap(signature: List[str], context: List[str]) -> int:
    cardinality = 0
    context_copy = context.copy()
    for word in signature:
        if word in context_copy:
            context_copy.remove(word)
            cardinality += 1
    return cardinality


def lesk(sent: Sequence[WSDToken], w_index: int) -> Synset:
    """Simplified Lesk algorithm.

    **IMPORTANT**: when looking up the word in WordNet, make sure you use the
    lemma of the word, *not* the wordform. For other cases, such as gathering
    the context words, use the wordform. See the WSDToken class in wsd.py for
    the relevant class attributes.

    Args:
        sent (list of WSDToken): The sentence containing the word to be
            disambiguated.
        w_index (int): The index of the target word in the sentence.

    Returns:
        Synset: The prediction of the correct sense for the given word.
    """
    ### YOUR CODE STARTS HERE
    best_sense = mfs(sent, w_index)
    best_score = 0
    context = [token.wordform for token in sent]
    for synset in wn.synsets(sent[w_index].lemma):
        signature = stop_tokenize(synset.definition()) + [token for example in synset.examples() for token in stop_tokenize(example)]
        score = overlap(signature, context)
        if score > best_score:
            best_sense = synset
            best_score = score
    return best_sense

def lesk_ext(sent: Sequence[WSDToken], w_index: int) -> Synset:
    """Extended Lesk algorithm.

    **IMPORTANT**: when looking up the word in WordNet, make sure you use the
    lemma of the word, *not* the wordform. For other cases, such as gathering
    the context words, use the wordform. See the WSDToken class in wsd.py for
    the relevant class attributes.

    Args:
        sent (list of WSDToken): The sentence containing the word to be
            disambiguated.
        w_index (int): The index of the target word in the sentence.

    Returns:
        Synset: The prediction of the correct sense for the given word.
    """
    ### YOUR CODE STARTS HERE
    best_sense = mfs(sent, w_index)
    best_score = 0
    context = [token.wordform for token in sent]
    for synset in wn.synsets(sent[w_index].lemma):
        signature_set = set(
            [synset] + synset.hyponyms() + synset.member_holonyms() + synset.part_holonyms() + synset.substance_holonyms() + synset.member_meronyms() + synset.part_meronyms() + synset.substance_meronyms()
        )
        signature = []
        for inner_synset in signature_set:
            signature.extend(stop_tokenize(inner_synset.definition()))
            for example in inner_synset.examples():
                signature.extend(stop_tokenize(example))

        score = overlap(signature, context)
        if score > best_score:
            best_sense = synset
            best_score = score
    return best_sense

def lesk_cos(sent: Sequence[WSDToken], w_index: int) -> Synset:
    """Extended Lesk algorithm using cosine similarity.

    **IMPORTANT**: when looking up the word in WordNet, make sure you use the
    lemma of the word, *not* the wordform. For other cases, such as gathering
    the context words, use the wordform. See the WSDToken class in wsd.py for
    the relevant class attributes.

    Args:
        sent (list of WSDToken): The sentence containing the word to be
            disambiguated.
        w_index (int): The index of the target word in the sentence.

    Returns:
        Synset: The prediction of the correct sense for the given word.
    """
    ### YOUR CODE STARTS HERE
    best_sense = mfs(sent, w_index)
    best_score = 0
    context = [token.wordform for token in sent]
    for synset in wn.synsets(sent[w_index].lemma):
        signature_set = set(
            [synset] + synset.hyponyms() + synset.member_holonyms() + synset.part_holonyms() + synset.substance_holonyms() + synset.member_meronyms() + synset.part_meronyms() + synset.substance_meronyms()
        )
        signature = []
        for inner_synset in signature_set:
            signature.extend(stop_tokenize(inner_synset.definition()))
            for example in inner_synset.examples():
                signature.extend(stop_tokenize(example))

        all_words = context + signature
        vocabulary = []
        visited_words = set()
        for word in all_words:
            if word not in visited_words:
                visited_words.add(word)
                vocabulary.append(word)
        context_vector = [0] * len(vocabulary)
        signature_vector = [0] * len(vocabulary)
        for index in range(len(vocabulary)):
            word  = vocabulary[index]
            if word in context:
                context_vector[index] = context.count(word)
            if word in signature:
                signature_vector[index] = signature.count(word)
        score = (np.dot(context_vector, signature_vector)) / (norm(context_vector) * norm(signature_vector)) if norm(context_vector) != 0 and norm(signature_vector) != 0 else 0.0
        if score > best_score:
            best_sense = synset
            best_score = score
    return best_sense

def lesk_cos_onesided(sent: Sequence[WSDToken], w_index: int) -> Synset:
    """Extended Lesk algorithm using one-sided cosine similarity.

    **IMPORTANT**: when looking up the word in WordNet, make sure you use the
    lemma of the word, *not* the wordform. For other cases, such as gathering
    the context words, use the wordform. See the WSDToken class in wsd.py for
    the relevant class attributes.

    Args:
        sent (list of WSDToken): The sentence containing the word to be
            disambiguated.
        w_index (int): The index of the target word in the sentence.

    Returns:
        Synset: The prediction of the correct sense for the given word.
    """
    ### YOUR CODE STARTS HERE
    best_sense = mfs(sent, w_index)
    best_score = 0
    context = [token.wordform for token in sent]
    for synset in wn.synsets(sent[w_index].lemma):
        signature_set = set(
            [synset] + synset.hyponyms() + synset.member_holonyms() + synset.part_holonyms() + synset.substance_holonyms() + synset.member_meronyms() + synset.part_meronyms() + synset.substance_meronyms()
        )
        signature = []
        for inner_synset in signature_set:
            signature.extend(stop_tokenize(inner_synset.definition()))
            for example in inner_synset.examples():
                signature.extend(stop_tokenize(example))

        vocabulary = []
        visited_words = set()
        for word in context:
            if word not in visited_words:
                visited_words.add(word)
                vocabulary.append(word)
        context_vector = [0] * len(vocabulary)
        signature_vector = [0] * len(vocabulary)
        for index in range(len(vocabulary)):
            word  = vocabulary[index]
            if word in context:
                context_vector[index] = context.count(word)
            if word in signature:
                signature_vector[index] = signature.count(word)
        score = (np.dot(context_vector, signature_vector)) / (norm(context_vector) * norm(signature_vector)) if norm(context_vector) != 0 and norm(signature_vector) != 0 else 0.0
        if score > best_score:
            best_sense = synset
            best_score = score
    return best_sense

def word_vector_lookup(word: str, vocab: Mapping[str, int], word2vec: np.ndarray) -> np.ndarray:
    underscore_word = word.replace(" ", "_")
    if underscore_word in vocab:
        return word2vec[vocab[underscore_word]]
    elif underscore_word.lower() in vocab:
        return word2vec[vocab[underscore_word.lower()]]
    else:
        words = underscore_word.split("_")
        if len(words) == 1:
            return np.zeros(word2vec.shape[1])
        else:
            vectors = []
            for each_word in words:
                vectors.append(word_vector_lookup(each_word, vocab, word2vec))
            return np.average(vectors, axis=0)

def lesk_w2v(sent: Sequence[WSDToken], w_index: int,
             vocab: Mapping[str, int], word2vec: np.ndarray) -> Synset:
    """Extended Lesk algorithm using word2vec-based cosine similarity.

    **IMPORTANT**: when looking up the word in WordNet, make sure you use the
    lemma of the word, *not* the wordform. For other cases, such as gathering
    the context words, use the wordform. See the WSDToken class in wsd.py for
    the relevant class attributes.

    To look up the vector for a word, first you need to look up the word's
    index in the word2vec matrix, which you can then use to get the specific
    vector. More directly, you can look up a string s using word2vec[vocab[s]].

    To look up the vector for a *single word*, use the following rules:
    * If the word exists in the vocabulary, then return the corresponding
      vector.
    * Otherwise, if the lower-cased version of the word exists in the
      vocabulary, return the corresponding vector for the lower-cased version.
    * Otherwise, return a vector of all zeros. You'll need to ensure that
      this vector has the same dimensions as the word2vec vectors.

    But some wordforms are actually multi-word expressions and contain spaces.
    word2vec can handle multi-word expressions, but uses the underscore
    character to separate words rather than spaces. So, to look up a string
    that has a space in it, use the following rules:
    * If the string has a space in it, replace the space characters with
      underscore characters and then follow the above steps on the new string
      (i.e., try the string as-is, then the lower-cased version if that
      fails), but do not return the zero vector if the lookup fails.
    * If the version with underscores doesn't yield anything, split the
      string into multiple words according to the spaces and look each word
      up individually according to the rules in the above paragraph (i.e.,
      as-is, lower-cased, then zero). Take the mean of the vectors for each
      word and return that.
    Recursion will make for more compact code for these.

    Args:
        sentence (list of WSDToken): The sentence containing the word to be
            disambiguated.
        w_index (int): The index of the target word in the sentence.
        vocab (dictionary mapping str to int): The word2vec vocabulary,
            mapping strings to their respective indices in the word2vec array.
        word2vec (np.ndarray): The word2vec word vectors, as a VxD matrix,
            where V is the vocabulary and D is the dimensionality of the word
            vectors.

    Returns:
        Synset: The prediction of the correct sense for the given word.
    """
    ### YOUR CODE STARTS HERE
    best_sense = mfs(sent, w_index)
    best_score = 0
    context = set([token.wordform for token in sent])
    context_vector = np.average(np.array([word_vector_lookup(word, vocab, word2vec) for word in context]), axis=0)
    for synset in wn.synsets(sent[w_index].lemma):
        signature = set((
            stop_tokenize(synset.definition()) +
            [token for example in synset.examples() for token in stop_tokenize(example)] +
            [token for hyponym in synset.hyponyms() for token in stop_tokenize(hyponym.definition())] +
            [token for hyponym in synset.hyponyms() for example in hyponym.examples() for token in stop_tokenize(example)] +
            [token for member in synset.member_holonyms() for token in stop_tokenize(member.definition())] +
            [token for member in synset.member_holonyms() for example in member.examples() for token in stop_tokenize(example)] +
            [token for part in synset.part_holonyms() for token in stop_tokenize(part.definition())] +
            [token for part in synset.part_holonyms() for example in part.examples() for token in stop_tokenize(example)] +
            [token for substance in synset.substance_holonyms() for token in stop_tokenize(substance.definition())] +
            [token for substance in synset.substance_holonyms() for example in substance.examples() for token in stop_tokenize(example)] +
            [token for member in synset.member_meronyms() for token in stop_tokenize(member.definition())] +
            [token for member in synset.member_meronyms() for example in member.examples() for token in stop_tokenize(example)] +
            [token for part in synset.part_meronyms() for token in stop_tokenize(part.definition())] +
            [token for part in synset.part_meronyms() for example in part.examples() for token in stop_tokenize(example)] +
            [token for substance in synset.substance_meronyms() for token in stop_tokenize(substance.definition())] +
            [token for substance in synset.substance_meronyms() for example in substance.examples() for token in stop_tokenize(example)]
        ))
        signature_vector = np.average(np.array([word_vector_lookup(word, vocab, word2vec) for word in signature]), axis=0)
        score = (np.dot(context_vector, signature_vector)) / (norm(context_vector) * norm(signature_vector)) if norm(context_vector) != 0 and norm(signature_vector) != 0 else 0.0
        if score > best_score:
            best_sense = synset
            best_score = score
    return best_sense

if __name__ == '__main__':
    np.random.seed(1234)
    eval_data = load_eval()
    for wsd_func in [mfs, lesk, lesk_ext, lesk_cos, lesk_cos_onesided]:
        evaluate(eval_data, wsd_func)

    evaluate(eval_data, lesk_w2v, *load_word2vec())
