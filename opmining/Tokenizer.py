import nltk,re
from nltk import WhitespaceTokenizer


class Tokenizer:
    """Tokenizing Utilities Class"""
    __PATTERNS__ = '''([A-Za-z]+n[']t)|\\$?\\d+(\\.\\d+)?%?|\\w+(-\\w+)*|\\.\\.\\.|[][.,;"\?!():-_`]'''

    def __init__(self, patterns = None):
        if patterns:
            p = ''
            for pattern in patterns:
                p += pattern + '|'

            self.__PATTERNS__ = p + self.__PATTERNS__

    def sent_tokenize(self, content):
        return nltk.sent_tokenize(content)

    def word_tokenize(self, content):
        return nltk.regexp_tokenize(content, self.__PATTERNS__, flags=re.IGNORECASE)
