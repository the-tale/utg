# coding: utf-8

from utg import relations as r

RESTRICTIONS = {
    r.WORD_TYPE.NOUN: { r.NUMBER.PLURAL: (r.GENDER,),
                        r.NOUN_FORM.COUNTABLE: (r.NUMBER,) },
    r.WORD_TYPE.ADJECTIVE:{ r.NUMBER.PLURAL: (r.GENDER,),
                            r.ADJECTIVE_CATEGORY.RELATIVE: (r.GRADE,),
                            r.ADJECTIVE_CATEGORY.POSSESSIVE: (r.GRADE,),
                            r.ADJECTIVE_FORM.SHORT: (r.CASE, r.ANIMALITY, r.GRADE) },
    r.WORD_TYPE.PRONOUN:{ r.NUMBER.PLURAL: (r.GENDER,),
                          r.PRONOUN_CATEGORY.REFLEXIVE: (r.NUMBER, r.GENDER, r.PERSON),
                          r.PRONOUN_CATEGORY.INTERROGATIVE: (r.PERSON,),
                          r.PRONOUN_CATEGORY.RELATIVE: (r.NUMBER, r.GENDER, r.PERSON),
                          r.PRONOUN_CATEGORY.DEMONSTRATIVE: (r.PERSON,),
                          r.PRONOUN_CATEGORY.ATTRIBUTIVE: (r.PERSON,),
                          r.PRONOUN_CATEGORY.NEGATIVE: (r.PERSON,),
                          r.PRONOUN_CATEGORY.VAGUE: (r.PERSON,),
                          r.PRONOUN_CATEGORY.MUTUAL: (r.PERSON,), },
    r.WORD_TYPE.VERB:{ r.VERB_FORM.INFINITIVE: (r.TIME, r.PERSON, r.NUMBER, r.GENDER),
                       r.VERB_FORM.CONDITIONAL: (r.TIME, r.PERSON,),
                       r.VERB_FORM.IMPERATIVE: (r.TIME, r.GENDER,),
                       r.NUMBER.PLURAL: (r.GENDER,),
                       r.TIME.PAST: (r.PERSON, ),
                       r.TIME.PRESENT: (r.GENDER,),
                       r.TIME.FUTURE: (r.GENDER,) },
    r.WORD_TYPE.PARTICIPLE:{ r.NUMBER.PLURAL: (r.GENDER,),
                             r.PARTICIPLE_FORM.SHORT: (r.TIME, r.VOICE, r.CASE, r.ANIMALITY) },
    r.WORD_TYPE.INTEGER:{},
    r.WORD_TYPE.TEXT:{},
    r.WORD_TYPE.PREPOSITION:{}}


INVERTED_RESTRICTIONS = {}
for word_type, word_type_restrictions in RESTRICTIONS.iteritems():
    inverted_restrictions = {}
    for property, property_groups in word_type_restrictions.iteritems():
        for property_group in property_groups:
            if property_group not in inverted_restrictions:
                inverted_restrictions[property_group] = set()
            inverted_restrictions[property_group].add(property)
    INVERTED_RESTRICTIONS[word_type] = {k: frozenset(v) for k, v in INVERTED_RESTRICTIONS.items()}

PRESETS = {r.NOUN_FORM.COUNTABLE: r.NUMBER.PLURAL}
