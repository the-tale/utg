# coding: utf-8
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
        TESTS = {(r.INTEGER_FORM.SINGULAR,): (r.INTEGER_FORM.SINGULAR, r.NUMBER.SINGULAR),

                 (r.INTEGER_FORM.DUAL, r.CASE.NOMINATIVE): (r.INTEGER_FORM.DUAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE),
                 (r.INTEGER_FORM.DUAL, r.CASE.DATIVE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.DATIVE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE): (r.INTEGER_FORM.DUAL, r.NUMBER.PLURAL, r.CASE.ACCUSATIVE, r.ANIMALITY.ANIMATE),
                 (r.INTEGER_FORM.DUAL, r.CASE.ACCUSATIVE, r.ANIMALITY.INANIMATE): (r.INTEGER_FORM.DUAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE, r.ANIMALITY.INANIMATE),

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
            # print '---'
            # print test
            # print result
            # print transformators._noun_integer(words.Properties(*test))._data.values()
            self.assertEqual(transformators._noun_integer(words.Properties(*test)),
                             words.Properties(*result))

    def test_noun_integer__unknown_integer_form(self):
        self.assertRaises(exceptions.UnknownIntegerFormError,
                          transformators._noun_integer,
                          words.Properties(mock.Mock(_relation=r.INTEGER_FORM,
                                                     **{'is_%s' % form.name: False for form in r.INTEGER_FORM.records})))
