import nltk
from nltk.tokenize import word_tokenize
import re
import nltk
import string
import spacy
import os
import sys
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from spacy import Language, util

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS + '/'
else:
    application_path = ""


# Класс для представления статей
class Article:
    def __init__(self, file_name, file_text):
        self.file_name = file_name
        self.file_text = file_text

    def __repr__(self):
        return f"Статья {self.file_name}, текст статьи: {self.file_text}"


# Загрузка стоп-слов и пунктуации
with open(application_path + 'data/stopwords_all.txt', 'r', encoding='utf-8') as file1:
    stop_words = set(file1.read().splitlines())
nltk.download('punkt')
punctuation = string.punctuation
# Загрузка языковой модели spaCy
nlp = spacy.load(application_path + 'ru_core_news_sm')


@Language.component("merge_hyphenated_tokens")
def merge_hyphenated_tokens(doc):
    spans = []
    for i, token in enumerate(doc[:-1]):
        if token.text == '-' and doc[i + 1].text and doc[i - 1].text:
            spans.append(doc[i - 1:i + 2])
    spans = util.filter_spans(spans)
    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(span)
    return doc


nlp.add_pipe("merge_hyphenated_tokens", before="parser")


def text_extraction(path):
    extracted_text_array = []
    c = 0

    for filename in os.scandir(path):
        if filename.is_file():
            extracted_text_array.append(Article(filename.name, ''))

            for pagenum, page in enumerate(extract_pages(filename.path)):
                for element in page:
                    if isinstance(element, LTTextContainer):
                        s = (element.get_text().replace('-\n', '')
                             .replace(' - ', '')
                             .replace('\n', '').lower()
                             .replace('ё', 'е'))
                        extracted_text_array[c].file_text += str(s + " ")

        extracted_text_array[c].file_text = re.sub(r'[\d!\"#$%&\'()*+/<=>?@\[\]^_`{|}~]', ' ',
                                                   extracted_text_array[c].file_text)
        extracted_text_array[c].file_text = lemmatize(delete_stop_words(extracted_text_array[c].file_text))

        c += 1

    return extracted_text_array


def delete_stop_words(text):
    words = word_tokenize(text)  # Привести к нижнему регистру и токенизировать
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    return " ".join(filtered_words)


def lemmatize(text):
    doc = nlp(text)  # Лемматизируем текст
    lemmatized_words = [token.lemma_ for token in doc if token.text not in stop_words]
    return " ".join(lemmatized_words)
