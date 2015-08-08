# coding: utf-8

from utg import relations as r
from utg import exceptions
from utg import data

# No need in master_properties since they are already in slave_propeties
def transform(slave_word, slave_propeties, master_form):

    transformator = _TRANSFORMATORS.get((slave_word.type, master_form.word.type))

    if transformator:
        return transformator(slave_word=slave_word, properties=slave_propeties, master_form=master_form)

    return slave_propeties


def _preposition_any(properties, slave_word, master_form):
    # http://newforum.gramota.ru/viewtopic.php?f=3&t=1045

    # В условиях контекста возможны дублеты типа в введении – во введении.
    # Добавление гласного о к предлогу, состоящему из одного согласного звука или оканчивающемуся на согласный, наблюдается в ряде случаев:

    slave = slave_word.normal_form()

    if slave[-1] in data.CONSONANTS:
        return _consonant_preposition_any(slave, properties, slave_word, master_form)

    return _vowels_preposition_any(slave, properties, slave_word, master_form)


def _consonant_preposition_any(slave, properties, slave_word, master_form):
    # http://newforum.gramota.ru/viewtopic.php?f=3&t=1045

    master = master_form.form

    # 1) перед односложным словом, начинающимся со стечения согласных, с беглым гласным в корне,
    #    например: во сне (ср.: в сновидениях), во рту (ср.: в ртутных испарениях), во льну (ср.: в льнотеребилках), ко мне (ср.: к мнимой величине);
    if ( master_form.starts_with_consonant_cluster and
         master_form.word.number_of_syllables == 1 and
         master_form.word.has_fluent_vowel):
        return properties.clone(r.PREPOSITION_FORM.ALTERNATIVE)

    # 2) часто после предлогов в и с, если с этих же согласных начинается последующее стечение согласных, например: во власти, во внушении, со слезами, со словами, со страху;
    if (slave in (u'в', u'с') and
        slave == master[0] and
        master_form.starts_with_consonant_cluster):
        return properties.clone(r.PREPOSITION_FORM.ALTERNATIVE)

    # 3) в отдельных фразеологических выражениях, например: во сто крат, изо всех сил, во главе войск, как кур во щи;
    # NotImplemented

    # 4) в текстах, имеющих оттенок торжественности, например: Во дни сомнений, во дни тягостных раздумий о судьбах моей родины... (Тургенев);
    # NotImplemented

    # 5) в сочетаниях официального стиля, например: во избежание, во исполнение, во имя (перед начальным гласным слова).
    # NotImplemented

    return properties


def _vowels_preposition_any(slave, properties, slave_word, master_form):
    # http://russ.hashcode.ru/questions/33493/правописание-предлог-об-и-обо

    master = master_form.form

    # Прелоги ОБО используется в особых случаях,
    # а именно с некоторыми местоимениями: обо мне, обо всех, обо всём (П.п.), обо что (В.п.), но: о тебе, о других, о чём.
    # Это традиционный принцип. Возможно, эти исключения связаны с влиянием беглых гласных, например: меня - обо мне (вместо "об мене"), сравнить: тебя - о тебе.
    if ( slave == u'о' and
         master in (u'всех', u'мне', u'всём', u'что', u'всей')):
        return properties.clone(r.PREPOSITION_FORM.SPECIAL)

    # Если существительное начинается на гласную (кроме йотированных), то пишем ОБ: сообщить об отъезде, удариться об асфальт. Это фонетический принцип.
    if master[0] in data.NOT_J_VOWELS:
        return properties.clone(r.PREPOSITION_FORM.ALTERNATIVE)

    # Прелоги участвуют в управлении В.п. или П.п. Для В.п. характерен предлог ОБ: удариться об дерево, об стену,
    # а для П.п. - предлог О: думать о дереве, о стене. Это грамматический принцип.
    # TODO

    return properties



