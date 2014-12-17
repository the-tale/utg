# coding: utf-8

from utg import logic
from utg.restrictions import RESTRICTIONS, PRESETS

VERBOSE_TO_PROPERTIES = logic.get_verbose_to_relations()


DEFAULT_PROPERTIES = logic.get_default_properties()


WORDS_CACHES, INVERTED_WORDS_CACHES = logic.get_caches(restrictions=RESTRICTIONS)

RAW_WORDS_CACHES = logic.get_raw_caches(INVERTED_WORDS_CACHES)


CONSONANTS = set(u'бвгджзйклмнпрстфхцчшщъьБВГДЖЗЙКЛМНПРСТФХЦЧШЩЪЬ')
VOWELS = set(u'аеёиоуыэюяАЕЁИОУЫЭЮЯ')
J_VOWELS = set(u'еёюяЕЁЮЯ')
NOT_J_VOWELS = VOWELS - J_VOWELS
