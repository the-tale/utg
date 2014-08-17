# coding: utf-8


from unittest import TestCase

from utg import relations as r
from utg import logic


class GeneralTests(TestCase):

    def setUp(self):
        super(GeneralTests, self).setUp()


    def test__properties_list(self):
        self.assertEqual(set(logic.get_property_relations()),
                         set([ r.CASE,
                               r.ANIMALITY,
                               r.NUMBER,
                               r.GENDER,
                               r.FORM,
                               r.TIME,
                               r.PERSON,
                               r.ASPECT,
                               r.MOOD,
                               r.ADJECTIVE_CATEGORY,
                               r.GRADE,
                               r.PRONOUN_CATEGORY,
                               r.WORD_CASE,
                               r.WORD_TYPE]))

    def test_scheme_orders(self):
        expected_order = [ r.FORM,
                           r.ADJECTIVE_CATEGORY,
                           r.PRONOUN_CATEGORY,

                           r.TIME,
                           r.ASPECT,
                           r.NUMBER,
                           r.CASE,
                           r.PERSON,
                           r.GENDER,

                           r.ANIMALITY,
                           r.GRADE,
                           r.MOOD,

                           r.WORD_CASE,

                           r.WORD_TYPE]

        self.assertEqual(set(logic.get_property_relations()), set(expected_order))

        for word_type in r.WORD_TYPE.records:
            self.assertEqual(word_type.schema,
                             tuple(sorted(word_type.schema,
                                        cmp=lambda a, b: cmp(expected_order.index(a), expected_order.index(b)))))

    def test_unique_verbose_ids(self):
        properties = set()

        for properties_relation in logic.get_property_relations():
            for property in properties_relation.records:
                self.assertFalse(property.verbose_id in properties)
                properties.add(property.verbose_id)