def _noun_integer(properties, slave_word=None, master_form=None):
    # http://www.pf.ujep.cz/files/KBO/Nazarenko/cvicebnice_3_4/page34.html

    integer_form = properties.get(r.INTEGER_FORM)

    if properties.get(r.DEPENDENCY_MODE).is_SEMANTIC:
        if integer_form.is_SINGULAR:
            return properties.clone(r.NOUN_FORM.NORMAL, r.NUMBER.SINGULAR)
        else:
            return properties.clone(r.NOUN_FORM.NORMAL, r.NUMBER.PLURAL)

    case = properties.get(r.CASE)
    animality = properties.get(r.ANIMALITY)

    # Числительное один (одна, одно) согласуется с существительным в роде, числе и падеже
    # (ср.: один день, одним днем, в одну неделю и т.д.).
    if integer_form.is_SINGULAR:
        return properties.clone(r.NOUN_FORM.NORMAL, r.NUMBER.SINGULAR)

    # Числительные два, три, четыре в форме И.п. (и В. п. при неодушевленных существительных)
    # управляют формой Р.п. единственного числа существительных: два дня, два товарища, три окна.
    # В остальных падежах эти числительные согласуются с существительными во множественном числе:
    if integer_form.is_DUAL:
        if case.is_NOMINATIVE:
            return properties.clone(r.NOUN_FORM.NORMAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE)
        if case.is_ACCUSATIVE and animality.is_INANIMATE:
            return properties.clone(r.NOUN_FORM.NORMAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE)
        return properties.clone(r.NOUN_FORM.COUNTABLE, r.NUMBER.PLURAL)

    # Составные числительные, оканчивающиеся на два, три, четыре, управляют в И.п. и В.п. формой Р.п. единственного числа существительных
    # (ср.: надо купить двадцать два компьютера, я вижу двадцать два студента. Но: я вижу двух студентов).
    # В остальных падежах эти числительные согласуются с существительными во множественном числе.
    if integer_form.is_COMPOSITE_DUAL:
        if case.is_NOMINATIVE:
            return properties.clone(r.NOUN_FORM.NORMAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE)
        if case.is_ACCUSATIVE:
            return properties.clone(r.NOUN_FORM.NORMAL, r.NUMBER.SINGULAR, r.CASE.GENITIVE)
        return properties.clone(r.NOUN_FORM.COUNTABLE, r.NUMBER.PLURAL)

    # Названные составные числительные не сочетаются с существительными, употребляемыми только во множественном числе.
    # В таких случаях используется конструкция со словом штука или пара (в сочетании с парными предметами) : двадцать две штуки саней или три пары лыж.
    # TODO


    # Числительные, начиная от пяти и далее  в И.-В. п. управляют формой Р.п. множественного числа существительных:
    # (пять учеников, сто журналов, девять студенток, шесть окон), а в остальных падежах – согласуются с существительными во множественном числе
    # (пятью учениками, ста журналами, на шести окнах).
    if integer_form.is_PLURAL:
        if case.is_NOMINATIVE:
            return properties.clone(r.NOUN_FORM.COUNTABLE, r.NUMBER.PLURAL, r.CASE.GENITIVE)
        if case.is_ACCUSATIVE:
            return properties.clone(r.NOUN_FORM.COUNTABLE, r.NUMBER.PLURAL, r.CASE.GENITIVE)
        return properties.clone(r.NOUN_FORM.COUNTABLE, r.NUMBER.PLURAL)

    # Слова миллион, миллиард во всех падежах управляют существительными в родительном падеже множественного числа
    # (миллион жителей, миллиона жителей, миллионам жителей).
    if integer_form.is_MIL_BIL:
        return properties.clone(r.NOUN_FORM.COUNTABLE, r.NUMBER.PLURAL, r.CASE.GENITIVE)


    # Определения, выраженные словами последний, первый, второй, каждый, другой употребляются в форме И.-В.п. мн. числа и обычно стоят перед числительным
    # (последние два экзамена, первые два шага, каждые два часа и т.п.).
    # TODO

    raise exceptions.UnknownIntegerFormError(form=integer_form)


