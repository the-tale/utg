# coding: utf-8

from unittest import TestCase

from utg import words
from utg import exceptions
from utg import relations as r
from utg.dictionary import Dictionary



class DictionaryTests(TestCase):

    def setUp(self):
        super(DictionaryTests, self).setUp()
        self.dictionary = Dictionary()

    def test_init(self):
        self.assertEqual(self.dictionary._data, {})


    def test_add_word(self):
        word = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        self.dictionary.add_word(word)

        self.assertEqual(self.dictionary._data,
                         {'x1': words.WordForm(word, properties=word.properties.clone(r.CASE.NOMINATIVE, r.NUMBER.SINGULAR)),
                          'x2': words.WordForm(word, properties=word.properties.clone(r.CASE.GENITIVE, r.NUMBER.SINGULAR)),
                          'x3': words.WordForm(word, properties=word.properties.clone(r.CASE.DATIVE, r.NUMBER.SINGULAR))})

    def test_add_word__duplicate_normal_form(self):
        word = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        self.dictionary.add_word(word)

        word = words.Word(type=r.WORD_TYPE.VERB, forms=['x1', 'y2', 'y3'], properties=words.Properties())
        self.dictionary.add_word(word)

        self.assertTrue(self.dictionary.get_word('x1').word.type.is_NOUN)
        self.assertTrue(self.dictionary.get_word('x2').word.type.is_NOUN)
        self.assertTrue(self.dictionary.get_word('y2').word.type.is_VERB)


    def test_add_word__duplicate_normal_form__inverse_add_order(self):
        word = words.Word(type=r.WORD_TYPE.VERB, forms=['x1', 'y2', 'y3'], properties=words.Properties())
        self.dictionary.add_word(word)

        word = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        self.dictionary.add_word(word)

        self.assertTrue(self.dictionary.get_word('x1').word.type.is_NOUN)
        self.assertTrue(self.dictionary.get_word('x2').word.type.is_NOUN)
        self.assertTrue(self.dictionary.get_word('y2').word.type.is_VERB)


    def check_add_order(self, text, word_1, word_2, expexted_word):
        dictionary = Dictionary()

        dictionary.add_word(word_1)
        dictionary.add_word(word_2)

        self.assertEqual(dictionary.get_word(text).word, expexted_word)

        dictionary = Dictionary()

        dictionary.add_word(word_2)
        dictionary.add_word(word_1)

        self.assertEqual(dictionary.get_word(text).word, expexted_word)


    def test_add_order__type(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['x1'], properties=words.Properties())
        self.check_add_order('x1', word_1, word_2, word_1)


    def test_add_order__forms(self):
        word_1 = words.Word(type=r.WORD_TYPE.VERB, forms=['x1'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['x2'], properties=words.Properties())
        self.check_add_order('x1', word_1, word_2, word_1)


    def test_add_order__manhattan(self):
        word_1 = words.Word(type=r.WORD_TYPE.VERB, forms=['x1'], properties=words.Properties(r.NUMBER.PLURAL, r.CASE.DATIVE, r.TIME.FUTURE))
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['x1'], properties=words.Properties(r.TIME.FUTURE, r.PERSON.SECOND))
        self.check_add_order('x1', word_1, word_2, word_2)

    def test_add_order__on_word(self):
        word_1 = words.Word(type=r.WORD_TYPE.VERB, forms=['x1'], properties=words.Properties(r.NUMBER.PLURAL, r.CASE.DATIVE, r.TIME.FUTURE))
        self.check_add_order('x1', word_1, word_1, word_1)


    def test_add_word__duplicates_in_one_word(self):
        word = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x1'], properties=words.Properties())
        self.dictionary.add_word(word)

        self.assertEqual(self.dictionary._data,
                         {'x1': words.WordForm(word, properties=word.properties.clone(r.CASE.NOMINATIVE, r.NUMBER.SINGULAR)),
                          'x2': words.WordForm(word, properties=word.properties.clone(r.CASE.GENITIVE, r.NUMBER.SINGULAR))})


    def test_add_word__duplicates_in_defferent_words(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertEqual(self.dictionary._data,
                         {'x1': words.WordForm(word_1, properties=word_1.properties.clone(r.CASE.NOMINATIVE, r.NUMBER.SINGULAR)),
                          'x2': words.WordForm(word_1, properties=word_1.properties.clone(r.CASE.GENITIVE, r.NUMBER.SINGULAR)),
                          'x3': words.WordForm(word_1, properties=word_1.properties.clone(r.CASE.DATIVE, r.NUMBER.SINGULAR)),
                          'y1': words.WordForm(word_2, properties=word_2.properties.clone(r.VERB_FORM.INFINITIVE)),
                          'y3': words.WordForm(word_2, properties=word_2.properties.clone(r.GENDER.MASCULINE, r.VERB_FORM.NORMAL, r.TIME.PAST, r.MOOD.CONDITIONAL, r.NUMBER.SINGULAR))})


    def test_add_word__duplicates_in_defferent_words__inverse_add(self):
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertEqual(self.dictionary._data,
                         {'x1': words.WordForm(word_1, properties=word_1.properties.clone(r.CASE.NOMINATIVE, r.NUMBER.SINGULAR)),
                          'x2': words.WordForm(word_1, properties=word_1.properties.clone(r.CASE.GENITIVE, r.NUMBER.SINGULAR)),
                          'x3': words.WordForm(word_1, properties=word_1.properties.clone(r.CASE.DATIVE, r.NUMBER.SINGULAR)),
                          'y1': words.WordForm(word_2, properties=word_2.properties.clone(r.VERB_FORM.INFINITIVE)),
                          'y3': words.WordForm(word_2, properties=word_2.properties.clone(r.GENDER.MASCULINE, r.VERB_FORM.NORMAL, r.TIME.PAST, r.MOOD.CONDITIONAL, r.NUMBER.SINGULAR))})


    def test_get_word(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        properties_1_1 = words.Properties(r.CASE.NOMINATIVE, r.NUMBER.SINGULAR)
        properties_1_2 = words.Properties(r.CASE.GENITIVE, r.NUMBER.SINGULAR)
        properties_1_3 = words.Properties(r.CASE.DATIVE, r.NUMBER.SINGULAR)

        properties_2_1 = words.Properties(r.VERB_FORM.INFINITIVE)
        properties_2_3 = words.Properties(r.TIME.PAST, r.NUMBER.SINGULAR, r.GENDER.MASCULINE, r.MOOD.CONDITIONAL, r.VERB_FORM.NORMAL)

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertEqual(self.dictionary.get_word('x1'), words.WordForm(word=word_1, properties=properties_1_1))
        self.assertEqual(self.dictionary.get_word('x2'), words.WordForm(word=word_1, properties=properties_1_2))
        self.assertEqual(self.dictionary.get_word('x3'), words.WordForm(word=word_1, properties=properties_1_3))
        self.assertEqual(self.dictionary.get_word('y1'), words.WordForm(word=word_2, properties=properties_2_1))
        self.assertEqual(self.dictionary.get_word('y3'), words.WordForm(word=word_2, properties=properties_2_3))


    def test_has_word(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertFalse(self.dictionary.has_word('z'))
        self.assertTrue(self.dictionary.has_word('x1'))
        self.assertTrue(self.dictionary.has_word('x2'))
        self.assertTrue(self.dictionary.has_word('x3'))
        self.assertTrue(self.dictionary.has_word('y1'))
        self.assertTrue(self.dictionary.has_word('y3'))


    def test_get_word__no_words(self):
        word_1 = words.Word(type=r.WORD_TYPE.NOUN, forms=['x1', 'x2', 'x3'], properties=words.Properties())
        word_2 = words.Word(type=r.WORD_TYPE.VERB, forms=['y1', 'x2', 'y3'], properties=words.Properties())

        self.dictionary.add_word(word_1)
        self.dictionary.add_word(word_2)

        self.assertRaises(exceptions.NoWordsFoundError, self.dictionary.get_word, 'z')
