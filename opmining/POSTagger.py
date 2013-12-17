#!/usr/bin/python2.7

import nltk


class POSTagger:
    """This is a utility class for all POS Tagging related tasks"""
    def ntlk_tag(self, tokens):
        return nltk.pos_tag(tokens)

    def stemmer(self, tokens, type = 'plurals'):

        if type == 'plurals':
            wnl = nltk.WordNetLemmatizer()
            return [wnl.lemmatize(token) for token in tokens]
