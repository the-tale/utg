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

class FORM(WORD_PROPERTY):
    records = ( ('INFINITIVE', 0, u'инфинитив', u'инф'),
                ('NORMAL', 1, u'нормальная форма', u'норм'), )

class TIME(WORD_PROPERTY):
    records = ( ('PAST', 1, u'прошлое время', u'прш'),
                ('PRESENT', 2, u'настоящее время', u'нст'),
                ('FUTURE', 3, u'будущее будущее', u'буд') )

class PERSON(WORD_PROPERTY):
    records = ( ('FIRST', 0, u'1-ое лицо', u'1л'),
                ('SECOND', 1, u'2-ое лицо', u'2л'),
                ('THIRD', 2, u'3-е лицо', u'3л') )

class ASPECT(WORD_PROPERTY):
    records = ( ('IMPERFECTIVE', 0, u'несовершенный', u'несов'),
                ('PERFECTIVE', 1, u'совершенный', u'сов') )

class MOOD(WORD_PROPERTY):
    records = ( ('INDICATIVE', 0, u'изъявительное наклонение', u'изъяв'),
                ('CONDITIONAL', 1, u'согласительное наклонение', u'согл'),
                ('IMPERATIVE', 2, u'повелительное наклонение', u'пов') )

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

class WORD_CASE(WORD_PROPERTY):
    records = ( ('LOWER', 0, u'строчная', u'строч'),
                ('UPPER', 1, u'заглавная', u'загл') )


class WORD_TYPE(WORD_PROPERTY):
    schema = Column(unique=False)
    properties = Column(unique=False, no_index=True)

    records = ( ('NOUN', 0, u'существительное', u'сущ', (NUMBER, CASE), {ANIMALITY: True, GENDER: True, NUMBER: False }), # нарицательность, разряд, склонение
                ('ADJECTIVE', 1, u'прилагательное', u'прил', (NUMBER, CASE, GENDER, ANIMALITY, GRADE), {ADJECTIVE_CATEGORY: True}),
                ('PRONOUN', 2, u'местоимение', u'мест', ( NUMBER, CASE, PERSON, GENDER), {PRONOUN_CATEGORY: True}),
                ('VERB', 3, u'глагол', u'гл', (FORM, TIME, NUMBER, PERSON, GENDER, MOOD), {ASPECT: True}),
                ('PARTICIPLE', 4, u'причастие', u'прич', (NUMBER, CASE, GENDER, ANIMALITY, GRADE), {ASPECT: True}) )

# имя числительное;
# наречие;
# предлог;
# союз;
# частица;
# междометие;
# причастие;
# деепричастие;
