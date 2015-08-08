# coding: utf-8

from utg import relations as r

# large restriction groups
RESTRICTIONS = {
    r.WORD_TYPE.NOUN: { r.NUMBER.PLURAL: (r.GENDER,) },
    r.WORD_TYPE.ADJECTIVE:{ r.NUMBER.PLURAL: (r.GENDER,),
                            r.ADJECTIVE_CATEGORY.RELATIVE: (r.GRADE,),
                            r.ADJECTIVE_CATEGORY.POSSESSIVE: (r.GRADE,),
                            r.ADJECTIVE_FORM.SHORT: (r.CASE, r.ANIMALITY, r.GRADE),
                            r.GRADE.COMPARATIVE: (r.NUMBER, r.CASE, r.GENDER, r.ANIMALITY) },
    r.WORD_TYPE.PRONOUN:{ r.NUMBER.PLURAL: (r.GENDER,) },
    r.WORD_TYPE.VERB:{ r.VERB_FORM.INFINITIVE: (r.TIME, r.PERSON, r.NUMBER, r.GENDER),
                       # r.VERB_FORM.CONDITIONAL: (r.TIME, r.PERSON,),
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

# additional restrictions
RESTRICTED_KEY_PARTS = {
    r.WORD_TYPE.NOUN: ( frozenset((r.NOUN_FORM.COUNTABLE, r.NUMBER.SINGULAR)), ),
    r.WORD_TYPE.VERB: ( frozenset((r.VERB_FORM.IMPERATIVE, r.PERSON.THIRD)),
                        frozenset((r.VERB_FORM.IMPERATIVE, r.PERSON.FIRST, r.NUMBER.SINGULAR)) )
    }


PRESETS = {r.NOUN_FORM.COUNTABLE: r.NUMBER.PLURAL}
