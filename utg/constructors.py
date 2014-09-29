# coding: utf-8

from utg import words
from utg import relations as r


def construct_integer(number):
    form = u'%s' % number
    number = abs(number)

    if number in (1000000, 1000000000):
        properties = words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.MIL_BIL)
    elif number == 1:
        properties = words.Properties(r.NUMBER.SINGULAR, r.INTEGER_FORM.SINGULAR)
    elif number in (2, 3, 4):
        properties = words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.DUAL)
    elif 10 <= number % 100 <= 19:
        properties = words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.PLURAL)
    elif number % 10 == 1:
        properties = words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.SINGULAR)
    elif 2 <= number % 10 <= 4:
        properties = words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.COMPOSITE_DUAL)
    else:
        properties = words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.PLURAL)

    return words.Word(type=r.WORD_TYPE.INTEGER, forms=[form], properties=properties)
