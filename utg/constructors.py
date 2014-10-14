# coding: utf-8

from utg import words
from utg import relations as r


from rels import EnumWithText, Column

class INTEGER_PROPERTIES(EnumWithText):
    properties = Column(unique=False, no_index=True)

    records = ( ('IS_KKK', 0, u'1kk или 1kkk', words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.MIL_BIL)),
                ('IS_1', 1, u'1', words.Properties(r.NUMBER.SINGULAR, r.INTEGER_FORM.SINGULAR)),
                ('IS_234', 2, u'2, 3 или 4', words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.DUAL)),
                ('IS_10_19', 3, u'от 10 до 19', words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.PLURAL)),
                ('IS_END_BY_1', 4, u'оканчивается на 1', words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.SINGULAR)),
                ('IS_MOD_234', 5, u'оканчивается на 2, 3 или 4', words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.COMPOSITE_DUAL)),
                ('IS_OTHER', 6, u'остальное', words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.PLURAL)) )


def _construct_integer(number):
    form = unicode(number)
    number = abs(number)

    if number in (1000000, 1000000000):
        properties = INTEGER_PROPERTIES.IS_KKK.properties
    elif number == 1:
        properties = INTEGER_PROPERTIES.IS_1.properties
    elif number in (2, 3, 4):
        properties = INTEGER_PROPERTIES.IS_234.properties
    elif 10 <= number % 100 <= 19:
        properties = INTEGER_PROPERTIES.IS_10_19.properties
    elif number % 10 == 1:
        properties = INTEGER_PROPERTIES.IS_END_BY_1.properties
    elif 2 <= number % 10 <= 4:
        properties = INTEGER_PROPERTIES.IS_MOD_234.properties
    else:
        properties = INTEGER_PROPERTIES.IS_OTHER.properties

    return words.WordForm(words.Word(type=r.WORD_TYPE.INTEGER, forms=[form], properties=properties))


_INTEGER_CACHE_LEFT = 0
_INTEGER_CACHE_RIGHT = 10000
_INTEGER_CACHE = tuple(_construct_integer(i+_INTEGER_CACHE_LEFT) for i in xrange(_INTEGER_CACHE_RIGHT-_INTEGER_CACHE_LEFT+1))

def construct_integer(number):
    if _INTEGER_CACHE_LEFT <= number <= _INTEGER_CACHE_RIGHT:
        return _INTEGER_CACHE[number]

    return _construct_integer(number)
