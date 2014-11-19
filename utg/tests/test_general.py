# coding: utf-8


from unittest import TestCase

from utg import relations as r
from utg import logic
from utg import data


EXPECTED_ORDER = [ r.VERB_FORM,
                   r.ADJECTIVE_FORM,
                   r.PARTICIPLE_FORM,

                   r.ADJECTIVE_CATEGORY,
                   r.PRONOUN_CATEGORY,

                   r.TIME,
                   r.VOICE,
                   r.ASPECT,
                   r.NUMBER,
                   r.CASE,
                   r.PERSON,
                   r.GENDER,

                   r.ANIMALITY,
                   r.GRADE,
                   r.MOOD,

                   r.INTEGER_FORM,

                   r.WORD_CASE,

                   r.PREPOSITION_FORM,

                   r.WORD_TYPE]


class GeneralTests(TestCase):

    def setUp(self):
        super(GeneralTests, self).setUp()


    def test__properties_list(self):
        self.assertEqual(set(logic.get_property_relations()),
                         set(EXPECTED_ORDER))

    def test_scheme_orders(self):
        self.assertEqual(set(logic.get_property_relations()), set(EXPECTED_ORDER))

        for word_type in r.WORD_TYPE.records:
            self.assertEqual(word_type.schema,
                             tuple(sorted(word_type.schema,
                                        cmp=lambda a, b: cmp(EXPECTED_ORDER.index(a), EXPECTED_ORDER.index(b)))))


    def test_restrictions_orders(self):
        for key, restrictions in data.RESTRICTIONS.iteritems():
            for restriction in restrictions:
                self.assertTrue(EXPECTED_ORDER.index(key._relation) < EXPECTED_ORDER.index(restriction))


    def test_unique_verbose_ids(self):
        properties = set()

        for properties_relation in logic.get_property_relations():
            for property in properties_relation.records:
                self.assertFalse(property.verbose_id in properties)
                properties.add(property.verbose_id)

    def test_all_property_types_in_relation(self):
        for properties_relation in logic.get_property_relations():
            self.assertTrue(properties_relation in r.PROPERTY_TYPE.index_relation)
