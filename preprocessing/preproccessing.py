from nltk.tokenize import word_tokenize
import re
import nltk
import string
import os
import docx
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from utils import apppath, spacysingle
import pymupdf


# Класс для представления статей
class Article:
    def __init__(self, file_name, file_text):
        self.file_name = file_name
        self.file_text = file_text

    def __repr__(self):
        return f"Статья {self.file_name}, текст статьи: {self.file_text}"


# Загрузка стоп-слов и пунктуации
with open(apppath.get_stopwords_path(), 'r', encoding='utf-8') as file1:
    stop_words = set(file1.read().splitlines())

tokenizer_path = apppath.get_app_path() + 'data/nltk'
nltk.data.path.append(tokenizer_path)
punctuation = string.punctuation


def text_extraction(path):
    extracted_text_array = []
    c = 0

    for filename in os.scandir(path):
        if filename.is_file():
            extracted_text_array.append(Article(filename.name, ''))
            if filename.name.endswith('.docx'):
                doc = docx.Document(filename.path)
                for paragraph in doc.paragraphs:
                    s = paragraph.text.replace('-\n', '').replace('\n', '').lower().replace('ё', 'е')
                    extracted_text_array[c].file_text += str(s + " ")
            else:
                # for pagenum, page in enumerate(extract_pages(filename.path)):
                #     for element in page:
                #         if isinstance(element, LTTextContainer):
                #             s = (element.get_text().replace('-\n', '')
                #                  .replace(' - ', ' ')
                #                  .replace('\n', ' ').lower()
                #                  .replace('ё', 'е'))
                #             extracted_text_array[c].file_text += str(s + " ")
                doc = pymupdf.open(filename.path)
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    s = (page.get_text("text").replace('-\n', '')
                         .replace(' - ', ' ')
                         .replace('\n', ' ').lower()
                         .replace('ё', 'е'))
                    extracted_text_array[c].file_text += str(s + " ")

        extracted_text_array[c].file_text = re.sub(r'[\d!\"#$%&\'()*+/<=>?@\[\]^_`{|}~]', ' ',
                                                   extracted_text_array[c].file_text)
        extracted_text_array[c].file_text = lemmatize(delete_stop_words(extracted_text_array[c].file_text))
        extracted_text_array[c].file_name = extracted_text_array[c].file_name.replace('.pdf', '').replace('.docx', '')
        c += 1

    return extracted_text_array


def delete_stop_words(text):
    words = word_tokenize(text, language='russian')  # Привести к нижнему регистру и токенизировать
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    return " ".join(filtered_words)


def lemmatize(text):
    nlp = spacysingle.SpacyNlp.get_instance()
    doc = nlp(text)  # Лемматизируем текст
    lemmatized_words = [token.lemma_ for token in doc if token.text not in stop_words]
    return " ".join(lemmatized_words)
