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


def _get_caches(schema, restrictions):
    cache = {}
    inverted_cache = []

    for i, key in enumerate(_keys_generator([], schema, restrictions=restrictions)):
        _populate_key_with_presets(key, schema)
        cache[tuple(key)] = i
        inverted_cache.append(tuple(key))

    return cache, inverted_cache


def _populate_key_with_presets(key, schema):
    from utg.data import PRESETS

    replaces = {}

    for property in key:
        if property not in PRESETS:
            continue

        replace = PRESETS[property]
        replaces[replace._relation] = replace

    if not replaces:
        return

    for index, property_group in enumerate(schema):
        if property_group in replaces:
            key[index] = replaces[property_group]


def get_caches(restrictions):

    caches = {}
    inverted_caches = {}

    for word in r.WORD_TYPE.records:
        cache, inverted_cache = _get_caches(word.schema, restrictions)

        caches[word] = cache
        inverted_caches[word] = inverted_cache


    return caches, inverted_caches


def get_nearest_key(key, available_keys):
    best_key = None
    best_similarity = -1

    for available_key in available_keys:
        current_similarity = 0
        for index, (key_property, available_key_property) in enumerate(zip(key, available_key)):
            if key_property == available_key_property:
                current_similarity += (1 + 0.01 * index) # first elements in schema has less priority

        if current_similarity > best_similarity:
            best_similarity = current_similarity
            best_key = available_key

    return best_key
