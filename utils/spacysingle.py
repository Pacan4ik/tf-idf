import spacy
from spacy import Language, util
from utils import apppath


class SpacyNlp:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            nlp = spacy.load(apppath.get_app_path() + 'ru_core_news_lg')
            #nlp.add_pipe("merge_hyphenated_tokens", before="parser")
            cls._instance = nlp
        return cls._instance


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
