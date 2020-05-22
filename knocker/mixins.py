# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import contextlib
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.utils.encoding import force_str
from django.utils.translation import get_language, gettext_lazy as _

from .signals import notify_items_post_delete  # NOQA
from .signals import notify_items_post_save, notify_items_pre_delete, notify_items_pre_save


class KnockerModel(object):

    _knocker_data = {
        'title': 'get_knocker_title',
        'message': 'get_knocker_message',
        'icon': 'get_knocker_icon',
        'url': 'get_absolute_url',
        'language': 'get_knocker_language',
    }

    def __new__(cls, *args, **kwargs):
        new_cls = object.__new__(cls)
        new_cls._connect()
        return new_cls

    @classmethod
    def _connect(cls):
        """
        Connect signal to current model
        """
        pre_save.connect(
            notify_items_pre_save, sender=cls,
            dispatch_uid='knocker_pre_save_{0}'.format(cls.__name__)
        )
        post_save.connect(
            notify_items_post_save, sender=cls,
            dispatch_uid='knocker_post_save_{0}'.format(cls.__name__)
        )
        pre_delete.connect(
            notify_items_pre_delete, sender=cls,
            dispatch_uid='knocker_pre_delete_{0}'.format(cls.__name__)
        )
        post_delete.connect(
            notify_items_post_delete, sender=cls,
            dispatch_uid='knocker_post_delete_{0}'.format(cls.__name__)
        )

    @classmethod
    def _disconnect(cls):
        """
        Disconnect signal from current model
        """
        pre_save.disconnect(
            notify_items_pre_save, sender=cls,
            dispatch_uid='knocker_pre_save_{0}'.format(cls.__name__)
        )
        post_save.disconnect(
            notify_items_post_save, sender=cls,
            dispatch_uid='knocker_post_save_{0}'.format(cls.__name__)
        )
        pre_delete.disconnect(
            notify_items_pre_delete, sender=cls,
            dispatch_uid='knocker_pre_delete_{0}'.format(cls.__name__)
        )
        post_delete.disconnect(
            notify_items_post_delete, sender=cls,
            dispatch_uid='knocker_post_delete_{0}'.format(cls.__name__)
        )

    def get_knocker_icon(self):
        """
        Generic function to return the knock icon

        Defaults to the value of settings.KNOCKER_ICON_URL
        """
        return getattr(settings, 'KNOCKER_ICON_URL', '')

    def get_knocker_title(self):
        """
        Generic function to return the knock title.

        Defaults to 'new `model_verbose_name`'
        """
        signal_type = self._get_signal_type()
        titles = {
            'post_save': force_str(_('new {0}'.format(self._meta.verbose_name))),
            'post_delete': force_str(_('deleted {0}'.format(self._meta.verbose_name)))
        }
        return titles[signal_type]

    def get_knocker_message(self):
        """
        Generic function to return the knock message.

        Defaults to calling ``self.get_title``
        """
        return self.get_title()

    def get_knocker_language(self):
        """
        Returns the current language.

        This will call ``selg.get_current_language`` if available or the Django
        ``django.utils.translation.get_language()`` otherwise
        """
        if hasattr(self, 'get_current_language'):
            return self.get_current_language()
        else:
            return get_language()

    def should_knock(self, signal_type, created=False):
        """
        Generic function to tell whether a knock should be emitted.

        Override this to avoid emitting knocks under specific circumstances (e.g.: if the object
        has just been created or update)

        :param signal_type: type of signal between pre_save, post_save, pre_delete, post_delete
        :param created: True if the object has been created
        """
        should = {
            'pre_save': False,
            'pre_delete': False,
            'post_save': True,
            'post_delete': True,
        }
        return should[signal_type]

    @contextlib.contextmanager
    def _set_signal_type(self, signal_type):
        """
        Context processor that sets the signal_type on the current instance

        :param signal_type: name of the catched signal
        """
        self._signal_type = signal_type
        yield
        delattr(self, '_signal_type')

    def _get_signal_type(self):
        """
        Retrieve the signal type from the current instance

        :return: string
        """
        return getattr(self, '_signal_type', '')

    def as_knock(self, signal_type, created=False):
        """
        Returns a dictionary with the knock data built from _knocker_data
        """
        knock = {}
        if self.should_knock(signal_type, created):
            with self._set_signal_type(signal_type):
                for field, data in self._retrieve_data(None, self._knocker_data):
                    knock[field] = data
                knock['action'] = created if created else signal_type.split('_')[1]
        return knock

    def send_knock(self, signal_type, created=False):
        """
        Send the knock in the associated channels Group
        """
        knock = self.as_knock(signal_type, created)
        if knock:
            channel_layer = get_channel_layer()
            group = 'knocker-%s' % knock['language']
            async_to_sync(channel_layer.group_send)(group, {
                'type': 'knocker.saved',
                'message': json.dumps(knock)
            })
