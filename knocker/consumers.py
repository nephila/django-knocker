# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels.generic.websocket import JsonWebsocketConsumer


class KnockerConsumer(JsonWebsocketConsumer):

    @property
    def groups(self):
        """
        Attach the consumer to the selected language
        """
        lang = self.scope['url_route']['kwargs'].get('language')
        return 'knocker-%s' % lang,

    def knocker_saved(self, event):
        """
        This method handles messages sent to knocker.saved

        :param event: event object
        """
        self.send_json(content=event['message'])
