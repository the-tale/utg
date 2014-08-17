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


def _keys_generator(schema, restrictions):

    if not schema:
        yield []
        return

    for head in schema[0].records:
        for tail in _keys_generator(schema[1:], restrictions):
            if any((head, tail_property) in restrictions for tail_property in tail):
                continue
            yield [head] + tail

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

    full_restrictions = _get_full_restrictions(restrictions)

    caches = {}
    inverted_caches = {}

    for word in r.WORD_TYPE.records:
        cache = {}
        inverted_cache = []

        caches[word] = cache
        inverted_caches[word] = inverted_cache

        for i, key in enumerate(_keys_generator(word.schema, restrictions=full_restrictions)):
            cache[tuple(key)] = i
            inverted_cache.append(tuple(key))

    return caches, inverted_caches
