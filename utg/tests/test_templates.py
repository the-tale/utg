# coding: utf-8

from unittest import TestCase

from utg import words
from utg import templates
from utg import exceptions
from utg import relations as r
from utg.dictionary import Dictionary
from utg.tests import helpers


class SubstitutionTests(TestCase):

    def setUp(self):
        super(SubstitutionTests, self).setUp()


    def test_init(self):
        substitution = templates.Substitution()
        self.assertEqual(substitution.id, None)
        self.assertEqual(substitution.dependencies, [])


    def test_parse__no_slugs(self):
        self.assertRaises(exceptions.WrongDependencyFormatError, templates.Substitution.parse, variable=u'', externals=[])
        self.assertRaises(exceptions.WrongDependencyFormatError, templates.Substitution.parse, variable=u'[]', externals=[])


    def test_parse__single_slug(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla]', externals=['bla-bla'])
        self.assertEqual(substitution.id, 'bla-bla')
        self.assertEqual(substitution.dependencies, [])

    def test_parse__default_properties(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|]', externals=['bla-bla'])
        self.assertEqual(substitution.id, 'bla-bla')
        self.assertEqual(substitution.dependencies, [words.Properties()])

    def test_parse__wrong_verbose_id(self):
        self.assertRaises(exceptions.UnknownVerboseIdError, templates.Substitution.parse, variable=u'[bla-bla|unknown|вы-вы]', externals=['bla-bla', u'вы-вы'])

    def test_parse(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|external_1|дт|external_2|вн,личн]', externals=['bla-bla', 'external_1', 'external_2'])
        self.assertEqual(substitution.id, 'bla-bla')
        self.assertEqual(substitution.dependencies, ['external_1',
                                                     words.Properties(r.CASE.DATIVE),
                                                     'external_2',
                                                     words.Properties(r.CASE.ACCUSATIVE, r.PRONOUN_CATEGORY.PERSONAL)])

    def test_parse__word_type(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|гл]', externals=[''])
        self.assertEqual(substitution.dependencies, [words.Properties(r.WORD_TYPE.VERB)])


    def test_merge_properties__no_dependencies(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla]', externals=[])
        self.assertEqual(substitution._merge_properties(externals={}), words.Properties())

    def test_merge_properties__external_not_in_externals(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|external]', externals=['external'])
        self.assertRaises(exceptions.ExternalDependecyNotFoundError, substitution._merge_properties, externals={})

    def test_merge_properties__properties(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|дт,сравн]', externals=[])
        self.assertEqual(substitution._merge_properties(externals={}), words.Properties(r.CASE.DATIVE, r.GRADE.COMPARATIVE))

    def test_merge_properties__externals(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|external]', externals=['external'])
        word = words.Word(type=r.WORD_TYPE.NOUN,
                          forms=helpers.TestForms.NOUN,
                          properties=words.Properties(r.CASE.DATIVE, r.GRADE.COMPARATIVE))
        self.assertEqual(substitution._merge_properties(externals={'external': word}), words.Properties(r.CASE.DATIVE, r.GRADE.COMPARATIVE))

    def test_merge_properties__complex__properties_last(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|external|вн,буд]', externals=['external'])
        word = words.Word(type=r.WORD_TYPE.NOUN,
                          forms=helpers.TestForms.NOUN,
                          properties=words.Properties(r.CASE.DATIVE, r.GRADE.COMPARATIVE))
        self.assertEqual(substitution._merge_properties(externals={'external': word}), words.Properties(r.CASE.ACCUSATIVE, r.GRADE.COMPARATIVE, r.TIME.FUTURE))

    def test_merge_properties__complex__external_last(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|вн,буд|external]', externals=['external'])
        word = words.Word(type=r.WORD_TYPE.NOUN,
                          forms=helpers.TestForms.NOUN,
                          properties=words.Properties(r.CASE.DATIVE, r.GRADE.COMPARATIVE))
        self.assertEqual(substitution._merge_properties(externals={'external': word}), words.Properties(r.CASE.DATIVE, r.GRADE.COMPARATIVE, r.TIME.FUTURE))



class TemplateTests(TestCase):

    def setUp(self):
        super(TemplateTests, self).setUp()


    def test_init(self):
        template = templates.Template()
        self.assertEqual(template._substitutions, [])
        self.assertEqual(template._template, None)


    def test_parse(self):
        TEXT = u'[external_1|загл] 1 [ед3|external_2|буд] 2 [external_2|тв,ед]'

        template = templates.Template()

        template.parse(TEXT, externals=['external_1', 'external_2'])

        self.assertEqual(template._template, u'%s 1 %s 2 %s')

        self.assertEqual(len(template._substitutions), 3)

        substitution = template._substitutions[0]
        self.assertEqual(substitution.id, 'external_1')
        self.assertEqual(substitution.dependencies, [words.Properties(r.WORD_CASE.UPPER)])

        substitution = template._substitutions[1]
        self.assertEqual(substitution.id, u'ед3')
        self.assertEqual(substitution.dependencies, ['external_2', words.Properties(r.TIME.FUTURE)])

        substitution = template._substitutions[2]
        self.assertEqual(substitution.id, 'external_2')
        self.assertEqual(substitution.dependencies, [words.Properties(r.CASE.INSTRUMENTAL, r.NUMBER.SINGULAR)])


    def test_substitute(self):
        TEXT = u'[external_1|загл] 1 [ед3|external_2|буд] 2 [external_2|тв,ед]'

        word_1 = helpers.create_noun(properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE, r.NUMBER.PLURAL))
        word_2 = helpers.create_noun(prefix=u'x-', properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE))
        word_3 = helpers.create_noun(prefix=u'y-', properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE, r.NUMBER.PLURAL))

        dictionary = Dictionary()

        dictionary.add_word(word_1)
        dictionary.add_word(word_2)
        dictionary.add_word(word_3)

        template = templates.Template()

        template.parse(TEXT, externals=['external_1', 'external_2'])

        result = template.substitute(externals={'external_1': word_2,
                                                'external_2': word_3},
                                    dictionary=dictionary)

        self.assertEqual(result, u'X-ед1 1 мн3 2 y-мн5')
