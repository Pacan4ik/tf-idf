import re
import math
from tfidfstat import lexicon


def tf(text: str):
    """
    Calculate term frequency (TF) for a given text.

    :param text: A string containing the text to analyze.
    :return: A Lexicon object representing the term frequencies (TF) of words in the text.

    Raises:
        TypeError: If the input text is not a string.

    The function calculates the term frequency (TF) for each word in the input text.
    The resulting Lexicon object contains this frequency information.
    """
    if not isinstance(text, str):
        raise TypeError('text must be a string')
    words = re.findall(r'\b\w+\b', text)
    lex = lexicon.Lexicon(words)
    return lex


def tfidf(texts: []):
    """
       Calculate TF-IDF (Term Frequency-Inverse Document Frequency) for a list of texts.

       :param texts: A list of strings, where each string represents a document.
       :return: A list of dictionaries, where each dictionary contains TF-IDF scores for words in the corresponding document.

       Raises:
           TypeError: If the input texts are not provided as a list.

       The function calculates TF-IDF scores for each word in each document within the provided list of texts.
       TF-IDF scores are computed as TF * IDF, where:
       - TF (Term Frequency) measures how frequently a word appears in a document.
       - IDF (Inverse Document Frequency) measures how important a word is across all documents.
       """
    if not isinstance(texts, list):
        raise TypeError('texts must be a list')
    data = [tf(text) for text in texts]
    res = []
    idf_cache = {}
    for stat in data:
        tfidfs = {}
        for word, values in stat:
            _, tf_value = values
            if word not in idf_cache:
                doc_count = sum(1 for other_stat in data if word in other_stat)
                idf = math.log(len(texts) / doc_count, 10)
                idf_cache[word] = idf
            else:
                idf = idf_cache[word]
            tfidfs[word] = tf_value * idf
        res.append(tfidfs)
    return res
