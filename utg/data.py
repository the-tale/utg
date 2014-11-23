# coding: utf-8

from utg import logic
from utg import relations as r

VERBOSE_TO_PROPERTIES = logic.get_verbose_to_relations()

RESTRICTIONS = { r.VERB_FORM.INFINITIVE: (r.TIME, r.PERSON, r.NUMBER, r.GENDER),
                 r.VERB_FORM.CONDITIONAL: (r.TIME, r.PERSON,),
                 r.VERB_FORM.IMPERATIVE: (r.TIME, r.GENDER,),
                 r.NUMBER.PLURAL: (r.GENDER,),
                 r.TIME.PAST: (r.PERSON, ),
                 r.TIME.PRESENT: (r.GENDER,),
                 r.TIME.FUTURE: (r.GENDER,),
                 r.ADJECTIVE_CATEGORY.RELATIVE: (r.GRADE,),
                 r.ADJECTIVE_CATEGORY.POSSESSIVE: (r.GRADE,),
                 r.ADJECTIVE_FORM.SHORT: (r.CASE, r.ANIMALITY, r.GRADE),
                 r.PARTICIPLE_FORM.SHORT: (r.TIME, r.VOICE, r.CASE, r.ANIMALITY),
                 r.NOUN_FORM.COUNTABLE: (r.NUMBER,),
                 r.PRONOUN_CATEGORY.REFLEXIVE: (r.NUMBER, r.GENDER, r.PERSON),
                 r.PRONOUN_CATEGORY.INTERROGATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.RELATIVE: (r.NUMBER, r.GENDER, r.PERSON),
                 r.PRONOUN_CATEGORY.DEMONSTRATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.ATTRIBUTIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.NEGATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.VAGUE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.MUTUAL: (r.PERSON,), }

INVERTED_RESTRICTIONS = {}
for property, property_groups in RESTRICTIONS.iteritems():
    for property_group in property_groups:
        if property_group not in INVERTED_RESTRICTIONS:
            INVERTED_RESTRICTIONS[property_group] = set()
        INVERTED_RESTRICTIONS[property_group].add(property)
INVERTED_RESTRICTIONS = {k: frozenset(v) for k, v in INVERTED_RESTRICTIONS.items()}

PRESETS = {r.NOUN_FORM.COUNTABLE: r.NUMBER.PLURAL}

DEFAULT_PROPERTIES = logic.get_default_properties()


WORDS_CACHES, INVERTED_WORDS_CACHES = logic.get_caches(restrictions=RESTRICTIONS)

RAW_WORDS_CACHES = logic.get_raw_caches(INVERTED_WORDS_CACHES)


CONSONANTS = set(u'бвгджзйклмнпрстфхцчшщъьБВГДЖЗЙКЛМНПРСТФХЦЧШЩЪЬ')
VOWELS = set(u'аеёиоуыэюяАЕЁИОУЫЭЮЯ')
