# coding: utf-8
import functools


def cached_property(cache_attribute):

    def decorator(func):

        @functools.wraps(func)
        def getter(self):
            cache = getattr(self, cache_attribute)
            key = func.__name__

            if key in cache:
                return cache[key]

            value = func(self)

            cache[key] = value

            return value

        return property(fget=getter)

    return decorator
