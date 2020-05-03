# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json

import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.utils.text import slugify
from tests.example_app.models import NoKnockPost, Post
from tests.example_app.routing import application


@pytest.mark.asyncio
async def test_consumer_connect():
    communicator = WebsocketCommunicator(application, "/knocker/notification/en/")
    connected, __ = await communicator.connect()
    assert connected
    assert await communicator.receive_nothing() is True
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_consumer_notification():
    @database_sync_to_async
    def get_post(title):
        return Post.objects.create(
            title=title,
            slug=slugify(title),
        )

    @database_sync_to_async
    def get_noknock_post(title):
        return NoKnockPost.objects.create(
            title=title,
            slug=slugify(title),
        )

    communicator = WebsocketCommunicator(application, "/knocker/notification/en/")
    await communicator.connect()

    # Post type which return notifications
    post = await get_post('first post')
    notification = json.loads(await communicator.receive_json_from())
    assert notification['title'] == 'new {0}'.format(post._meta.verbose_name)
    assert notification['message'] == post.title
    assert notification['url'] == post.get_absolute_url()

    # Post type without notifications
    await get_noknock_post('first post')
    assert await communicator.receive_nothing() is True
    await communicator.disconnect()
