import PyPDF2
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer
def textExtraction (path):
    extractedTextArray = []
    for pagenum, page in enumerate(extract_pages(path)):
        for element in page:
            # Проверяем, является ли элемент текстовым
            if isinstance(element, LTTextContainer):
                line_text = element.get_text()
                pass
                # Функция для извлечения формата текста
                pass
    return 0