# coding: utf-8

class UtgError(Exception):
    MSG = None

    def __init__(self, **kwargs):
        super(UtgError, self).__init__(self.MSG % kwargs)
        self.arguments = kwargs



class WordsError(UtgError):
    pass


class WrongFormsNumberError(WordsError):
    MSG = 'constuctor of word receive wrong number of forms (%(wrong_number)s intead of %(expected_number)s), forms are: %(forms)s'

class DuplicateWordError(WordsError):
    MSG = 'duplicate word in dictionary, type: %(type)s, normal form: %(normal_form)s'

class UnknownVerboseIdError(WordsError):
    MSG = 'Unknown verbose id: %(verbose_id)s'


class ExternalDependecyNotFoundError(WordsError):
    MSG = 'External dependency not found: %(dependency)s'


class WrongDependencyFormatError(WordsError):
    MSG = 'wrong dependency format: %(dependency)s'


class NoWordsFoundError(WordsError):
    MSG = 'no words found for text="%(text)s"'


class MoreThenOneWordFoundError(WordsError):
    MSG = 'more then one word found for text="%(text)s" and type=%(type)s'


class LexiconError(UtgError):
    pass

class UnknownLexiconKeyError(LexiconError):
    MSG = 'unknown lexicon key: %(key)s'

class NoTemplatesWithSpecifiedRestrictions(LexiconError):
    MSG = 'no templates with specified key: %(key)s and restrictions: %(restrictions)r'

class TransformatorsError(UtgError):
    pass

class UnknownIntegerFormError(TransformatorsError):
    MSG = 'unknown integer form: %(form)s'
