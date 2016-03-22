# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json

from channels import Group
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from .signals import notify_items  # NOQA


class KnockerModel(object):

    _knocker_data = {
        'title': 'get_knocker_title',
        'message': 'get_title',
        'icon': 'get_knocker_icon',
        'language': 'get_current_language',
    }

    def __init__(self, *args, **kwargs):
        super(KnockerModel, self).__init__(*args, **kwargs)
        post_save.connect(notify_items, sender=self.__class__)

    def get_knocker_icon(self):
        return getattr(settings, 'KNOCKER_ICON_URL', '')

    def get_knocker_title(self):
        return force_text(_('new {0}'.format(self._meta.verbose_name)))

    def should_knock(self, created):
        return True

    def as_knock(self, created):
        knock = {}
        if self.should_knock(created):
            for field, data in self._retrieve_data(None, self._knocker_data):
                knock[field] = data
        return knock

    def send_knock(self, created):
        knock = self.as_knock(created)
        if knock:
            gr = Group('knocker-{0}'.format(knock['language']))
            gr.send({'text': json.dumps(knock)})
