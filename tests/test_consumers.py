# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels.test import ChannelTestCase, WSClient
from tests.example_app.models import MultiLanguagePost, NoKnockPost, Post


class KnockerConsumerTest(ChannelTestCase):

    def tearDown(self):
        MultiLanguagePost._disconnect()
        Post._disconnect()
        super(KnockerConsumerTest, self).tearDown()

    def test_connect(self):
        client = WSClient()

        client.send_and_consume('websocket.connect', path='/knocker/en/')
        self.assertIsNone(client.receive())

    def test_notification(self):
        client = WSClient()

        client.send_and_consume('websocket.connect', path='/knocker/en/')
        post = Post.objects.create(
            title='first post',
            slug='first-post',
        )
        notification = client.receive()
        self.assertEqual(notification['title'], 'new {0}'.format(post._meta.verbose_name))
        self.assertEqual(notification['message'], post.title)
        self.assertEqual(notification['url'], post.get_absolute_url())

        # This model does not send notifications
        NoKnockPost.objects.create(
            title='first post',
            slug='first-post',
        )
        self.assertIsNone(client.receive())
