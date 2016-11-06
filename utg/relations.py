# coding: utf-8

from rels import EnumWithText, Column


class WORD_PROPERTY(EnumWithText):
    verbose_id = Column()


class CASE(WORD_PROPERTY):
    records = ( ('NOMINATIVE', 0, 'именительный', 'им'),
                ('GENITIVE', 1, 'родительный', 'рд'),
                ('DATIVE', 2, 'дательный', 'дт'),
                ('ACCUSATIVE', 3, 'винительный', 'вн'),
                ('INSTRUMENTAL', 4, 'творительный', 'тв'),
                ('PREPOSITIONAL', 5, 'предложный', 'пр'), )


class ANIMALITY(WORD_PROPERTY):
    records = ( ('ANIMATE', 0, 'одушевлённое', 'од'),
                ('INANIMATE', 1, 'неодушевлённое', 'но') )

class NUMBER(WORD_PROPERTY):
    records = ( ('SINGULAR', 0, 'единственное число', 'ед'),
                ('PLURAL', 1, 'множественное число', 'мн') )

class GENDER(WORD_PROPERTY):
    records = ( ('MASCULINE', 0, 'мужской род', 'мр'),
                ('NEUTER', 1, 'средний род', 'ср'),
                ('FEMININE', 2, 'женский род', 'жр') )

class VERB_FORM(WORD_PROPERTY):
    records = ( ('INFINITIVE', 0, 'инфинитив', 'инф'),
                ('INDICATIVE', 1, 'изъявительное наклонение', 'изъяв'),
                # ('CONDITIONAL', 2, u'согласительное наклонение', u'согл'),
                ('IMPERATIVE', 3, 'повелительное наклонение', 'пов') )

class VOICE(WORD_PROPERTY):
    records = ( ('DIRECT', 0, 'прямой залог', 'прям'),
                ('REVERSE', 1, 'возвратный залог', 'взв')  )

class TIME(WORD_PROPERTY):
    records = ( ('PAST', 1, 'прошедшее время', 'прш'),
                ('PRESENT', 2, 'настоящее время', 'нст'),
                ('FUTURE', 3, 'будущее время', 'буд') )

class PERSON(WORD_PROPERTY):
    records = ( ('FIRST', 0, '1-ое лицо', '1л'),
                ('SECOND', 1, '2-ое лицо', '2л'),
                ('THIRD', 2, '3-е лицо', '3л') )

class ASPECT(WORD_PROPERTY):
    records = ( ('IMPERFECTIVE', 0, 'несовершенный', 'несов'),
                ('PERFECTIVE', 1, 'совершенный', 'сов') )

class ADJECTIVE_CATEGORY(WORD_PROPERTY):
    records = ( ('QUALITY', 0, 'качественное', 'кач'),
                ('RELATIVE', 1, 'относительное', 'отн'),
                ('POSSESSIVE', 2, 'притяжательное', 'прит')  )

class GRADE(WORD_PROPERTY):
    records = ( ('POSITIVE', 0, 'положительная степень', 'пол'),
                ('COMPARATIVE', 1, 'сравнительная степень', 'сравн'),
                ('SUPERLATIVE', 2, 'превосходная степень', 'прев') )


class PRONOUN_CATEGORY(WORD_PROPERTY):
    records = ( ('PERSONAL', 0, 'личное', 'личн'),
                ('REFLEXIVE', 1, 'возвратное', 'возвр'),
                ('POSSESSIVE', 2, 'притяжательное', 'притяж'),
                ('INTERROGATIVE', 3, 'вопросительное', 'вопр'),
                ('RELATIVE', 4, 'относительное', 'относ'),
                ('DEMONSTRATIVE', 5, 'указательное', 'указат'),
                ('ATTRIBUTIVE', 6, 'определительное', 'опред'),
                ('NEGATIVE', 7, 'отрицательное', 'отриц'),
                ('VAGUE', 8, 'неопределённое', 'неопр'),
                ('MUTUAL', 9, 'взаимное', 'взаимн')  )


class INTEGER_FORM(WORD_PROPERTY):
    records = ( ('SINGULAR', 0, 'один', 'цо'),
                ('DUAL', 1, 'дуальные 2, 3, 4', 'цд'),
                ('COMPOSITE_DUAL', 2, 'составные дуальные на 2, 3, 4', 'цсд'),
                ('PLURAL', 3, 'остальные целые', 'цост'),
                ('MIL_BIL', 4, 'миллион и миллиард', 'цмм'), )

class NOUN_FORM(WORD_PROPERTY):
    records = ( ('NORMAL', 0, 'нормальная форма', 'нс'),
                ('COUNTABLE', 1, 'счётная форма', 'счт'))

