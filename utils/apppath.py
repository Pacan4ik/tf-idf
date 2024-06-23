import os
import sys

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS + '/'
else:
    application_path = ""


def get_app_path():
    return application_path
