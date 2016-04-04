#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os

from tempfile import mkdtemp

HELPER_SETTINGS = dict(
    ROOT_URLCONF='tests.example_app.urls',
    INSTALLED_APPS=[
        'channels',
        'tests.example_app',
    ],
    LANGUAGES=(
        ('en', 'English'),
        ('fr', 'French'),
        ('it', 'Italiano'),
    ),
    PARLER_LANGUAGES={
        1: (
            {'code': 'en'},
            {'code': 'it'},
            {'code': 'fr'},
        ),
        2: (
            {'code': 'en'},
        ),
        'default': {
            'fallbacks': ['en'],
            'hide_untranslated': False,
        }
    },
    FILE_UPLOAD_TEMP_DIR=mkdtemp(),
    CHANNEL_LAYERS={
        'default': {
            'BACKEND': 'asgi_redis.RedisChannelLayer',
            'CONFIG': {
                'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
            },
            'ROUTING': 'knocker.routing.channel_routing',
        },
    }
)


def run():
    from djangocms_helper import runner
    runner.run('knocker')


def setup():
    import sys
    from djangocms_helper import runner
    runner.setup('knocker', sys.modules[__name__], use_cms=False)

if __name__ == "__main__":
    run()
