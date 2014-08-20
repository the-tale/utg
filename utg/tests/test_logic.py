# coding: utf-8


from unittest import TestCase

from utg import relations as r
from utg import logic


class LogicTests(TestCase):

    def setUp(self):
        super(LogicTests, self).setUp()


    def test_get_default_properties(self):
        properties = set([r.CASE.NOMINATIVE,
                          r.GENDER.MASCULINE,
                          r.FORM.INFINITIVE,
                          r.TIME.PAST,
                          r.PRONOUN_CATEGORY.PERSONAL,
                          r.WORD_CASE.LOWER,
                          r.ANIMALITY.ANIMATE,
                          r.PERSON.FIRST,
                          r.GRADE.POSITIVE,
                          r.ADJECTIVE_CATEGORY.QUALITY,
                          r.NUMBER.SINGULAR,
                          r.ASPECT.IMPERFECTIVE,
                          r.MOOD.INDICATIVE,
                          None])

        self.assertEqual(set(logic.get_default_properties().values()),
                         properties)


    def test_keys_generation__no_restrictions(self):
        schema = (r.GENDER, r.FORM, r.CASE)
        restrictions = set()

        expected = []
        for gender in r.GENDER.records:
            for form in r.FORM.records:
                for case in r.CASE.records:
                    expected.append([gender, form, case])

        self.assertEqual(list(logic._keys_generator(left=[], right=schema, restrictions=restrictions)),
                         expected)


    def test_keys_generation__with_restrictions(self):
        schema = (r.GENDER, r.FORM, r.CASE)
        restrictions = {r.GENDER.MASCULINE: [r.FORM, r.CASE],
                        r.GENDER.FEMININE: [r.FORM],
                        r.FORM.INFINITIVE: [r.CASE]}

        expected = [ [r.GENDER.MASCULINE, None, None],
                     [r.GENDER.NEUTER, r.FORM.INFINITIVE, None],
                     [r.GENDER.NEUTER, r.FORM.NORMAL, r.CASE.NOMINATIVE],
                     [r.GENDER.NEUTER, r.FORM.NORMAL, r.CASE.GENITIVE],
                     [r.GENDER.NEUTER, r.FORM.NORMAL, r.CASE.DATIVE],
                     [r.GENDER.NEUTER, r.FORM.NORMAL, r.CASE.ACCUSATIVE],
                     [r.GENDER.NEUTER, r.FORM.NORMAL, r.CASE.INSTRUMENTAL],
                     [r.GENDER.NEUTER, r.FORM.NORMAL, r.CASE.PREPOSITIONAL],
                     [r.GENDER.FEMININE, None, r.CASE.NOMINATIVE],
                     [r.GENDER.FEMININE, None, r.CASE.GENITIVE],
                     [r.GENDER.FEMININE, None, r.CASE.DATIVE],
                     [r.GENDER.FEMININE, None, r.CASE.ACCUSATIVE],
                     [r.GENDER.FEMININE, None, r.CASE.INSTRUMENTAL],
                     [r.GENDER.FEMININE, None, r.CASE.PREPOSITIONAL] ]

        self.assertEqual(list(logic._keys_generator(left=[], right=schema, restrictions=restrictions)),
                         expected)

    def test__get_full_restrictions(self):
        restrictions = {r.FORM.NORMAL: (r.TIME, r.GENDER),
                        r.GENDER.MASCULINE: (r.TIME,)}

        self.assertEqual(logic._get_full_restrictions(restrictions),
                         set([ (r.FORM.NORMAL, r.TIME.PAST),
                               (r.FORM.NORMAL, r.TIME.PRESENT),
                               (r.FORM.NORMAL, r.TIME.FUTURE),
                               (r.FORM.NORMAL, r.GENDER.MASCULINE),
                               (r.FORM.NORMAL, r.GENDER.NEUTER),
                               (r.FORM.NORMAL, r.GENDER.FEMININE),

                               (r.GENDER.MASCULINE, r.TIME.PAST),
                               (r.GENDER.MASCULINE, r.TIME.PRESENT),
                               (r.GENDER.MASCULINE, r.TIME.FUTURE),

                               (r.TIME.PAST, r.GENDER.MASCULINE),
                               (r.TIME.PRESENT, r.GENDER.MASCULINE),
                               (r.TIME.FUTURE, r.GENDER.MASCULINE),

                               (r.TIME.PAST, r.FORM.NORMAL),
                               (r.TIME.PRESENT, r.FORM.NORMAL),
                               (r.TIME.FUTURE, r.FORM.NORMAL),
                               (r.GENDER.MASCULINE, r.FORM.NORMAL),
                               (r.GENDER.NEUTER, r.FORM.NORMAL),
                               (r.GENDER.FEMININE, r.FORM.NORMAL) ]))

    def test_get_caches__for_every_word(self):
        caches, inverted_caches = logic.get_caches(restrictions={})
        self.assertEqual(set(caches.keys()),  set(r.WORD_TYPE.records))
        self.assertEqual(set(inverted_caches.keys()), set(r.WORD_TYPE.records))

    def test_get_caches(self):
        caches, inverted_caches = logic.get_caches(restrictions={})

        cache = caches[r.WORD_TYPE.NOUN]
        inverted_cache = inverted_caches[r.WORD_TYPE.NOUN]

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

    def test_get_caches__with_restrictions(self):
        caches, inverted_caches = logic.get_caches(restrictions={r.NUMBER.PLURAL: [r.CASE]})

        cache = caches[r.WORD_TYPE.NOUN]
        inverted_cache = inverted_caches[r.WORD_TYPE.NOUN]

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
