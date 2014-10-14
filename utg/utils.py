# coding: utf-8
import functools


def lazy_property(func):

    lazy_name = '_lazy__%s' % func.__name__

    @functools.wraps(func)
    def getter(self):
        if not hasattr(self, lazy_name):
            setattr(self, lazy_name, func(self))
        return getattr(self, lazy_name)

    def deleter(self):
        if hasattr(self, lazy_name):
            delattr(self, lazy_name)

    return property(fget=getter, fdel=deleter)
