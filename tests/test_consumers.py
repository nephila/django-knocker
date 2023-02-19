import json

import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.utils.text import slugify

from tests.example_app.models import NoKnockPost, Post
from tests.example_app.routing import application


async def _connect():
    path = "knocker/notification/en/"
    communicator = WebsocketCommunicator(application, path)
    connected, __ = await communicator.connect()
    assert connected
    assert await communicator.receive_nothing() is True
    return communicator


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

    communicator = await _connect()

    # Post type without notifications
    await get_noknock_post("first post")
    assert await communicator.receive_nothing() is True

    # Post type which return notifications
    post = await get_post("first post")
    data = await communicator.receive_json_from()
    notification = json.loads(data)
    assert notification["title"] == "new {}".format(post._meta.verbose_name)
    assert notification["message"] == post.title
    assert notification["url"] == post.get_absolute_url()

    await communicator.disconnect()
