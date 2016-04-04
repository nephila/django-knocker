# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.utils.translation import get_language, override


def notify_items(**kwargs):
    """
    Signal endpoint that actually sends knocks whenever an instance is created / saved
    """
    instance = kwargs.get('instance')
    created = kwargs.get('created', False)
    if hasattr(instance, 'send_knock'):
        try:
            # This is a stupid generic interface for multilanguage models (hvad / parler)
            if hasattr(instance, 'get_available_languages'):
                langs = instance.get_available_languages()
            else:
                langs = [get_language()]
            for lang in langs:
                with override(lang):
                    instance.send_knock(created)
        except AttributeError:  # pragma: no cover
            pass