class ADJECTIVE_FORM(WORD_PROPERTY):
    records = ( ('FULL', 0, 'полная форма', 'полнприл'),
                ('SHORT', 1, 'краткая форма', 'крприл'))

class PARTICIPLE_FORM(WORD_PROPERTY):
    records = ( ('FULL', 0, 'полная форма', 'полнприч'),
                ('SHORT', 1, 'краткая форма', 'крприч') )


class WORD_CASE(WORD_PROPERTY):
    records = ( ('LOWER', 0, 'строчная', 'строч'),
                ('UPPER', 1, 'заглавная', 'загл') )

class DEPENDENCY_MODE(WORD_PROPERTY):
    records = ( ('FULL', 0, 'полная зависимость', 'пзв'),
                ('SEMANTIC', 1, 'семантическая зависимость', 'сзв') )


class PREPOSITION_FORM(WORD_PROPERTY):
    records = ( ('NORMAL', 0, 'основная форма', 'осн'),
                ('ALTERNATIVE', 1, 'альтернативная форма', 'алт'),
                ('SPECIAL', 2, 'специальная форма', 'спц') )


class WORD_TYPE(WORD_PROPERTY):
    schema = Column(unique=False)
    properties = Column(unique=False, no_index=True)

    records = ( ('NOUN', 0, 'существительное', 'сущ', (NOUN_FORM, NUMBER, CASE), {ANIMALITY: True, GENDER: True, NUMBER: False }),
                ('ADJECTIVE', 1, 'прилагательное', 'прил', (ADJECTIVE_FORM, GRADE, ANIMALITY, NUMBER, CASE, GENDER), {ADJECTIVE_CATEGORY: True}),
                ('PRONOUN', 2, 'местоимение', 'мест', (ANIMALITY, NUMBER, CASE, GENDER), {PRONOUN_CATEGORY: True, PERSON: False}),
                ('VERB', 3, 'глагол', 'гл', (VERB_FORM, TIME, NUMBER, PERSON, GENDER), {ASPECT: True, VOICE: True}),
                ('PARTICIPLE', 4, 'причастие', 'прич', (PARTICIPLE_FORM, TIME, ANIMALITY, NUMBER, CASE, GENDER), {ASPECT: True, VOICE: True}),
                ('INTEGER', 5, 'целое число', 'целое', (), {NUMBER: True, INTEGER_FORM: True},),
                ('TEXT', 6, 'текст', 'текст', (), {},),
                ('PREPOSITION', 10, 'предлог', 'предл', (PREPOSITION_FORM,), {}) )


class PROPERTY_TYPE(EnumWithText):
    relation = Column(no_index=False)

    records = ( ('CASE', 0, 'падеж', CASE),
                ('ANIMALITY', 1, 'одушевлённость', ANIMALITY),
                ('NUMBER', 2, 'число', NUMBER),
                ('GENDER', 3, 'род', GENDER),
                ('FORM', 4, 'форма глагола', VERB_FORM),
                ('TIME', 5, 'время', TIME),
                ('PERSON', 6, 'лицо', PERSON),
                ('ASPECT', 7, 'вид', ASPECT),
                # ('MOOD', 8, u'наклонение', MOOD),
                ('ADJECTIVE_CATEGORY', 9, 'категория прилагательного', ADJECTIVE_CATEGORY),
                ('GRADE', 10, 'степень прилагательного', GRADE),
                ('PRONOUN_CATEGORY', 11, 'категория местоимения', PRONOUN_CATEGORY),
                ('WORD_CASE', 12, 'размер 1-ой буквы', WORD_CASE),
                ('WORD_TYPE', 13, 'часть речи', WORD_TYPE),
                ('INTEGER_FORM', 14, 'виды целых чисел', INTEGER_FORM),
                ('VOICE', 15, 'залог', VOICE),
                ('PREPOSITION_FORM', 16, 'форма предлога', PREPOSITION_FORM),
                ('ADJECTIVE_FORM', 17, 'форма прилагательного', ADJECTIVE_FORM),
                ('PARTICIPLE_FORM', 18, 'форма причастия', PARTICIPLE_FORM),
                ('NOUN_FORM', 19, 'форма существительного', NOUN_FORM),
                ('DEPENDENCY_MODE', 20, 'вид зависимости между словами', DEPENDENCY_MODE)
              )


# имя числительное;
# наречие;
# союз;
# частица;
# междометие;
# деепричастие;


class TOKEN_TYPE(WORD_PROPERTY):
    records = (('START', 0, 'начало'),
               ('FINISH', 1, 'конец'),
               ('WORD', 2, 'слово'),
               ('NUMBER', 3, 'число'),
               ('PUNCTUATION', 4, 'пунктуация'),
               ('SPACE', 5, u'пробел'))
