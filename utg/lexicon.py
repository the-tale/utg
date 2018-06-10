
import random

from utg import exceptions


class Lexicon(object):
    __slots__ = ('_data',)

    def __init__(self):
        self._data = {}

    def add_template(self, key, template, restrictions=frozenset()):
        if key not in self._data:
            self._data[key] = []

        self._data[key].append((template, restrictions))

    def has_key(self, key):
        return key in self._data

    def get_templates(self, key, restrictions):
        templates = tuple(template
                          for template, template_restrictions in self._data.get(key, ())
                          if template_restrictions.issubset(restrictions))

        return templates

    def get_random_template(self, key, restrictions=frozenset()):
        if key not in self._data:
            raise exceptions.UnknownLexiconKeyError(key=key)

        candidates = self.get_templates(key, restrictions)

        if not candidates:
            raise exceptions.NoTemplatesWithSpecifiedRestrictions(key=key, restrictions=restrictions)

        return random.choice(candidates)

    def _get_nearest_templates(self, key, restrictions):
        templates = []

        best_distance = -1

        for template, template_restrictions in self._data.get(key, ()):
            if not template_restrictions.issubset(restrictions):
                continue

            distance = len(template_restrictions & restrictions)

            if best_distance < distance:
                best_distance = distance

            templates.append((template, distance))

        return [template for template, distance in templates if distance == best_distance]

    def get_random_nearest_template(self, key, restrictions=frozenset()):
        if key not in self._data:
            raise exceptions.UnknownLexiconKeyError(key=key)

        candidates = self._get_nearest_templates(key, restrictions)

        if not candidates:
            raise exceptions.NoTemplatesWithSpecifiedRestrictions(key=key, restrictions=restrictions)

        return random.choice(candidates)
