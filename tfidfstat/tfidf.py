import re
import math
from preprocessing.preproccessing import Article
from tfidfstat.lexicon import Lexicon
from typing import List, Tuple
import spacy

nlp = spacy.load('ru_core_news_sm')
nlp.add_pipe("merge_hyphenated_tokens", before="parser")


def tf(text: str) -> Lexicon:
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
    pattern = re.compile(r'^[а-яА-ЯёЁ]+-?[а-яА-ЯёЁ]+$')
    doc = nlp(text)
    prev_pos = 'NAN'
    prev_text = ''
    terms = []

    # for token in doc:
    #     print(token.text)

    for token in doc:
        if pattern.match(token.text):
            terms.append(token.text)
            if token.pos_ == 'NOUN' and prev_pos == 'ADJ':
                terms.append(prev_text + ' ' + token.text)
            prev_pos = token.pos_
            prev_text = token.text
        elif token.pos_ == 'PUNCT':
            prev_pos = token.pos_
            prev_text = token.text
        else:
            prev_pos = 'NAN'
            prev_text = ''

    lex = Lexicon(terms)
    return lex


def tfidf(articles: List[Article]) -> List[Tuple[Article, dict]]:
    """
       Calculate TF-IDF (Term Frequency-Inverse Document Frequency) for a list of Article objects.

       :param articles: A list of Article objects, where each Article represents a document.
       :return: A list of tuples, where each tuple contains an Article object and a dictionary with TF-IDF scores
        for words in the corresponding document.

       Raises:
        TypeError: If the input is not provided as a list of Article objects.
        UserWarning: If the list of articles contains fewer than 2 elements.

       The function calculates TF-IDF scores for each word in each document within the provided list of articles.
       TF-IDF scores are computed as TF * IDF, where:
       - TF (Term Frequency) measures how frequently a word appears in a document.
       - IDF (Inverse Document Frequency) measures how important a word is across all documents.
       """
    if not isinstance(articles, list) or not all(isinstance(article, Article) for article in articles):
        raise TypeError('articles must be a list of Article objects')
    if len(articles) < 2:
        raise UserWarning('articles must contain at least 2 elements')
    data = [(article, tf(article.file_text)) for article in articles]
    res = []
    idf_cache = {}
    for article, stat in data:
        tfidfs = {}
        for word, values in stat:
            _, tf_value = values
            if word not in idf_cache:
                doc_count = sum(1 for other_article, other_stat in data if word in other_stat)
                idf = math.log(len(articles) / doc_count, 1.5)
                idf_cache[word] = idf
            else:
                idf = idf_cache[word]
            tfidfs[word] = tf_value * idf
        res.append((article, tfidfs))
    return res
