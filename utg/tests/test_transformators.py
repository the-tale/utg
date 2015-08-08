# coding: utf-8
import random

from unittest import TestCase

import mock

from utg import words
from utg import exceptions
from utg import transformators
from utg import relations as r


class TransformatorsTests(TestCase):

    def setUp(self):
        super(TransformatorsTests, self).setUp()


    def test_noun_integer(self):
        TESTS = {(r.INTEGER_FORM.SINGULAR,): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.SINGULAR, r.NUMBER.SINGULAR),

                 (r.INTEGER_FORM.DUAL, r.CASE.NOMINATIVE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.DUAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE),
                 (r.INTEGER_FORM.DUAL, r.CASE.DATIVE): (r.NOUN_FORM.COUNTABLE, r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.NOUN_FORM.COUNTABLE, r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.DUAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE, r.ANIMALITY.INANIMATE),

                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.NOMINATIVE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.DATIVE): (r.NOUN_FORM.COUNTABLE, r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE, r.ANIMALITY.INANIMATE),

                 (r.INTEGER_FORM.PLURAL, r.CASE.NOMINATIVE): (r.NOUN_FORM.COUNTABLE, r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.GENITIVE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.DATIVE): (r.NOUN_FORM.COUNTABLE, r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.NOUN_FORM.COUNTABLE, r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.NOUN_FORM.COUNTABLE, r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.ANIMALITY.INANIMATE),

                 (r.INTEGER_FORM.MIL_BIL, r.CASE.NOMINATIVE): (r.NOUN_FORM.COUNTABLE, r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.GENITIVE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.DATIVE): (r.NOUN_FORM.COUNTABLE, r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.GENITIVE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.NOUN_FORM.COUNTABLE, r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.NOUN_FORM.COUNTABLE, r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.ANIMALITY.INANIMATE)

                 }

        for test, result in TESTS.iteritems():
            self.assertEqual(transformators._noun_integer(words.Properties(*test)),
                             words.Properties(*result))


    def test_noun_integer__semantic_dependency(self):
        TESTS = {(r.INTEGER_FORM.SINGULAR,): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.SINGULAR, r.NUMBER.SINGULAR),

                 (r.INTEGER_FORM.DUAL, r.CASE.NOMINATIVE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE),
                 (r.INTEGER_FORM.DUAL, r.CASE.DATIVE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE),

                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.NOMINATIVE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.DATIVE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE),

                 (r.INTEGER_FORM.PLURAL, r.CASE.NOMINATIVE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.DATIVE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE),

                 (r.INTEGER_FORM.MIL_BIL, r.CASE.NOMINATIVE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.DATIVE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.NOUN_FORM.NORMAL, r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE)

                 }

        for test, result in TESTS.iteritems():
            self.assertEqual(transformators._noun_integer(words.Properties(r.DEPENDENCY_MODE.SEMANTIC, *test)),
                             words.Properties(r.DEPENDENCY_MODE.SEMANTIC, *result))


    def test_adjective_integer(self):
        TESTS = {(r.INTEGER_FORM.SINGULAR,): (r.INTEGER_FORM.SINGULAR, r.NUMBER.SINGULAR),

                 (r.INTEGER_FORM.DUAL, r.CASE.NOMINATIVE, r.GENDER.MASCULINE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.GENDER.MASCULINE),
                 (r.INTEGER_FORM.DUAL, r.CASE.DATIVE, r.GENDER.MASCULINE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE, r.GENDER.MASCULINE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.MASCULINE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.GENDER.MASCULINE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.MASCULINE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.GENDER.MASCULINE),

                 (r.INTEGER_FORM.DUAL, r.CASE.NOMINATIVE, r.GENDER.NEUTER): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.GENDER.NEUTER),
                 (r.INTEGER_FORM.DUAL, r.CASE.DATIVE, r.GENDER.NEUTER): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE, r.GENDER.NEUTER),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.NEUTER): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.GENDER.NEUTER),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.NEUTER): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.GENDER.NEUTER),

                 (r.INTEGER_FORM.DUAL, r.CASE.NOMINATIVE, r.GENDER.FEMININE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE, r.GENDER.FEMININE),
                 (r.INTEGER_FORM.DUAL, r.CASE.DATIVE, r.GENDER.FEMININE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE, r.GENDER.FEMININE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.FEMININE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE, r.GENDER.FEMININE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.FEMININE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE, r.GENDER.FEMININE),

                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.NOMINATIVE): (r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.DATIVE): (r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE, r.ANIMALITY.INANIMATE),

                 (r.INTEGER_FORM.PLURAL, r.CASE.NOMINATIVE): (r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.GENITIVE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.DATIVE): (r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.ANIMALITY.INANIMATE),

                 (r.INTEGER_FORM.MIL_BIL, r.CASE.NOMINATIVE): (r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.GENITIVE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.DATIVE): (r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.GENITIVE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.GENITIVE, r.ANIMALITY.INANIMATE)
                }

        for test, result in TESTS.iteritems():
            self.assertEqual(transformators._adjective_integer(words.Properties(*test)),
                             words.Properties(*result))

    def test_adjective_integer__semantic_dependency(self):
        TESTS = {(r.INTEGER_FORM.SINGULAR,): (r.INTEGER_FORM.SINGULAR, r.NUMBER.SINGULAR),

                 (r.INTEGER_FORM.DUAL, r.CASE.NOMINATIVE, r.GENDER.MASCULINE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE, r.GENDER.MASCULINE),
                 (r.INTEGER_FORM.DUAL, r.CASE.DATIVE, r.GENDER.MASCULINE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE, r.GENDER.MASCULINE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.MASCULINE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.GENDER.MASCULINE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.MASCULINE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.GENDER.MASCULINE),

                 (r.INTEGER_FORM.DUAL, r.CASE.NOMINATIVE, r.GENDER.NEUTER): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE, r.GENDER.NEUTER),
                 (r.INTEGER_FORM.DUAL, r.CASE.DATIVE, r.GENDER.NEUTER): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE, r.GENDER.NEUTER),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.NEUTER): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.GENDER.NEUTER),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.NEUTER): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.GENDER.NEUTER),

                 (r.INTEGER_FORM.DUAL, r.CASE.NOMINATIVE, r.GENDER.FEMININE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE, r.GENDER.FEMININE),
                 (r.INTEGER_FORM.DUAL, r.CASE.DATIVE, r.GENDER.FEMININE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE, r.GENDER.FEMININE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.FEMININE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.GENDER.FEMININE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.GENDER.FEMININE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.GENDER.FEMININE),

                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.NOMINATIVE): (r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.DATIVE): (r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.COMPOSITE_DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.INTEGER_FORM.COMPOSITE_DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE),

                 (r.INTEGER_FORM.PLURAL, r.CASE.NOMINATIVE): (r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.DATIVE): (r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.INTEGER_FORM.PLURAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE),

                 (r.INTEGER_FORM.MIL_BIL, r.CASE.NOMINATIVE): (r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.NOMINATIVE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.DATIVE): (r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.MIL_BIL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.INTEGER_FORM.MIL_BIL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE)
                }

        for test, result in TESTS.iteritems():
            self.assertEqual(transformators._adjective_integer(words.Properties(r.DEPENDENCY_MODE.SEMANTIC, *test)),
                             words.Properties(r.DEPENDENCY_MODE.SEMANTIC, *result))

    def test_noun_integer__unknown_integer_form(self):
        self.assertRaises(exceptions.UnknownIntegerFormError,
                          transformators._noun_integer,
                          words.Properties(mock.Mock(_relation=r.INTEGER_FORM,
                                                     **{'is_%s' % form.name: False for form in r.INTEGER_FORM.records})))


    def _create_preposition(self, forms):
        return words.Word(r.WORD_TYPE.PREPOSITION,
                          forms=forms,
                          properties=words.Properties())

    def test_preposition_consonants(self):
        pre_1 = self._create_preposition([u'под', u'подо', u'подо'])
        pre_2 = self._create_preposition([u'за', u'за', u'за'])
        pre_3 = self._create_preposition([u'в', u'во', u'во'])
        pre_4 = self._create_preposition([u'с', u'со', u'со'])

        master_word_1 = words.Word(type=r.WORD_TYPE.NOUN,
                                   forms=[u'сон', u'сна', u'сну', u'сон', u'сном', u'сне',
                                          u'сны', u'снов', u'снам', u'сны', u'снами', u'снах',
                                          u'сны', u'снов', u'снам', u'сны', u'снами', u'снах'],
                                   properties=words.Properties(r.GENDER.MASCULINE, r.ANIMALITY.INANIMATE))

        master_word_2 = words.Word(type=r.WORD_TYPE.NOUN,
                                   forms=[u'сновидение', u'сновидения', u'сновидению', u'сновидение', u'сновидением', u'сновидении',
                                          u'сновидения', u'сновидений', u'сновидениям', u'сновидения', u'сновидениями', u'сновидениях',
                                          u'сновидения', u'сновидений', u'сновидениям', u'сновидения', u'сновидениями', u'сновидениях'],
                                   properties=words.Properties(r.GENDER.NEUTER, r.ANIMALITY.INANIMATE))

        master_word_3 = words.Word(type=r.WORD_TYPE.NOUN,
                                   forms=[u'власть', u'власти', u'власти', u'власть', u'властью', u'власти',
                                          u'', u'', u'', u'', u'', u'',
                                          u'', u'', u'', u'', u'', u''],
                                   properties=words.Properties(r.GENDER.MASCULINE, r.ANIMALITY.INANIMATE, r.NUMBER.SINGULAR))

        slave_properties = words.Properties(random.choice(r.PREPOSITION_FORM.records))

        master_form_1 = words.WordForm(word=master_word_1, properties=words.Properties(r.CASE.NOMINATIVE)) # сон
        master_form_2 = words.WordForm(word=master_word_1, properties=words.Properties(r.CASE.DATIVE)) # сну
        master_form_3 = words.WordForm(word=master_word_2) # сновидение
        master_form_4 = words.WordForm(word=master_word_3) # власть

        tests = {(pre_1, master_form_1): slave_properties, # под сон
                 (pre_1, master_form_2): words.Properties(r.PREPOSITION_FORM.ALTERNATIVE), # подо сну
                 (pre_1, master_form_3): slave_properties, # под сновидение
                 (pre_1, master_form_4): slave_properties, # под власть

                 (pre_2, master_form_1): slave_properties, # за сон
                 (pre_2, master_form_2): slave_properties, # за сну
                 (pre_2, master_form_3): slave_properties, # за сновидение
                 (pre_2, master_form_4): slave_properties, # за власть

                 (pre_3, master_form_1): slave_properties, # в сон
                 (pre_3, master_form_2): words.Properties(r.PREPOSITION_FORM.ALTERNATIVE), # во сну
                 (pre_3, master_form_3): slave_properties, # в сновидение
                 (pre_3, master_form_4): words.Properties(r.PREPOSITION_FORM.ALTERNATIVE), # во власть

                 (pre_4, master_form_1): slave_properties, # с сон
                 (pre_4, master_form_2): words.Properties(r.PREPOSITION_FORM.ALTERNATIVE), # со сну
                 (pre_4, master_form_3): words.Properties(r.PREPOSITION_FORM.ALTERNATIVE), # со сновидение
                 (pre_4, master_form_4): slave_properties} # с власть

        for (pre, master_form), result_properties in tests.iteritems():
            self.assertEqual(transformators._preposition_any(properties=slave_properties, slave_word=pre, master_form=master_form),
                             result_properties)


    def test_preposition_vovels(self):
        pre_1 = self._create_preposition([u'о', u'об', u'обо'])
        pre_2 = self._create_preposition([u'у', u'у', u'у'])

        master_word_1 = words.Word(type=r.WORD_TYPE.NOUN,
                                   forms=[u'ужин', u'ужина', u'ужину', u'ужин', u'ужином', u'ужине',
                                          u'ужины', u'ужинов', u'ужинам', u'ужины', u'ужинами', u'ужинах',
                                          u'ужины', u'ужинов', u'ужинам', u'ужины', u'ужинами', u'ужинах'],
                                   properties=words.Properties(r.GENDER.MASCULINE, r.ANIMALITY.INANIMATE))

        master_word_2 = words.Word(type=r.WORD_TYPE.NOUN,
                                   forms=[u'юрист', u'юриста', u'юристу', u'юриста', u'юристом', u'юристе',
                                          u'юристы', u'юристов', u'юристам', u'юристов', u'юристами', u'юристах',
                                          u'юристы', u'юристов', u'юристам', u'юристов', u'юристами', u'юристах'],
                                   properties=words.Properties(r.GENDER.NEUTER, r.ANIMALITY.INANIMATE))

        master_word_3 = words.Word(type=r.WORD_TYPE.PRONOUN, forms=[ u'я', u'я', u'я', u'меня', u'меня', u'меня', u'мне', u'мне', u'мне', u'меня', u'меня', u'меня', u'мной', u'мной', u'мной', u'мне', u'мне', u'мне', u'мы', u'нас', u'нам', u'нас', u'нами', u'нас', u'я', u'я', u'я', u'меня', u'меня', u'меня', u'мне', u'мне', u'мне', u'меня', u'меня', u'меня', u'мной', u'мной', u'мной', u'мне', u'мне', u'мне', u'мы', u'нас', u'нам', u'нас', u'нами', u'нас'],
                                   properties=words.Properties(r.PRONOUN_CATEGORY.PERSONAL))

        slave_properties = words.Properties(random.choice(r.PREPOSITION_FORM.records))

        master_form_1 = words.WordForm(word=master_word_1, properties=words.Properties(r.CASE.NOMINATIVE)) # ужин
        master_form_2 = words.WordForm(word=master_word_1, properties=words.Properties(r.CASE.DATIVE)) # ужину
        master_form_3 = words.WordForm(word=master_word_2) # юрист
        master_form_4 = words.WordForm(word=master_word_3) # я
        master_form_5 = words.WordForm(word=master_word_3, properties=words.Properties(r.CASE.DATIVE)) # мне

        self.assertEqual(master_form_5.form, u'мне')

        tests = {(pre_1, master_form_1): words.Properties(r.PREPOSITION_FORM.ALTERNATIVE), # об ужин
                 (pre_1, master_form_2): words.Properties(r.PREPOSITION_FORM.ALTERNATIVE), # об ужину
                 (pre_1, master_form_3): slave_properties, # о юрист
                 (pre_1, master_form_4): slave_properties, # о я
                 (pre_1, master_form_5): words.Properties(r.PREPOSITION_FORM.SPECIAL), # обо мне

                 (pre_2, master_form_1): words.Properties(r.PREPOSITION_FORM.ALTERNATIVE), # у ужин
                 (pre_2, master_form_2): words.Properties(r.PREPOSITION_FORM.ALTERNATIVE), # у ужину
                 (pre_2, master_form_3): slave_properties, # у юрист
                 (pre_2, master_form_4): slave_properties, # у я
                 (pre_2, master_form_5): slave_properties, # у мне
                }

        for (pre, master_form), result_properties in tests.iteritems():
            self.assertEqual(transformators._preposition_any(properties=slave_properties, slave_word=pre, master_form=master_form),
                             result_properties)
