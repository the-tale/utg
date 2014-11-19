# coding: utf-8
import copy
import random

from unittest import TestCase

from utg import words
from utg import logic
from utg import data
from utg import relations as r


class PropertiesTests(TestCase):

    def setUp(self):
        super(PropertiesTests, self).setUp()

    def test_construct__empty(self):
        properties = words.Properties()
        self.assertEqual(properties._data, {})

    def test_construct(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)

        self.assertTrue(properties._data[r.CASE].is_DATIVE)
        self.assertTrue(properties._data[r.NUMBER].is_PLURAL)
        self.assertTrue(properties._data[r.PERSON].is_SECOND)

    def test_serialization(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)
        self.assertEqual(properties.serialize(), words.Properties.deserialize(properties.serialize()).serialize())

    def test_update__empty(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)

        old_data = copy.copy(properties._data)

        properties._update()

        self.assertEqual(old_data, properties._data)

    def test_update(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)
        properties._update(r.NUMBER.SINGULAR, r.TIME.FUTURE)

        self.assertTrue(properties._data[r.CASE].is_DATIVE)
        self.assertTrue(properties._data[r.NUMBER].is_SINGULAR)
        self.assertTrue(properties._data[r.PERSON].is_SECOND)
        self.assertTrue(properties._data[r.TIME].is_FUTURE)

    def test_get(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)

        for relation in logic.get_property_relations():
            if relation == r.WORD_TYPE:
                self.assertEqual(properties.get(relation), None)
            elif relation in properties._data:
                self.assertEqual(properties.get(relation), properties._data[relation])
            else:
                self.assertEqual(properties.get(relation), relation.records[0])

    def test_get_key(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.GENDER.FEMININE)
        self.assertEqual(properties.get_key(key=[]), ())
        self.assertEqual(properties.get_key(key=(r.TIME, r.CASE, r.GENDER)), (r.TIME.PAST, r.CASE.DATIVE, r.GENDER.FEMININE))

    def test_get_key__restrictions(self):
        properties = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND, r.GENDER.FEMININE)
        schema = (r.TIME, r.CASE, r.GENDER, r.PERSON)
        key = (r.CASE, r.GENDER, r.PERSON)
        self.assertEqual(properties.get_key(schema=schema, key=key),
                         (r.CASE.DATIVE, r.GENDER.FEMININE, None))

    def test_eq(self):
        properties_1 = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)

        properties_2 = words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, r.PERSON.SECOND)

        self.assertEqual(properties_1, properties_2)

        properties_3 = words.Properties(properties_2, r.NUMBER.SINGULAR)

        self.assertNotEqual(properties_1, properties_3)



