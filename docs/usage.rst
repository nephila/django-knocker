=====
Usage
=====

After installing and configuring it, you need to adapt your models to use ``knocker`` interface.

* Extend your model to use ``KnockerModel`` and ``ModelMeta``

* Override  the `api`_ if needed

* Load ``{% static "js/knocker.js" %}`` and ``{% static "js/reconnecting-websocket.min" %}`` into
  the templates

* Deploy you project according to the `channels documentation`_

Now, for every user which has of the knocker-enabled pages opened, whenever an instance of your
knocker-enabled models is saved, a desktop notification is emitted.

.. _api:

===========
Knocker API
===========

The Knocker API is a very thin layer of syntactic sugar on top of `django-meta`_ and `channels`_.

Attributes
----------

``KnockerModel`` mixin defines the attribute to build the notification information::

    _knocker_data = {
        'title': 'get_knocker_title',
        'message': 'get_knocker_message',
        'icon': 'get_knocker_icon',
        'url': 'get_absolute_url',
        'language': 'get_knocker_language',
    }

Each key in the ``_knocker_data`` attribute is an attribute of the notification package
delivered to the client. Each key can be overridden in the ``__init__`` method or the attribute
entirely redefined in the model class::


    class Post(KnockerModel, ModelMeta, models.Model):
        title = models.CharField(_('Title'), max_length=255)
        ...

        _knocker_data = {
            'title': 'get_my_title',
            'message': 'get_message',
            'icon': 'get_knocker_icon',
            'url': 'get_absolute_url',
            'language': 'get_knocker_language',
        }

        def get_message(self):
            return self.title

        def get_my_message(self):
            return 'hello'

Attributes
##########

* title: the title that appears in the desktop notification; defaults to
  ``New Model verbose name``;
* message: the content of the desktop notification; default to the result of ``self.get_title``
  on the model instance;
* icon: an icon displayed on the notification; defaults to the value of ``KNOCKER_ICON_URL``;
* url: the url the notification is linked to; default to the model ``get_absolute_url``;
* language: the language group the notification is sent; if the model uses `django-parler`_ or
  `django-hvad`_ the language of the instance is determined by calling
  ``self.get_current_language()``, otherwise the current django language is used.

Methods
-------

``django-knocker`` defines a few methods that are intended to be overridden in the models


.. autoclass:: knocker.mixins.KnockerModel
    :members: should_knock, get_knocker_language, get_knocker_message, get_knocker_icon, get_knocker_title


.. _django-hvad: https://github.com/KristianOellegaard/django-hvad
.. _django-parler: https://github.com/edoburu/django-parler
.. _django-meta: https://github.com/nephila/django-meta
.. _channels: https://github.com/andrewgodwin/channels
.. _channels documentation: https://channels.readthedocs.io/en/latest/deploying.html
