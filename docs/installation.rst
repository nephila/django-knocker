============
Installation
============

* Install it

    $ pip install django-knocker

* Add it to ``INSTALLED_APPS`` with channels::

    INSTALLED_APPS = [
        ...
        'channels,
        'knocker',
        ...
    ]

* Load the ``knocker`` routing into channels configuration::

    CHANNEL_LAYERS={
        'default': {
            'BACKEND': 'asgi_redis.RedisChannelLayer',
            'CONFIG': {
                'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
            },
            'ROUTING': 'myproject.routing.channel_routing',
        },
    }

  Check `channels documentation`_ for more detailed information on ``CHANNEL_LAYERS`` setup.

.. _channels documentation: https://channels.readthedocs.io/en/latest/deploying.html

* Add to ``myproject.routing.channel_routing.py`` the knocker routes::

    # -*- coding: utf-8 -*-

    from channels import include
    from knocker.routing import channel_routing as knocker_routing

    channel_routing = [
        include(knocker_routing, path=r'^/notifications'),
    ]
