# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from contextlib import contextmanager

from asgiref.local import Local
from django.utils.translation import get_language, override

_thread_locals = Local()


def notify_items_pre_save(**kwargs):
    return notify_items(signal_type='pre_save', **kwargs)


def notify_items_post_save(**kwargs):
    return notify_items(signal_type='post_save', **kwargs)


def notify_items_pre_delete(**kwargs):
    return notify_items(signal_type='pre_delete', **kwargs)


def notify_items_post_delete(**kwargs):
    return notify_items(signal_type='post_delete', **kwargs)


def notify_items(signal_type, **kwargs):
    """
    Signal endpoint that actually sends knocks whenever an instance is created / saved
    """
    instance = kwargs.get('instance')
    created = kwargs.get('created', False)
    if hasattr(instance, 'send_knock') and active_knocks(instance):
        try:
            # This is a stupid generic interface for multilanguage models (hvad / parler)
            if hasattr(instance, 'get_available_languages'):
                langs = instance.get_available_languages()
            else:
                langs = [get_language()]
            for lang in langs:
                with override(lang):
                    instance.send_knock(signal_type, created)
            return True
        except AttributeError:  # pragma: no cover
            pass
    return False


def active_knocks(obj):
    """
    Checks whether knocks are enabled for the model given as argument

    :param obj: model instance
    :return True if knocks are active
    """
    if not hasattr(_thread_locals, 'knock_enabled'):
        return True
    return _thread_locals.knock_enabled.get(obj.__class__, True)


@contextmanager
def pause_knocks(obj):
    """
    Context manager to suspend sending knocks for the given model

    :param obj: model instance
    """
    if not hasattr(_thread_locals, 'knock_enabled'):
        _thread_locals.knock_enabled = {}
    obj.__class__._disconnect()
    _thread_locals.knock_enabled[obj.__class__] = False
    yield
    _thread_locals.knock_enabled[obj.__class__] = True
    obj.__class__._connect()
