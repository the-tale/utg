# coding: utf-8

from utg import relations as r


def get_property_relations():
    return [relation
            for relation in r.__dict__.itervalues()
            if relation != r.WORD_PROPERTY and isinstance(relation, type) and issubclass(relation, r.WORD_PROPERTY)]


def get_default_properties():
    values = {}

    for relation in get_property_relations():
        values[relation] = relation.records[0]

    values[r.WORD_TYPE] = None

    return values

def get_verbose_to_relations():
    values = {}

    for relation in get_property_relations():
        for record in relation.records:
            values[record.verbose_id] = record

    return values


def _keys_generator(left, right, restrictions):

    if not right:
        yield []
        return

    central, right = right[0], right[1:]

    for used_property in left:
        if used_property in restrictions and central in restrictions[used_property]:
            for tail in _keys_generator(left + [None], right, restrictions):
                yield [None] + tail
            return

    for record in central.records:
        for tail in _keys_generator(left + [record], right, restrictions):
            yield [record] + tail

    return


def _get_full_restrictions(restrictions):
    full_restrictions = set()

    for property_1, groups in restrictions.iteritems():
        for group in groups:
            for property_2 in group.records:
                full_restrictions.add((property_1, property_2))
                full_restrictions.add((property_2, property_1))

    return full_restrictions


def get_caches(restrictions):

    caches = {}
    inverted_caches = {}

    for word in r.WORD_TYPE.records:
        cache = {}
        inverted_cache = []

        caches[word] = cache
        inverted_caches[word] = inverted_cache

        for i, key in enumerate(_keys_generator([], word.schema, restrictions=restrictions)):
            cache[tuple(key)] = i
            inverted_cache.append(tuple(key))

    return caches, inverted_caches
