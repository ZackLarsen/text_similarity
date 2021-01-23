"""
Command-line interface to compare the similarity of two texts
Zack Larsen
January 23, 2021
"""

import re
from collections import defaultdict, Counter, OrderedDict

punctuation = [',',
'.',
'!',
'?',
'-',
':',
';'
]


stopwords = ['a',
'about',
'above',
'after',
'again',
'against',
'all',
'am',
'an',
'and',
'any',
'are',
'aren\'t',
'as',
'at',
'be',
'because',
'been',
'before',
'being',
'below',
'between',
'both',
'but',
'by',
'can\'t',
'cannot',
'could',
'couldn\'t',
'did',
'didn\'t',
'do',
'does',
'doesn\'t',
'doing',
'don\'t',
'down',
'during',
'each',
'few',
'for',
'from',
'further',
'had',
'hadn\'t',
'has',
'hasn\'t',
'have',
'haven\'t',
'having',
'he',
'he\'d',
'he\'ll',
'he\'s',
'her',
'here',
'here\'s',
'hers',
'herself',
'him',
'himself',
'his',
'how',
'how\'s',
'i',
'i\'d',
'i\'ll',
'i\'m',
'i\'ve',
'if',
'in',
'into',
'is',
'isn\'t',
'it',
'it\'s',
'its',
'itself',
'let\'s',
'me',
'more',
'most',
'mustn\'t',
'my',
'myself',
'no',
'nor',
'not',
'of',
'off',
'on',
'once',
'only',
'or',
'other',
'ought',
'our',
'ours',
'ourselves',
'out',
'over',
'own',
'same',
'shan\'t',
'she',
'she\'d',
'she\'ll',
'she\'s',
'should',
'shouldn\'t',
'so',
'some',
'such',
'than',
'that',
'that\'s',
'the',
'their',
'theirs',
'them',
'themselves',
'then',
'there',
'there\'s',
'these',
'they',
'they\'d',
'they\'ll',
'they\'re',
'they\'ve',
'this',
'those',
'through',
'to',
'too',
'under',
'until',
'up',
'very',
'was',
'wasn\'t',
'we',
'we\'d',
'we\'ll',
'we\'re',
'we\'ve',
'were',
'weren\'t',
'what',
'what\'s',
'when',
'when\'s',
'where',
'where\'s',
'which',
'while',
'who',
'who\'s',
'whom',
'why',
'why\'s',
'with',
'won\'t',
'would',
'wouldn\'t',
'you',
'you\'d',
'you\'ll',
'you\'re',
'you\'ve',
'your',
'yours',
'yourself',
'yourselves',
]

def find_ngrams(input_list, n=3):
    """
    Construct an iterator to yield ngrams from a token list
    :param input_list: List of tokens
    :param n: Length of the ngram. Defaults to 3
    :return:
    """
    return zip(*[input_list[i:] for i in range(n)])


def jaccard_similarity(x, y):
    """
    Compute the Jaccard similarity between two lists of items, typically tokens in a text string
    :param x: First list
    :param y: Second list
    :return:
    """
    intersection = set(x).intersection(set(y))
    union = set(x).union(set(y))
    return len(intersection)/len(union)


def prep_texts(x, y, remove_stopwords=True, remove_punctuation=True):
    """
    Preprocess the input text
    :param x: First text
    :param y: Second text
    :param remove_stopwords: Boolean True/False whether or not to remove common words
    :param remove_punctuation: Boolean True/False whether or not to remove punctuation marks
    :return: Preprocessed token lists
    """
    # Tokenize the input texts
    x_tokens = re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", x)
    y_tokens = re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", y)

    # Lowercase
    x_tokens = [i.lower() for i in x_tokens]
    y_tokens = [i.lower() for i in y_tokens]

    # Remove punctuation (optional)
    if remove_punctuation:
        x_tokens = [i for i in x_tokens if i not in punctuation]
        y_tokens = [i for i in y_tokens if i not in punctuation]

    # Remove common stopwords (optional)
    if remove_stopwords:
        x_tokens = [i for i in x_tokens if i not in stopwords]
        y_tokens = [i for i in y_tokens if i not in stopwords]

    # Convert tokens to numeric with dictionary mapping
    all_tokens = {x for x in x_tokens + y_tokens}
    indexer = {v: k for k, v in enumerate(OrderedDict.fromkeys(all_tokens))}

    # Convert x_tokens to numeric
    numeric_x_tokens = [indexer[i] for i in x_tokens]

    # Convert y_tokens to numeric
    numeric_y_tokens = [indexer[i] for i in y_tokens]

    return numeric_x_tokens, numeric_y_tokens


def compare_texts(x, y, ngram_length=3, preserve_order=True, remove_stopwords=True, remove_punctuation=True):
    """
    Function to compare the similarity of two texts.
    Output is a similarity score based on Jaccard similarity, where
    a score of 1 indicates exact texts and a score of 0 indicates no
    commonality between the texts
    :param x: Text 1
    :param y: Text 2
    :param ngram_length: Option for considering bigrams, trigrams, etc.
    :param preserve_order: Boolean True/False whether or not to consider the order of the words
    :param remove_stopwords: Boolean True/False whether or not to remove common words
    :param remove_punctuation: Boolean True/False whether or not to remove punctuation in calculations
    :return: similarity score: The individual or combined similarity scores of the texts
    """
    # Preprocess the input texts
    x_tokens, y_tokens = prep_texts(x, y, remove_stopwords, remove_punctuation)

    # Find the ngrams for each numeric token list
    x_ngrams = [i for i in find_ngrams(x_tokens, ngram_length)]
    y_ngrams = [i for i in find_ngrams(y_tokens, ngram_length)]

    # Compute individual similarity scores
    token_similarity = jaccard_similarity(x_tokens, y_tokens)
    ngram_similarity = jaccard_similarity(x_ngrams, y_ngrams)

    # Compute individual or combined similarity score
    if preserve_order:
        similarity_score = token_similarity * ngram_similarity
    elif not preserve_order:
        similarity_score = token_similarity

    return similarity_score


def get_bool(prompt):
    """
    Convenience function for handling errors in arguments supplied by the user
    :param prompt:
    :return:
    """
    while True:
        try:
           return {"true":True,"false":False}[input(prompt).lower()]
        except KeyError:
           print("Invalid input; please enter True or False.")


if __name__ == '__main__':
    text_1 = str(input("Please write the first text: "))
    text_2 = str(input("Please write the second text: "))
    final_similarity_score = compare_texts(text_1, text_2, ngram_length=3, preserve_order=False, remove_stopwords=True, remove_punctuation=True)
    print("The similarity of these two texts is a score of: ", final_similarity_score)
