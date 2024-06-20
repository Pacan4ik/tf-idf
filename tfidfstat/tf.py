from collections import Counter
import re


def tf(text):
    if not isinstance(text, str):
        raise TypeError('text must be a string')
    words = re.findall(r'\b\w+\b', text)
    dictionary = Counter(words)
    return Counter(dictionary)
