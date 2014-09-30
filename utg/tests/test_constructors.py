# coding: utf-8

from unittest import TestCase

from utg import words
from utg import constructors
from utg import relations as r


class ConstructTests(TestCase):

    def setUp(self):
        super(ConstructTests, self).setUp()

    def test_construct_integer(self):
        singular_properties = words.Properties(r.NUMBER.SINGULAR, r.INTEGER_FORM.SINGULAR)
        singular_plural_properties = words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.SINGULAR)
        dual_properties = words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.DUAL)
        composite_dual_properties = words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.COMPOSITE_DUAL)
        plural_properties = words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.PLURAL)
        mil_bil_properties = words.Properties(r.NUMBER.PLURAL, r.INTEGER_FORM.MIL_BIL)

        tests = {1: singular_properties,
                 2: dual_properties,
                 3: dual_properties,
                 4: dual_properties,
                 5: plural_properties,
                 10: plural_properties,
                 11: plural_properties,
                 12: plural_properties,
                 13: plural_properties,
                 14: plural_properties,
                 15: plural_properties,
                 24: composite_dual_properties,
                 25: plural_properties,

                 1001: singular_plural_properties,

                 1002: composite_dual_properties,
                 1003: composite_dual_properties,
                 1004: composite_dual_properties,
                 1005: plural_properties,
                 1010: plural_properties,
                 1011: plural_properties,
                 1012: plural_properties,
                 1013: plural_properties,
                 1014: plural_properties,
                 1015: plural_properties,
                 1024: composite_dual_properties,
                 1025: plural_properties,

                 1000000: mil_bil_properties,
                 1000000000: mil_bil_properties}

        for number, properties in tests.iteritems():
            word = words.Word(type=r.WORD_TYPE.INTEGER, forms=['%d' % number], properties=properties)
            self.assertEqual(constructors.construct_integer(number), word)
