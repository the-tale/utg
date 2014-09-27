# coding: utf-8

from utg import logic
from utg import relations as r

VERBOSE_TO_PROPERTIES = logic.get_verbose_to_relations()

RESTRICTIONS = { r.FORM.INFINITIVE: (r.TIME, r.PERSON, r.NUMBER, r.MOOD, r.GENDER),
                 r.NUMBER.PLURAL: (r.GENDER,),
                 r.TIME.PAST: (r.PERSON, ),
                 r.TIME.PRESENT: (r.GENDER, r.MOOD),
                 r.TIME.FUTURE: (r.GENDER,),
                 r.ADJECTIVE_CATEGORY.RELATIVE: (r.GRADE,),
                 r.ADJECTIVE_CATEGORY.POSSESSIVE: (r.GRADE,),
                 r.PRONOUN_CATEGORY.REFLEXIVE: (r.NUMBER, r.GENDER, r.PERSON),
                 r.PRONOUN_CATEGORY.INTERROGATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.RELATIVE: (r.NUMBER, r.GENDER, r.PERSON),
                 r.PRONOUN_CATEGORY.DEMONSTRATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.ATTRIBUTIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.NEGATIVE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.VAGUE: (r.PERSON,),
                 r.PRONOUN_CATEGORY.MUTUAL: (r.PERSON,) }

INVERTED_RESTRICTIONS = {}
for property, property_groups in RESTRICTIONS.iteritems():
    for property_group in property_groups:
        if property_group not in INVERTED_RESTRICTIONS:
            INVERTED_RESTRICTIONS[property_group] = set()
        INVERTED_RESTRICTIONS[property_group].add(property)

DEFAULT_PROPERTIES = logic.get_default_properties()

WORDS_CACHES, INVERTED_WORDS_CACHES = logic.get_caches(restrictions=RESTRICTIONS)