def _adjective_integer(properties, slave_word=None, master_form=None):
    # http://www.pf.ujep.cz/files/KBO/Nazarenko/cvicebnice_3_4/page34.html

    integer_form = properties.get(r.INTEGER_FORM)

    if properties.get(r.DEPENDENCY_MODE).is_SEMANTIC:
        if integer_form.is_SINGULAR:
            return properties.clone(r.NUMBER.SINGULAR)
        else:
            return properties.clone(r.NUMBER.PLURAL)

    case = properties.get(r.CASE)
    gender = properties.get(r.GENDER)

    # Числительное один (одна, одно) согласуется с существительным в роде, числе и падеже
    # (ср.: один день, одним днем, в одну неделю и т.д.).
    if integer_form.is_SINGULAR:
        return properties.clone(r.NUMBER.SINGULAR)

    # Субстантивированные прилагательные мужского и среднего рода в сочетании с числительными два, три, четыре употребляются в форме Р.п. мн.ч.
    # (ср.: два дежурных, три насекомых), а субстантивированные прилагательные женского рода - в форме Р. или И.-В. п. множественного числа
    # (ср.: две запятых - две запятые и т.п.).
    #
    # Прилагательное-определение к существительному мужского и среднего рода в сочетаниях с числительными два, три, четыре употребляется в форме Р.п. мн. числа:
    # два новых телефона, три больших поля.
    # При именах существительных женского рода прилагательные-определения могут употребляться как в форме И.-В.п., так и в форме Р.п. мн. числа:
    # две новые книги, две новых книги. Первая форма более употребительна.
    if integer_form.is_DUAL:
        if case.is_NOMINATIVE or case.is_ACCUSATIVE:
            if gender.is_MASCULINE or gender.is_NEUTER:
                return properties.clone(r.NUMBER.PLURAL, r.CASE.GENITIVE)

            if gender.is_FEMININE:
                return properties.clone(r.NUMBER.PLURAL, r.CASE.NOMINATIVE)
        else:
            return properties.clone(r.NUMBER.PLURAL)

    # Составные числительные, оканчивающиеся на два, три, четыре, управляют в И.п. и В.п. формой Р.п. единственного числа существительных
    # (ср.: надо купить двадцать два компьютера, я вижу двадцать два студента. Но: я вижу двух студентов).
    # В остальных падежах эти числительные согласуются с существительными во множественном числе.
    if integer_form.is_COMPOSITE_DUAL:
        if case.is_NOMINATIVE:
            return properties.clone(r.NUMBER.SINGULAR, r.CASE.GENITIVE)
        if case.is_ACCUSATIVE:
            return properties.clone(r.NUMBER.SINGULAR, r.CASE.GENITIVE)
        return properties.clone(r.NUMBER.PLURAL)

    # Названные составные числительные не сочетаются с существительными, употребляемыми только во множественном числе.
    # В таких случаях используется конструкция со словом штука или пара (в сочетании с парными предметами) : двадцать две штуки саней или три пары лыж.
    # TODO

    # Числительные, начиная от пяти и далее  в И.-В. п. управляют формой Р.п. множественного числа существительных:
    # (пять учеников, сто журналов, девять студенток, шесть окон), а в остальных падежах – согласуются с существительными во множественном числе
    # (пятью учениками, ста журналами, на шести окнах).
    if integer_form.is_PLURAL:
        if case.is_NOMINATIVE:
            return properties.clone(r.NUMBER.PLURAL, r.CASE.GENITIVE)
        if case.is_ACCUSATIVE:
            return properties.clone(r.NUMBER.PLURAL, r.CASE.GENITIVE)
        return properties.clone(r.NUMBER.PLURAL)

   # Слова миллион, миллиард во всех падежах управляют существительными в родительном падеже множественного числа
    # (миллион жителей, миллиона жителей, миллионам жителей).
    if integer_form.is_MIL_BIL:
        return properties.clone(r.NUMBER.PLURAL, r.CASE.GENITIVE)

    # Определения, выраженные словами последний, первый, второй, каждый, другой употребляются в форме И.-В.п. мн. числа и обычно стоят перед числительным
    # (последние два экзамена, первые два шага, каждые два часа и т.п.).
    # TODO

    raise exceptions.UnknownIntegerFormError(form=integer_form)


_TRANSFORMATORS = {(r.WORD_TYPE.NOUN, r.WORD_TYPE.INTEGER): _noun_integer,
                   (r.WORD_TYPE.ADJECTIVE, r.WORD_TYPE.INTEGER): _adjective_integer,
                   (r.WORD_TYPE.VERB, r.WORD_TYPE.INTEGER): _adjective_integer,
                   (r.WORD_TYPE.PRONOUN, r.WORD_TYPE.INTEGER): _noun_integer,
                   (r.WORD_TYPE.PARTICIPLE, r.WORD_TYPE.INTEGER): _adjective_integer}

for word_type in r.WORD_TYPE.records:
    _TRANSFORMATORS[(r.WORD_TYPE.PREPOSITION, word_type)] = _preposition_any
