# coding: utf-8

from utg import words
from utg import relations as r


class TestForms(object):
    NOUN = [u'ед1', u'ед2', u'ед3', u'ед4', u'ед5', u'ед6', u'мн1', u'мн2', u'мн3', u'мн4', u'мн5', u'мн6']


def create_noun(prefix=u'', properties=None):
    return words.Word(type=r.WORD_TYPE.NOUN,
                      forms=[prefix + form for form in TestForms.NOUN],
                      properties=properties if properties is not None else words.Properties())
