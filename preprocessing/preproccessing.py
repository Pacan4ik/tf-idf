import nltk
from nltk.tokenize import word_tokenize
import re
import string
import spacy
from spacy.lang.ru.examples import sentences
import os
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer

# Загрузка стоп-слов и пунктуации
with open('data/stopwords_all.txt', 'r', encoding='utf-8') as file1:
    stop_words = set(file1.read().splitlines())
punctuation = string.punctuation
# Загрузка языковой модели spaCy
nlp = spacy.load("ru_core_news_sm")


def text_extraction(path):
    extracted_text_array = []
    c = 0

    for filename in os.scandir(path):
        if filename.is_file():
            extracted_text_array.append('')

            for pagenum, page in enumerate(extract_pages(filename.path)):
                for element in page:
                    if isinstance(element, LTTextContainer):
                        s = element.get_text().replace('\n', '').lower().replace('ё', 'е')
                        if (s[-1] != '-'):
                            extracted_text_array[c] += str(s + " ")
                        else:
                            extracted_text_array[c] += str(s)
        extracted_text_array[c] = re.sub(r'[\d!\"#$%&\'()*+,./:;<=>?@\[\]^_`{|}~]', ' ', extracted_text_array[c])

        extracted_text_array[c] = lemmatize(delete_stop_words(extracted_text_array[c]))

        c += 1

    return extracted_text_array


def delete_stop_words(text):
    nltk.download('punkt')
    words = word_tokenize(text)  # Привести к нижнему регистру и токенизировать
    filtered_words = [word for word in words if word not in stop_words and word not in punctuation]
    return " ".join(filtered_words)


def lemmatize(text):
    doc = nlp(text)  # Лемматизируем текст
    lemmatized_words = [token.lemma_ for token in doc if token.text not in punctuation and token.text not in stop_words]
    return " ".join(lemmatized_words)
