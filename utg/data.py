# coding: utf-8

from . import logic
from . import restrictions

VERBOSE_TO_PROPERTIES = logic.get_verbose_to_relations()


DEFAULT_PROPERTIES = logic.get_default_properties()


WORDS_CACHES, INVERTED_WORDS_CACHES = logic.get_caches(restrictions=restrictions.RESTRICTIONS,
                                                       restricted_key_parts=restrictions.RESTRICTED_KEY_PARTS)

RAW_WORDS_CACHES = logic.get_raw_caches(INVERTED_WORDS_CACHES)


CONSONANTS = set(u'бвгджзйклмнпрстфхцчшщъьБВГДЖЗЙКЛМНПРСТФХЦЧШЩЪЬ')
VOWELS = set(u'аеёиоуыэюяАЕЁИОУЫЭЮЯ')
J_VOWELS = set(u'еёюяЕЁЮЯ')
NOT_J_VOWELS = VOWELS - J_VOWELS
