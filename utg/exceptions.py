# coding: utf-8

class UtgError(Exception):
    MSG = None

    def __init__(self, **kwargs):
        super(UtgError, self).__init__(self.MSG % kwargs)
        self.arguments = kwargs



class WordsError(UtgError):
    pass


class DuplicateWordError(WordsError):
    MSG = u'duplicate word in dictionary, type: %(type)s, normal form: %(normal_form)s'

class UnknownVerboseIdError(WordsError):
    MSG = u'Unknown verbose id: %(verbose_id)s'


class ExternalDependecyNotFoundError(WordsError):
    MSG = u'External dependency not found: %(dependency)s'


class WrongDependencyFormatError(WordsError):
    MSG = u'wrong dependency format: %(dependency)s'


class NoWordsFoundError(WordsError):
    MSG = u'no words found for text="%(text)s" and type=%(type)s'


class MoreThenOneWordFoundError(WordsError):
    MSG = u'more then one word found for text="%(text)s" and type=%(type)s'


class UnknownLexiconKeyError(WordsError):
    MSG = u'unknown lexicon key: %(key)s'


class TransformatorsError(UtgError):
    pass

class UnknownIntegerFormError(TransformatorsError):
    MSG = u'unknown integer form: %(form)s'
