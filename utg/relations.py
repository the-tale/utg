# coding: utf-8

from rels import EnumWithText, Column


class WORD_PROPERTY(EnumWithText):
    verbose_id = Column()


class CASE(WORD_PROPERTY):
    records = ( ('NOMINATIVE', 0, u'именительный', u'им'),
                ('GENITIVE', 1, u'родительный', u'рд'),
                ('DATIVE', 2, u'дательный', u'дт'),
                ('ACCUSATIVE', 3, u'винительный', u'вн'),
                ('INSTRUMENTAL', 4, u'творительный', u'тв'),
                ('PREPOSITIONAL', 5, u'предложный', u'пр'), )


class ANIMALITY(WORD_PROPERTY):
    records = ( ('ANIMATE', 0, u'одушевлённое', u'од'),
                ('INANIMATE', 1, u'неодушевлённое', u'но') )

class NUMBER(WORD_PROPERTY):
    records = ( ('SINGULAR', 0, u'единственное число', u'ед'),
                ('PLURAL', 1, u'множественное число', u'мн') )

class GENDER(WORD_PROPERTY):
    records = ( ('MASCULINE', 0, u'мужской род', u'мр'),
                ('NEUTER', 1, u'средний род', u'ср'),
                ('FEMININE', 2, u'женский род', u'жр') )

class VERB_FORM(WORD_PROPERTY):
    records = ( ('INFINITIVE', 0, u'инфинитив', u'инф'),
                ('INDICATIVE', 1, u'изъявительное наклонение', u'изъяв'),
                # ('CONDITIONAL', 2, u'согласительное наклонение', u'согл'),
                ('IMPERATIVE', 3, u'повелительное наклонение', u'пов') )

class VOICE(WORD_PROPERTY):
    records = ( ('DIRECT', 0, u'прямой залог', u'прям'),
                ('REVERSE', 1, u'возвратный залог', u'взв')  )

class TIME(WORD_PROPERTY):
    records = ( ('PAST', 1, u'прошедшее время', u'прш'),
                ('PRESENT', 2, u'настоящее время', u'нст'),
                ('FUTURE', 3, u'будущее время', u'буд') )

class PERSON(WORD_PROPERTY):
    records = ( ('FIRST', 0, u'1-ое лицо', u'1л'),
                ('SECOND', 1, u'2-ое лицо', u'2л'),
                ('THIRD', 2, u'3-е лицо', u'3л') )

class ASPECT(WORD_PROPERTY):
    records = ( ('IMPERFECTIVE', 0, u'несовершенный', u'несов'),
                ('PERFECTIVE', 1, u'совершенный', u'сов') )

class ADJECTIVE_CATEGORY(WORD_PROPERTY):
    records = ( ('QUALITY', 0, u'качественное', u'кач'),
                ('RELATIVE', 1, u'относительное', u'отн'),
                ('POSSESSIVE', 2, u'притяжательное', u'прит')  )

class GRADE(WORD_PROPERTY):
    records = ( ('POSITIVE', 0, u'положительная степень', u'пол'),
                ('COMPARATIVE', 1, u'сравнительная степень', u'сравн'),
                ('SUPERLATIVE', 2, u'превосходная степень', u'прев') )


class PRONOUN_CATEGORY(WORD_PROPERTY):
    records = ( ('PERSONAL', 0, u'личное', u'личн'),
                ('REFLEXIVE', 1, u'возвратное', u'возвр'),
                ('POSSESSIVE', 2, u'притяжательное', u'притяж'),
                ('INTERROGATIVE', 3, u'вопросительное', u'вопр'),
                ('RELATIVE', 4, u'относительное', u'относ'),
                ('DEMONSTRATIVE', 5, u'указательное', u'указат'),
                ('ATTRIBUTIVE', 6, u'определительное', u'опред'),
                ('NEGATIVE', 7, u'отрицательное', u'отриц'),
                ('VAGUE', 8, u'неопределённое', u'неопр'),
                ('MUTUAL', 9, u'взаимное', u'взаимн')  )


class INTEGER_FORM(WORD_PROPERTY):
    records = ( ('SINGULAR', 0, u'один', u'цо'),
                ('DUAL', 1, u'дуальные 2, 3, 4', u'цд'),
                ('COMPOSITE_DUAL', 2, u'составные дуальные на 2, 3, 4', u'цсд'),
                ('PLURAL', 3, u'остальные целые', u'цост'),
                ('MIL_BIL', 4, u'миллион и миллиард', u'цмм'), )

