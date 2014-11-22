# coding: utf-8

from unittest import TestCase

from utg import words
from utg import templates
from utg import exceptions
from utg import relations as r
from utg.dictionary import Dictionary


class SubstitutionTests(TestCase):

    def setUp(self):
        super(SubstitutionTests, self).setUp()


    def test_init(self):
        substitution = templates.Substitution()
        self.assertEqual(substitution.id, None)
        self.assertEqual(substitution.dependencies, [])


    def test_serialization(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|external_1|дт|external_2|вн,личн]', externals=['bla-bla', 'external_1', 'external_2'])
        self.assertEqual(substitution.serialize(), templates.Substitution.deserialize(substitution.serialize()).serialize())


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

    def test_parse__upper_case(self):
        substitution = templates.Substitution.parse(variable=u'[Bla-bla]', externals=[''])
        self.assertEqual(substitution.id, 'bla-bla')
        self.assertEqual(substitution.dependencies, [words.Properties(r.WORD_CASE.UPPER)])


    def test_merge_properties__no_dependencies(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla]', externals=[])
        self.assertEqual(substitution._list_propeties(externals={}), ([], []))

    def test_merge_properties__external_not_in_externals(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|external]', externals=['external'])
        self.assertRaises(exceptions.ExternalDependecyNotFoundError, substitution._list_propeties, externals={})

    def test_merge_properties__properties(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|дт,сравн]', externals=[])
        self.assertEqual(substitution._list_propeties(externals={}), ([words.Properties(r.CASE.DATIVE, r.GRADE.COMPARATIVE)], []))

    def test_merge_properties__externals(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|external]', externals=['external'])
        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN,
                                           prefix='w-',
                                           properties=words.Properties(r.CASE.DATIVE, r.GRADE.COMPARATIVE))
        self.assertEqual(substitution._list_propeties(externals={'external': word}), ([words.Properties(r.CASE.DATIVE, r.GRADE.COMPARATIVE)], [word]))

    def test_merge_properties__complex__properties_last(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|external|вн,буд]', externals=['external'])
        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN,
                                           prefix='w-',
                                           properties=words.Properties(r.CASE.DATIVE, r.GRADE.COMPARATIVE))

        self.assertEqual(substitution._list_propeties(externals={'external': word}),
                         ([word.properties, words.Properties(r.CASE.ACCUSATIVE, r.TIME.FUTURE)], [word]))

    def test_merge_properties__complex__external_last(self):
        substitution = templates.Substitution.parse(variable=u'[bla-bla|вн,буд|external]', externals=['external'])
        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN,
                                           prefix='w-',
                                           properties=words.Properties(r.CASE.DATIVE, r.GRADE.COMPARATIVE))
        self.assertEqual(substitution._list_propeties(externals={'external': word}),
                         ([words.Properties(r.CASE.ACCUSATIVE, r.TIME.FUTURE), word.properties], [word]))



class TemplateTests(TestCase):

    def setUp(self):
        super(TemplateTests, self).setUp()


    def test_init(self):
        template = templates.Template()
        self.assertEqual(template._substitutions, [])
        self.assertEqual(template.template, None)


    def test_serialization(self):
        TEXT = u'[external_1|загл] 1 [ед3|external_2|буд] 2 [external_2|тв,ед]'
        template = templates.Template()
        template.parse(TEXT, externals=['external_1', 'external_2'])

        self.assertEqual(template.serialize(), templates.Template.deserialize(template.serialize()).serialize())


    def test_parse(self):
        TEXT = u'[external_1|загл] 1 [ед3|external_2|буд] 2 [external_2|тв,ед]'

        template = templates.Template()

        template.parse(TEXT, externals=['external_1', 'external_2'])

        self.assertEqual(template.template, u'%s 1 %s 2 %s')

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


    def test_parse__percent_symbol(self):
        TEXT = u'[external_1|загл] 1 [ед3|external_2|буд] 2% [external_2|тв,ед]'

        template = templates.Template()

        template.parse(TEXT, externals=['external_1', 'external_2'])

        self.assertEqual(template.template, u'%s 1 %s 2%% %s')


    def test_substitute(self):
        TEXT = u'[external_1|загл] 1 [w-нс,ед,тв|external_2|буд] 2 [external_2|тв,ед]'

        # TEXT = u'[external_2|тв,ед]'

        word_1 = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, prefix='w-', properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE))
        word_2 = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, prefix='x-', properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE))
        word_3 = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, prefix='y-', properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE, r.NUMBER.PLURAL))

        dictionary = Dictionary()

        dictionary.add_word(word_1)
        dictionary.add_word(word_2)
        dictionary.add_word(word_3)

        template = templates.Template()

        template.parse(TEXT, externals=['external_1', 'external_2'])

        result = template.substitute(externals={'external_1': dictionary.get_word(u'x-нс,ед,им'),
                                                'external_2': dictionary.get_word(u'y-нс,мн,им'),},
                                    dictionary=dictionary)

        self.assertEqual(result, u'X-нс,ед,им 1 w-нс,мн,им 2 y-нс,мн,тв')


    def test_substitute__percent_symbol(self):
        TEXT = u'[external_1|загл] 1 [w-нс,ед,тв|external_2|буд] 2% [external_2|тв,ед]'

        # TEXT = u'[external_2|тв,ед]'

        word_1 = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, prefix='w-', properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE))
        word_2 = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, prefix='x-', properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE))
        word_3 = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, prefix='y-', properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE, r.NUMBER.PLURAL))

        dictionary = Dictionary()

        dictionary.add_word(word_1)
        dictionary.add_word(word_2)
        dictionary.add_word(word_3)

        template = templates.Template()

        template.parse(TEXT, externals=['external_1', 'external_2'])

        result = template.substitute(externals={'external_1': dictionary.get_word(u'x-нс,ед,им'),
                                                'external_2': dictionary.get_word(u'y-нс,мн,им'),},
                                    dictionary=dictionary)

        self.assertEqual(result, u'X-нс,ед,им 1 w-нс,мн,им 2% y-нс,мн,тв')

    def test_get_undictionaried_words(self):
        word_1 = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, prefix='w-', properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE, r.NUMBER.PLURAL))
        word_2 = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, prefix='x-', properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE))
        word_3 = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, prefix='y-', properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE, r.NUMBER.PLURAL))

        dictionary = Dictionary()

        dictionary.add_word(word_1)
        dictionary.add_word(word_2)
        dictionary.add_word(word_3)

        TEXT = u'[external_1|загл] 1 [x-нс,ед,тв|external_2|буд] 2 [слово|тв,ед] [бла-бла]'

        template = templates.Template()

        template.parse(TEXT, externals=['external_1', 'external_2'])

        self.assertEqual(template.get_undictionaried_words(externals=['external_1', 'external_2'], dictionary=dictionary),
                         [u'слово', u'бла-бла'])
