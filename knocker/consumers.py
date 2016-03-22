# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels import Group
from channels.sessions import channel_session


@channel_session
def ws_connect(message):
    prefix, language = message['path'].strip('/').split('/')
    gr = Group('knocker-{0}'.format(language))
    gr.add(message.reply_channel)
    message.channel_session['knocker'] = language
    print(gr.channel_layer._group_channels(gr.name))


@channel_session
def ws_receive(message):
    pass


@channel_session
def ws_disconnect(message):
    language = message.channel_session['knocker']
    gr = Group('knocker-{0}'.format(language))
    print(gr.channel_layer._group_channels(gr.name))
    gr.discard(message.reply_channel)