class NOUN_FORM(WORD_PROPERTY):
    records = ( ('NORMAL', 0, u'нормальная форма', u'нс'),
                ('COUNTABLE', 1, u'счётная форма', u'счт'))

class ADJECTIVE_FORM(WORD_PROPERTY):
    records = ( ('FULL', 0, u'полная форма', u'полнприл'),
                ('SHORT', 1, u'краткая форма', u'крприл'))

class PARTICIPLE_FORM(WORD_PROPERTY):
    records = ( ('FULL', 0, u'полная форма', u'полнприч'),
                ('SHORT', 1, u'краткая форма', u'крприч') )


class WORD_CASE(WORD_PROPERTY):
    records = ( ('LOWER', 0, u'строчная', u'строч'),
                ('UPPER', 1, u'заглавная', u'загл') )

class DEPENDENCY_MODE(WORD_PROPERTY):
    records = ( ('FULL', 0, u'полная зависимость', u'пзв'),
                ('SEMANTIC', 1, u'семантическая зависимость', u'сзв') )


class PREPOSITION_FORM(WORD_PROPERTY):
    records = ( ('NORMAL', 0, u'основная форма', u'осн'),
                ('ALTERNATIVE', 1, u'альтернативная форма', u'алт'),
                ('SPECIAL', 2, u'специальная форма', u'спц') )


class WORD_TYPE(WORD_PROPERTY):
    schema = Column(unique=False)
    properties = Column(unique=False, no_index=True)

    records = ( ('NOUN', 0, u'существительное', u'сущ', (NOUN_FORM, NUMBER, CASE), {ANIMALITY: True, GENDER: True, NUMBER: False }),
                ('ADJECTIVE', 1, u'прилагательное', u'прил', (ADJECTIVE_FORM, GRADE, ANIMALITY, NUMBER, CASE, GENDER), {ADJECTIVE_CATEGORY: True}),
                ('PRONOUN', 2, u'местоимение', u'мест', (ANIMALITY, NUMBER, CASE, GENDER), {PRONOUN_CATEGORY: True, PERSON: False}),
                ('VERB', 3, u'глагол', u'гл', (VERB_FORM, TIME, NUMBER, PERSON, GENDER), {ASPECT: True, VOICE: True}),
                ('PARTICIPLE', 4, u'причастие', u'прич', (PARTICIPLE_FORM, TIME, ANIMALITY, NUMBER, CASE, GENDER), {ASPECT: True, VOICE: True}),
                ('INTEGER', 5, u'целое число', u'целое', (), {NUMBER: True, INTEGER_FORM: True},),
                ('TEXT', 6, u'текст', u'текст', (), {},),
                ('PREPOSITION', 10, u'предлог', u'предл', (PREPOSITION_FORM,), {}) )


class PROPERTY_TYPE(EnumWithText):
    relation = Column()

    records = ( ('CASE', 0, u'падеж', CASE),
                ('ANIMALITY', 1, u'одушевлённость', ANIMALITY),
                ('NUMBER', 2, u'число', NUMBER),
                ('GENDER', 3, u'род', GENDER),
                ('FORM', 4, u'форма глагола', VERB_FORM),
                ('TIME', 5, u'время', TIME),
                ('PERSON', 6, u'лицо', PERSON),
                ('ASPECT', 7, u'вид', ASPECT),
                # ('MOOD', 8, u'наклонение', MOOD),
                ('ADJECTIVE_CATEGORY', 9, u'категория прилагательного', ADJECTIVE_CATEGORY),
                ('GRADE', 10, u'степень прилагательного', GRADE),
                ('PRONOUN_CATEGORY', 11, u'категория местоимения', PRONOUN_CATEGORY),
                ('WORD_CASE', 12, u'размер 1-ой буквы', WORD_CASE),
                ('WORD_TYPE', 13, u'часть речи', WORD_TYPE),
                ('INTEGER_FORM', 14, u'виды целых чисел', INTEGER_FORM),
                ('VOICE', 15, u'залог', VOICE),
                ('PREPOSITION_FORM', 16, u'форма предлога', PREPOSITION_FORM),
                ('ADJECTIVE_FORM', 17, u'форма прилагательного', ADJECTIVE_FORM),
                ('PARTICIPLE_FORM', 18, u'форма причастия', PARTICIPLE_FORM),
                ('NOUN_FORM', 19, u'форма существительного', NOUN_FORM),
                ('DEPENDENCY_MODE', 20, u'вид зависимости между словами', DEPENDENCY_MODE)
              )

# имя числительное;
# наречие;
# союз;
# частица;
# междометие;
# деепричастие;
