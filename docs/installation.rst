============
Installation
============

* Install it:

  .. code-block:: bash

      pip install django-knocker

* Add it to ``INSTALLED_APPS`` with channels:

  .. code-block:: python

      INSTALLED_APPS = [
          ...
          'channels,
          'knocker',
          ...
      ]

* Load the ``knocker`` routing into channels configuration:

  .. code-block:: python

      CHANNEL_LAYERS={
          'default': {
              'BACKEND': 'channels_redis.core.RedisChannelLayer',
              'CONFIG': {
                  'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
              }
          },
      }

      ASGI_APPLICATION='myproject.routing.channel_routing',

  Check `channels documentation`_ for more detailed information on ``CHANNEL_LAYERS`` setup.

.. _channels documentation: https://channels.readthedocs.io/en/latest/deploying.html

* Add to ``myproject.routing.channel_routing.py`` the knocker routes:

  .. code-block:: python

      # -*- coding: utf-8 -*-

      from channels.auth import AuthMiddlewareStack
      from channels.routing import ProtocolTypeRouter, URLRouter
      from django.urls import path
      from knocker.routing import channel_routing as knocker_routing

      application = ProtocolTypeRouter({
          'websocket': AuthMiddlewareStack(
              URLRouter([
                  path('knocker/', knocker_routing),
              ])
          ),
      })


.. _upgrade:


Upgrade
=======

Upgrade from channels 1 version of django-knocker require updating the configuration and minor changes

Configuration
-------------

* Discard existing configuration
* Rewrite the main router according to channels 2 specifications and include knocker router. Example:

  .. code-block:: python

      application = ProtocolTypeRouter({
          'websocket': AuthMiddlewareStack(
              URLRouter([
                  path('knocker/', knocker_routing),
              ])
          ),
      })



API Changes
-----------

If you added a custom ``should_knock`` method, you must add the ``signal_type`` argument to match the current signature:

.. code-block::  python

   def should_knock(self, signal_type, created=False):
       ...
