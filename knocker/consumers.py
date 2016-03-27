# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels import Group
from channels.sessions import channel_session


@channel_session
def ws_connect(message):
    """
    Channels connection setup.
    Register the current client on the related Group according to the language
    """
    prefix, language = message['path'].strip('/').split('/')
    gr = Group('knocker-{0}'.format(language))
    gr.add(message.reply_channel)
    message.channel_session['knocker'] = language


@channel_session
def ws_receive(message):
    """
    Currently no-op
    """
    pass


@channel_session
def ws_disconnect(message):
    """
    Channels connection close.
    Deregister the client
    """
    language = message.channel_session['knocker']
    gr = Group('knocker-{0}'.format(language))
    gr.discard(message.reply_channel)
