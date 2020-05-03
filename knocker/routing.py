# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels.routing import URLRouter
from django.urls import path

from .consumers import KnockerConsumer

# consumers can be freely appended: path ensure the correct match
channel_routing = URLRouter([
    path('notification/<str:language>/', KnockerConsumer),
])
