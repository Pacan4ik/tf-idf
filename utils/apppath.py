import os
import sys

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS + '/'
else:
    application_path = ""


def get_app_path():
    return application_path


def get_stopwords_path():
    stopwords = os.getenv('STOPWORDS_PATH')
    if stopwords is not None:
        return stopwords
    else:
        return get_app_path() + 'data/stopwords_all.txt'