class WordTests(TestCase):

    def setUp(self):
        super(WordTests, self).setUp()

    def test_init(self):
        word = words.Word(type=r.WORD_TYPE.VERB, forms=['x1', 'x2', 'x3'], properties=words.Properties(r.CASE.DATIVE, r.TIME.FUTURE))
        self.assertTrue(word.type.is_VERB)
        self.assertEqual(word.forms, ['x1', 'x2', 'x3'])
        self.assertEqual(word.properties, words.Properties(r.CASE.DATIVE, r.TIME.FUTURE))

    def test_serialization(self):
        patch = words.Word(type=r.WORD_TYPE.NOUN_COUNTABLE_FORM,
                          forms=['y1', 'y2', 'y3'],
                          properties=words.Properties(r.CASE.ACCUSATIVE,) )
        word = words.Word(type=r.WORD_TYPE.NOUN,
                          forms=['x1', 'x2', 'x3'],
                          properties=words.Properties(r.CASE.DATIVE, r.TIME.FUTURE),
                          patches={r.WORD_TYPE.NOUN_COUNTABLE_FORM: patch})
        self.assertEqual(word.serialize(), words.Word.deserialize(word.serialize()).serialize())

    def test_get_forms_number__integer(self):
        self.assertEqual(words.Word.get_forms_number(r.WORD_TYPE.INTEGER), 1)


    def test_form(self):
        word = words.Word.create_test_word(r.WORD_TYPE.NOUN, properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE))

        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE)), u'w-ед,дт')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL)), u'w-мн,дт')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.TIME.FUTURE)), u'w-ед,дт')


    def test_form__optional_property(self):
        word = words.Word.create_test_word(r.WORD_TYPE.NOUN, properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE, r.NUMBER.PLURAL))

        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE)), u'w-мн,дт')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL)), u'w-мн,дт')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.TIME.FUTURE)), u'w-мн,дт')

        word = words.Word.create_test_word(r.WORD_TYPE.NOUN, properties=words.Properties(r.GENDER.FEMININE, r.ANIMALITY.INANIMATE, r.NUMBER.SINGULAR))

        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE)), u'w-ед,дт')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL)), u'w-ед,дт')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.TIME.FUTURE)), u'w-ед,дт')

    def test_normal_form(self):
        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, only_required=True)
        self.assertEqual(word.normal_form(), word.forms[0])

    def test_normal_form__fixed_properties(self):
        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, only_required=True, properties=words.Properties(r.NUMBER.PLURAL))
        self.assertEqual(word.normal_form(), u'w-мн,им')

    def test_patch(self):
        patch = words.Word.create_test_word(type=r.WORD_TYPE.NOUN_COUNTABLE_FORM,
                                            prefix='p-')
        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN,
                                           prefix='w-',
                                           patches={r.WORD_TYPE.NOUN_COUNTABLE_FORM: patch})

        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.NUMBER.SINGULAR)), u'w-ед,дт')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL)), u'w-мн,дт')
        self.assertEqual(word.form(words.Properties(r.CASE.DATIVE, r.NUMBER.PLURAL, random.choice(r.INTEGER_FORM.records))), u'p-дт')


    def test_number_of_syllables(self):
        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN)
        word.forms[0] = u'б'
        self.assertEqual(word.number_of_syllables, 1)

        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN)
        word.forms[0] = u'а'
        self.assertEqual(word.number_of_syllables, 1)

        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN)
        word.forms[0] = u'абвг'
        self.assertEqual(word.number_of_syllables, 1)

        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN)
        word.forms[0] = u'абракадабра'
        self.assertEqual(word.number_of_syllables, 5)

    def test_has_fluent_vowel(self):
        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN)
        word.forms = [u'абракадубр']*len(word.forms)
        self.assertFalse(word.has_fluent_vowel)

        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN)
        word.forms = [u'абракадубр'] + [u'абракадубр' + random.choice(list(data.VOWELS)) for i in xrange(len(word.forms)-1)]
        self.assertFalse(word.has_fluent_vowel)

        word = words.Word(type=r.WORD_TYPE.NOUN_COUNTABLE_FORM,
                                   forms=[u'сон', u'сна', u'сну', u'сон', u'сном', u'сне',
                                          u'сны', u'снов', u'снам', u'сны', u'снами', u'снах'],
                                   properties=words.Properties(r.GENDER.MASCULINE, r.ANIMALITY.INANIMATE))
        self.assertTrue(word.has_fluent_vowel)


    def test_all_forms(self):
        patch = words.Word.create_test_word(type=r.WORD_TYPE.NOUN_COUNTABLE_FORM, prefix=u'p-')
        patches = {r.WORD_TYPE.NOUN_COUNTABLE_FORM: patch}
        word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, patches=patches)

        forms = list(word.all_forms())

        self.assertEqual(len(forms), 6*2+6)
        # print u'\n'.join([word_form.form for word_form in forms])
        self.assertEqual([word_form.form for word_form in forms], word.forms + patch.forms)



class WordFormTests(TestCase):

    def setUp(self):
        super(WordFormTests, self).setUp()
        self.word = words.Word.create_test_word(type=r.WORD_TYPE.NOUN, only_required=True)

    def test_init__simple(self):
        form = words.WordForm(word=self.word, properties=words.Properties(r.NUMBER.PLURAL))
        self.assertEqual(form.properties, words.Properties(r.NUMBER.PLURAL))
        self.assertEqual(form.form_properties, words.Properties(r.NUMBER.PLURAL))

    def test_form(self):
        form = words.WordForm(word=self.word,
                              properties=words.Properties(r.NUMBER.PLURAL),
                              form_properties=words.Properties(r.NUMBER.PLURAL, r.CASE.DATIVE),)
        self.assertEqual(form.form, u'w-мн,дт')


    def test_starts_with_consonant_cluster(self):
        word = words.Word(type=r.WORD_TYPE.NOUN_COUNTABLE_FORM,
                          forms=[u'сон', u'сна', u'сну', u'сон', u'сном', u'сне',
                                 u'сны', u'снов', u'снам', u'сны', u'снами', u'снах'],
                          properties=words.Properties(r.GENDER.MASCULINE, r.ANIMALITY.INANIMATE))

        form = words.WordForm(word=word, properties=words.Properties(r.CASE.NOMINATIVE)) # сон
        self.assertFalse(form.starts_with_consonant_cluster)

        form = words.WordForm(word=word, properties=words.Properties(r.CASE.DATIVE)) # сну
        self.assertTrue(form.starts_with_consonant_cluster)
