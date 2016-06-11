# -*- coding: utf-8 -*-
from channels.routing import include
from knocker.routing import channel_routing


routing = [
    include(include(channel_routing), path=r'^/knocker')
]
