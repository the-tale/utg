# coding: utf-8


from unittest import TestCase

from utg import relations as r
from utg import restrictions as restr
from utg import logic
from utg import data
from utg import dictionary
from utg import words
from utg import templates
from utg import constructors


EXPECTED_ORDER = [ r.VERB_FORM,
                   r.ADJECTIVE_FORM,
                   r.PARTICIPLE_FORM,
                   r.NOUN_FORM,

                   r.ADJECTIVE_CATEGORY,
                   r.PRONOUN_CATEGORY,

                   r.GRADE,

                   r.TIME,
                   r.VOICE,
                   r.ASPECT,

                   # ANIMALITY must be before NUMBER, CASE & GENDER to correct work of nearest_key for adjective & participle
                   r.ANIMALITY,

                   r.NUMBER,
                   r.CASE,
                   r.PERSON,
                   r.GENDER,

                   r.INTEGER_FORM,

                   r.WORD_CASE,
                   r.DEPENDENCY_MODE,

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
        for word_type, restrictions in restr.RESTRICTIONS.iteritems():
            for key, word_type_restrictions in restrictions.iteritems():
                for restriction in word_type_restrictions:
                    self.assertTrue(EXPECTED_ORDER.index(key._relation) < EXPECTED_ORDER.index(restriction))

    def test_only_schema_properties_in_restrictions(self):
        for word_type, restrictions in restr.RESTRICTIONS.iteritems():
            for key, word_type_restrictions in restrictions.iteritems():
                self.assertIn(key._relation, set(word_type.schema)|set(word_type.properties))
                for restriction in word_type_restrictions:
                    self.assertIn(restriction, set(word_type.schema)|set(word_type.properties))

    def test_presets(self):
        for preset_owner, preset_slave in restr.PRESETS.iteritems():
            for word_type, cache in data.WORDS_CACHES.iteritems():
                if preset_owner._relation not in word_type.schema or preset_slave._relation not in word_type.schema:
                    continue

                for key in cache:
                    if preset_owner not in key:
                        continue

                    self.assertIn(preset_slave, key)


    def test_unique_verbose_ids(self):
        properties = set()

        for properties_relation in logic.get_property_relations():
            for property in properties_relation.records:
                self.assertFalse(property.verbose_id in properties)
                properties.add(property.verbose_id)

    def test_all_property_types_in_relation(self):
        for properties_relation in logic.get_property_relations():
            self.assertTrue(properties_relation in r.PROPERTY_TYPE.index_relation)

    # example from readme
    def test_full_usage(self):
        # описываем существительное для словаря
        coins_word = words.Word(type=r.WORD_TYPE.NOUN,
                                forms=[ u'монета', u'монеты', u'монете', u'монету', u'монетой', u'монете',    # единственнео число
                                        u'монеты', u'монет', u'монетам', u'монеты', u'монетами', u'монетах',  # множественное число
                                        u'монеты', u'монет', u'монетам', u'монеты', u'монетами', u'монетах'], # счётное число (заполнено для пример, может быть заполнено методом autofill_missed_forms)
                                properties=words.Properties(r.ANIMALITY.INANIMATE, r.GENDER.FEMININE)) # свойства: неодушевлённое, женский род

        # описываем глагол для словаря
        action_word = words.Word(type=r.WORD_TYPE.VERB,
                                 # описываем только нужны нам формы слова (порядок важен и определён в utg.data.WORDS_CACHES[r.WORD_TYPE.VERB])
                                 forms=[u'подарить', u'подарил', u'подарило', u'подарила', u'подарили'] + [u''] * (len(data.WORDS_CACHES[r.WORD_TYPE.VERB]) - 5),
                                 properties=words.Properties(r.ASPECT.PERFECTIVE, r.VOICE.DIRECT) )
        action_word.autofill_missed_forms() # заполняем пропущенные формы на основе введённых (выбираются наиболее близкие)

        # создаём словарь для использования в шаблонах
        test_dictionary = dictionary.Dictionary(words=[coins_word, action_word])

        # создаём шаблон
        template = templates.Template()

        # externals — внешние переменные, не обязаны быть в словаре
        template.parse(u'[Npc] [подарил|npc] [hero|дт] [coins] [монета|coins|вн].', externals=('hero', 'npc', 'coins'))

        # описываем внешние переменные
        hero = words.WordForm(words.Word(type=r.WORD_TYPE.NOUN,
                                           forms=[u'герой', u'героя', u'герою', u'героя', u'героем', u'герое',
                                                  u'герои', u'героев', u'героям', u'героев', u'героями', u'героях',
                                                  u'герои', u'героев', u'героям', u'героев', u'героями', u'героях'],
                                           properties=words.Properties(r.ANIMALITY.ANIMATE, r.GENDER.MASCULINE)))

        npc = words.WordForm(words.Word(type=r.WORD_TYPE.NOUN,
                                           forms=[u'русалка', u'русалки', u'русалке', u'русалку', u'русалкой', u'русалке',
                                                  u'русалки', u'русалок', u'русалкам', u'русалок', u'русалками', u'русалках',
                                                  u'русалки', u'русалок', u'русалкам', u'русалок', u'русалками', u'русалках'],
                                           properties=words.Properties(r.ANIMALITY.ANIMATE, r.GENDER.FEMININE)))

        # осуществляем подстановку
        result = template.substitute(externals={'hero': hero,
                                                'npc': npc,
                                                'coins': constructors.construct_integer(125)},
                                     dictionary=test_dictionary)

        self.assertEqual(result, u'Русалка подарила герою 125 монет.')
