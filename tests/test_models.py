# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.db.models.signals import post_save
from django.utils.translation import get_language, override
from mock import patch
from parler.utils.context import smart_override

from knocker.signals import active_knocks, pause_knocks

from .base import BaseKnocker
from .example_app.models import MultiLanguagePost, NoKnockPost, Post


class KnockerTest(BaseKnocker):

    def tearDown(self):
        MultiLanguagePost._disconnect()
        Post._disconnect()
        super(KnockerTest, self).tearDown()

    def test_model_attributes(self):
        posts = []
        posts.append(MultiLanguagePost.objects.create(
            title='first post',
            slug='first-post',
        ))
        posts.append(MultiLanguagePost.objects.create(
            title='second post',
            slug='second-post',
        ))

        for language in [get_language()]:
            with override(language):
                for post in posts:
                    knock_create = post.as_knock(True)
                    self.assertEqual(knock_create['title'],
                                     'new {0}'.format(post._meta.verbose_name))
                    self.assertEqual(knock_create['message'], post.title)
                    self.assertEqual(knock_create['language'], language)

    def test_parler_model_attributes(self):
        posts = []
        with smart_override('en'):
            posts.append(MultiLanguagePost.objects.create(
                title='first post',
                slug='first-post',
            ))
            posts.append(MultiLanguagePost.objects.create(
                title='second post',
                slug='second-post',
            ))
        posts[0].create_translation(
            'it',
            title='primo articolo',
            slug='primo-articolo'
        )
        posts[1].create_translation(
            'it',
            title='secondo articolo',
            slug='secondo-articolo'
        )
        posts[0].create_translation(
            'fr',
            title='premier article',
            slug='premier-article'
        )

        for post in posts:
            for language in post.get_available_languages():
                with smart_override(language):
                    post.set_current_language(language)
                    if language != 'fr':
                        knock_create = post.as_knock(True)
                        self.assertEqual(knock_create['title'],
                                         'new {0}'.format(post._meta.verbose_name))
                        self.assertEqual(knock_create['message'], post.title)
                        self.assertEqual(knock_create['language'], language)
                        post.send_knock(True)

                        knock_create = post.as_knock(False)
                        self.assertEqual(knock_create['title'],
                                         'new {0}'.format(post._meta.verbose_name))
                        self.assertEqual(knock_create['message'], post.title)
                        self.assertEqual(knock_create['language'], language)
                        post.send_knock(False)
                    else:
                        self.assertFalse(post.should_knock())
                        self.assertFalse(post.as_knock(True))
                        self.assertFalse(post.as_knock(False))
                        post.send_knock(False)

    @patch('knocker.signals.notify_items', autospec=True)
    def test_no_knock(self, handler):
        posts = []
        post_save.connect(handler, NoKnockPost, dispatch_uid='test_knocker_mock')
        posts.append(NoKnockPost.objects.create(
            title='first post',
            slug='first-post',
        ))
        posts.append(NoKnockPost.objects.create(
            title='second post',
            slug='second-post',
        ))
        self.assertEqual(handler.call_count, 2)

    @patch('knocker.mixins.notify_items')
    def test_signal(self, handler):
        post = Post.objects.create(
            title='signal post',
            slug='signal-post',
        )
        handler.assert_called_once()
        self.assertTrue(handler.return_value)
        handler.reset_mock()

        post.title = 'mod title'
        post.save()
        handler.assert_called_once()
        self.assertTrue(handler.return_value)
        handler.reset_mock()

        with pause_knocks(post):
            post.title = 'pause title'
            post.save()
            self.assertFalse(active_knocks(post))
            handler.assert_not_called()

        post.title = 'mod title'
        post.save()
        handler.assert_called_once()
        self.assertTrue(handler.return_value)
        handler.reset_mock()
