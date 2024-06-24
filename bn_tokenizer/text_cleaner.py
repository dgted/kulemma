"""
This cleantext scripts functions solely depends on clean-text library.
Most of the functions are copied from clean-text.
"""
import re

from library.bn_tokenizer import constants

from ftfy import fix_text
from unicodedata import normalize


def fix_bad_unicode(text, normalization="NFC"):
    return fix_text(text, normalization=normalization)


def fix_strange_quotes(text):
    """
    Replace strange quotes, i.e., 〞with a single quote ' or a double quote " if it fits better.
    """
    text = constants.SINGLE_QUOTE_REGEX.sub("'", text)
    text = constants.DOUBLE_QUOTE_REGEX.sub('"', text)
    return text


def replace_urls(text, replace_with=""):
    """
    Replace all URLs in ``text`` str with ``replace_with`` str.
    """
    return constants.URL_REGEX.sub(replace_with, text)


def remove_number_or_digit(text, replace_with=""):
    return re.sub(constants.BANGLA_DIGIT_REGEX, replace_with, text)


def remove_punctuations(text, replace_with=""):
    for punc in constants.punctuations_sentence:
        text = text.replace(punc, " ")

    for punc in constants.punctuations:
        text = text.replace(punc, replace_with)

    return text


class TextCleaner(object):
    def __init__(self, unicode_norm_form=None):
        self.unicode_norm_form = unicode_norm_form

    def __call__(self, text: str) -> str:
        if text is None:
            text = ""

        text = str(text)
        text = fix_strange_quotes(text)
        text = fix_bad_unicode(text)
        text = remove_number_or_digit(text)
        text = replace_urls(text)
        text = remove_punctuations(text)

        if self.unicode_norm_form:
            text = normalize(self.unicode_norm_form, text)

        return text
