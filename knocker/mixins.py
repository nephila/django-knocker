# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json

from channels import Group
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.encoding import force_text
from django.utils.translation import get_language, ugettext_lazy as _

from .signals import notify_items  # NOQA


class KnockerModel(object):

    _knocker_data = {
        'title': 'get_knocker_title',
        'message': 'get_knocker_message',
        'icon': 'get_knocker_icon',
        'url': 'get_absolute_url',
        'language': 'get_knocker_language',
    }

    def __init__(self, *args, **kwargs):
        super(KnockerModel, self).__init__(*args, **kwargs)
        self._connect()

    def _connect(self):
        """
        Connect signal to current model
        """
        post_save.connect(
            notify_items, sender=self.__class__,
            dispatch_uid='knocker_{0}'.format(self.__class__.__name__)
        )

    def _disconnect(self):
        """
        Disconnect signal from current model
        """
        post_save.disconnect(
            notify_items, sender=self.__class__,
            dispatch_uid='knocker_{0}'.format(self.__class__.__name__)
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
        return force_text(_('new {0}'.format(self._meta.verbose_name)))

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

    def should_knock(self, created=False):
        """
        Generic function to tell whether a knock should be emitted.

        Override this to avoid emitting knocks under specific circumstances (e.g.: if the object
        has just been created or update)

        :param created: True if the object has been created
        """
        return True

    def as_knock(self, created=False):
        """
        Returns a dictionary with the knock data built from _knocker_data
        """
        knock = {}
        if self.should_knock(created):
            for field, data in self._retrieve_data(None, self._knocker_data):
                knock[field] = data
        return knock

    def send_knock(self, created=False):
        """
        Send the knock in the associated channels Group
        """
        knock = self.as_knock(created)
        if knock:
            gr = Group('knocker-{0}'.format(knock['language']))
            gr.send({'text': json.dumps(knock)})
