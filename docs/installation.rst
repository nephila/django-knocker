============
Installation
============

* Install it

    $ pip install django-knocker

* Add it to ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
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
            'ROUTING': 'knocker.routing.channel_routing',
        },
    }

