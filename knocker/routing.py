# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from . import consumers

channel_routing = {
    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_receive,
    'websocket.disconnect': consumers.ws_disconnect,
}
