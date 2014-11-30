# coding: utf-8

import random

from utg import exceptions


class Lexicon(object):
    __slots__ = ('_data', '_restrictions_cache')

    def __init__(self):
        self._data = {}
        self._restrictions_cache = {}


    def add_template(self, key, template, restrictions=frozenset()):
        if key not in self._data:
            self._data[key] = []

        self._data[key].append((template, restrictions))

    def has_key(self, key):
        return key in self._data


    def get_templates(self, key, restrictions):
        cache_key = (key, restrictions)

        if cache_key in self._restrictions_cache:
            return self._restrictions_cache[cache_key]

        templates = [template
                     for template, template_restrictions in self._data.get(key, ())
                     if template_restrictions.issubset(restrictions)]

        self._restrictions_cache[cache_key] = templates

        return templates


    def get_random_template(self, key, restrictions=frozenset()):
        if key not in self._data:
            raise exceptions.UnknownLexiconKeyError(key=key)

        candidates = self.get_templates(key, restrictions)

        if not candidates:
            raise exceptions.NoTemplatesWithSpecifiedRestrictions(key=key, restrictions=restrictions)

        return random.choice(candidates)
