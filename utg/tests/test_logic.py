# coding: utf-8

from unittest import TestCase

import mock

from utg import relations as r
from utg import logic


class LogicTests(TestCase):

    def setUp(self):
        super(LogicTests, self).setUp()


    def test_get_default_properties(self):
        properties = set([r.CASE.NOMINATIVE,
                          r.GENDER.MASCULINE,
                          r.VERB_FORM.INFINITIVE,
                          r.ADJECTIVE_FORM.FULL,
                          r.PARTICIPLE_FORM.FULL,
                          r.TIME.PAST,
                          r.VOICE.DIRECT,
                          r.PRONOUN_CATEGORY.PERSONAL,
                          r.WORD_CASE.LOWER,
                          r.DEPENDENCY_MODE.FULL,
                          r.ANIMALITY.ANIMATE,
                          r.PERSON.FIRST,
                          r.GRADE.POSITIVE,
                          r.ADJECTIVE_CATEGORY.QUALITY,
                          r.NUMBER.SINGULAR,
                          r.ASPECT.IMPERFECTIVE,
                          r.INTEGER_FORM.SINGULAR,
                          r.PREPOSITION_FORM.NORMAL,
                          r.NOUN_FORM.NORMAL,
                          None])

        self.assertEqual(set(logic.get_default_properties().values()),
                         properties)


    def test_keys_generation__no_restrictions(self):
        schema = (r.GENDER, r.VERB_FORM, r.CASE)
        restrictions = set()

        expected = []
        for gender in r.GENDER.records:
            for form in r.VERB_FORM.records:
                for case in r.CASE.records:
                    expected.append([gender, form, case])

        self.assertEqual(list(logic._keys_generator(left=[], right=schema, restrictions=restrictions)),
                         expected)


    def test_keys_generation__with_restrictions(self):
        schema = (r.GENDER, r.VERB_FORM, r.CASE)
        restrictions = {r.GENDER.MASCULINE: [r.VERB_FORM, r.CASE],
                        r.GENDER.FEMININE: [r.VERB_FORM],
                        r.VERB_FORM.INFINITIVE: [r.CASE]}

        expected = [ [r.GENDER.MASCULINE, None, None],

                     [r.GENDER.NEUTER, r.VERB_FORM.INFINITIVE, None],

                     [r.GENDER.NEUTER, r.VERB_FORM.INDICATIVE, r.CASE.NOMINATIVE],
                     [r.GENDER.NEUTER, r.VERB_FORM.INDICATIVE, r.CASE.GENITIVE],
                     [r.GENDER.NEUTER, r.VERB_FORM.INDICATIVE, r.CASE.DATIVE],
                     [r.GENDER.NEUTER, r.VERB_FORM.INDICATIVE, r.CASE.ACCUSATIVE],
                     [r.GENDER.NEUTER, r.VERB_FORM.INDICATIVE, r.CASE.INSTRUMENTAL],
                     [r.GENDER.NEUTER, r.VERB_FORM.INDICATIVE, r.CASE.PREPOSITIONAL],

                     [r.GENDER.NEUTER, r.VERB_FORM.IMPERATIVE, r.CASE.NOMINATIVE],
                     [r.GENDER.NEUTER, r.VERB_FORM.IMPERATIVE, r.CASE.GENITIVE],
                     [r.GENDER.NEUTER, r.VERB_FORM.IMPERATIVE, r.CASE.DATIVE],
                     [r.GENDER.NEUTER, r.VERB_FORM.IMPERATIVE, r.CASE.ACCUSATIVE],
                     [r.GENDER.NEUTER, r.VERB_FORM.IMPERATIVE, r.CASE.INSTRUMENTAL],
                     [r.GENDER.NEUTER, r.VERB_FORM.IMPERATIVE, r.CASE.PREPOSITIONAL],

                     [r.GENDER.FEMININE, None, r.CASE.NOMINATIVE],
                     [r.GENDER.FEMININE, None, r.CASE.GENITIVE],
                     [r.GENDER.FEMININE, None, r.CASE.DATIVE],
                     [r.GENDER.FEMININE, None, r.CASE.ACCUSATIVE],
                     [r.GENDER.FEMININE, None, r.CASE.INSTRUMENTAL],
                     [r.GENDER.FEMININE, None, r.CASE.PREPOSITIONAL] ]

        self.assertEqual(list(logic._keys_generator(left=[], right=schema, restrictions=restrictions)),
                         expected)

    def test_get_caches__for_every_word(self):
        caches, inverted_caches = logic.get_caches(restrictions={word_type: {} for word_type in r.WORD_TYPE.records}, restricted_key_parts={})
        self.assertEqual(set(caches.keys()),  set(r.WORD_TYPE.records))
        self.assertEqual(set(inverted_caches.keys()), set(r.WORD_TYPE.records))

    def test_get_caches(self):
        cache, inverted_cache = logic._get_cache(schema=(r.NUMBER, r.CASE), restrictions={}, restricted_key_parts=())

        self.assertEqual(len(cache), 12)

        self.assertEqual(cache,
                         { (r.NUMBER.SINGULAR, r.CASE.NOMINATIVE): 0,
                           (r.NUMBER.SINGULAR, r.CASE.GENITIVE): 1,
                           (r.NUMBER.SINGULAR, r.CASE.DATIVE): 2,
                           (r.NUMBER.SINGULAR, r.CASE.ACCUSATIVE): 3,
                           (r.NUMBER.SINGULAR, r.CASE.INSTRUMENTAL): 4,
                           (r.NUMBER.SINGULAR, r.CASE.PREPOSITIONAL): 5,
                           (r.NUMBER.PLURAL, r.CASE.NOMINATIVE): 6,
                           (r.NUMBER.PLURAL, r.CASE.GENITIVE): 7,
                           (r.NUMBER.PLURAL, r.CASE.DATIVE): 8,
                           (r.NUMBER.PLURAL, r.CASE.ACCUSATIVE): 9,
                           (r.NUMBER.PLURAL, r.CASE.INSTRUMENTAL): 10,
                           (r.NUMBER.PLURAL, r.CASE.PREPOSITIONAL): 11})
        self.assertEqual(inverted_cache,
                         [ (r.NUMBER.SINGULAR, r.CASE.NOMINATIVE),
                           (r.NUMBER.SINGULAR, r.CASE.GENITIVE),
                           (r.NUMBER.SINGULAR, r.CASE.DATIVE),
                           (r.NUMBER.SINGULAR, r.CASE.ACCUSATIVE),
                           (r.NUMBER.SINGULAR, r.CASE.INSTRUMENTAL),
                           (r.NUMBER.SINGULAR, r.CASE.PREPOSITIONAL),
                           (r.NUMBER.PLURAL, r.CASE.NOMINATIVE),
                           (r.NUMBER.PLURAL, r.CASE.GENITIVE),
                           (r.NUMBER.PLURAL, r.CASE.DATIVE),
                           (r.NUMBER.PLURAL, r.CASE.ACCUSATIVE),
                           (r.NUMBER.PLURAL, r.CASE.INSTRUMENTAL),
                           (r.NUMBER.PLURAL, r.CASE.PREPOSITIONAL) ] )

    def test_get_caches__restricted_parts(self):
        cache, inverted_cache = logic._get_cache(schema=(r.NUMBER, r.CASE),
                                                 restrictions={},
                                                 restricted_key_parts=(frozenset((r.NUMBER.SINGULAR, r.CASE.DATIVE)), frozenset((r.NUMBER.PLURAL, r.CASE.ACCUSATIVE))))

        self.assertEqual(len(cache), 10)

        self.assertEqual(cache,
                         { (r.NUMBER.SINGULAR, r.CASE.NOMINATIVE): 0,
                           (r.NUMBER.SINGULAR, r.CASE.GENITIVE): 1,
                           (r.NUMBER.SINGULAR, r.CASE.ACCUSATIVE): 2,
                           (r.NUMBER.SINGULAR, r.CASE.INSTRUMENTAL): 3,
                           (r.NUMBER.SINGULAR, r.CASE.PREPOSITIONAL): 4,
                           (r.NUMBER.PLURAL, r.CASE.NOMINATIVE): 5,
                           (r.NUMBER.PLURAL, r.CASE.GENITIVE): 6,
                           (r.NUMBER.PLURAL, r.CASE.DATIVE): 7,
                           (r.NUMBER.PLURAL, r.CASE.INSTRUMENTAL): 8,
                           (r.NUMBER.PLURAL, r.CASE.PREPOSITIONAL): 9})
        self.assertEqual(inverted_cache,
                         [ (r.NUMBER.SINGULAR, r.CASE.NOMINATIVE),
                           (r.NUMBER.SINGULAR, r.CASE.GENITIVE),
                           (r.NUMBER.SINGULAR, r.CASE.ACCUSATIVE),
                           (r.NUMBER.SINGULAR, r.CASE.INSTRUMENTAL),
                           (r.NUMBER.SINGULAR, r.CASE.PREPOSITIONAL),
                           (r.NUMBER.PLURAL, r.CASE.NOMINATIVE),
                           (r.NUMBER.PLURAL, r.CASE.GENITIVE),
                           (r.NUMBER.PLURAL, r.CASE.DATIVE),
                           (r.NUMBER.PLURAL, r.CASE.INSTRUMENTAL),
                           (r.NUMBER.PLURAL, r.CASE.PREPOSITIONAL) ] )

    def test_get_caches__with_restrictions(self):
        cache, inverted_cache = logic._get_cache(schema=(r.NUMBER, r.CASE), restrictions={r.NUMBER.PLURAL: [r.CASE]}, restricted_key_parts=())

        self.assertEqual(len(cache), 7)
        self.assertEqual(cache,
                         { (r.NUMBER.SINGULAR, r.CASE.NOMINATIVE): 0,
                           (r.NUMBER.SINGULAR, r.CASE.GENITIVE): 1,
                           (r.NUMBER.SINGULAR, r.CASE.DATIVE): 2,
                           (r.NUMBER.SINGULAR, r.CASE.ACCUSATIVE): 3,
                           (r.NUMBER.SINGULAR, r.CASE.INSTRUMENTAL): 4,
                           (r.NUMBER.SINGULAR, r.CASE.PREPOSITIONAL): 5,
                           (r.NUMBER.PLURAL, None): 6})
        self.assertEqual(inverted_cache,
                         [ (r.NUMBER.SINGULAR, r.CASE.NOMINATIVE),
                           (r.NUMBER.SINGULAR, r.CASE.GENITIVE),
                           (r.NUMBER.SINGULAR, r.CASE.DATIVE),
                           (r.NUMBER.SINGULAR, r.CASE.ACCUSATIVE),
                           (r.NUMBER.SINGULAR, r.CASE.INSTRUMENTAL),
                           (r.NUMBER.SINGULAR, r.CASE.PREPOSITIONAL),
                           (r.NUMBER.PLURAL, None) ] )


    def test_get_nearest_key(self):
        available_keys = [(None, None, None),
                          (r.CASE.DATIVE, r.GENDER.MASCULINE, r.NUMBER.SINGULAR),
                          (r.CASE.DATIVE, None, r.NUMBER.PLURAL),
                          (None, r.GENDER.MASCULINE, None),]

        expected = {(None, r.GENDER.FEMININE, None): (None, None, None),
                    (None, r.GENDER.MASCULINE, r.NUMBER.PLURAL): (None, r.GENDER.MASCULINE, None),
                    (r.CASE.DATIVE, r.GENDER.FEMININE, r.NUMBER.SINGULAR): (r.CASE.DATIVE, r.GENDER.MASCULINE, r.NUMBER.SINGULAR)}

        for key, expected_key in expected.iteritems():
            self.assertEqual(logic.get_nearest_key(key, available_keys), expected_key)
