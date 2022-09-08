import os
import django
from django.test import TestCase
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network.settings')
django.setup()

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from posts.models import Post, Like
from users.models import Profile


class PostCreateViewTest(TestCase):
    """
        TestCase class to test the view functionality
    """
    c = Client()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user1',
            email='test@gmail.com',
            password='high_mountain'
        )
        self.profile = Profile.objects.get(
            user=self.user,
        )
        self.profile.status = 'developer'
        self.profile.country = 'USA'
        self.profile.save()

    def test_create_post(self):
        Post.objects.create(
            author=self.profile, content="Simple post"
        ).save()

        self.c.force_login(self.user)
        self.c.post(reverse('posts:main'))
        self.assertTrue(Post.objects.filter(author=self.profile).exists())


class PostUpdateViewTest(TestCase):
    """
    TestCase class to test the view functionality
    """
    c = Client()

    def test_post_update(self):
        self.user = get_user_model().objects.create_user(
            username='test_user2',
            email='test1@gmail.com',
            password='high_mountain'
        )
        self.profile = Profile.objects.get(
            user=self.user,
        )
        self.profile.status = 'developer'
        self.profile.country = 'USA'
        post = Post.objects.create(
            author=self.profile, content='test post')

        self.c.force_login(self.user)
        response = self.c.post(
            reverse('posts:post_update', kwargs=({'pk': post.id})),
            {'content': 'change content'}
        )
        self.assertEqual(response.status_code, 302)


class PostDeleteViewTest(TestCase):
    """
    TestCase class to test the view functionality
    """
    c = Client()

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user1',
            email='test1@gmail.com',
            password='high_mountain')
        self.profile = Profile.objects.get(
            user=self.user,
        )
        self.profile.status = 'developer'
        self.profile.country = 'USA'

        self.post = Post.objects.create(
            author=self.profile, content='test post')

    def test_delete_post(self):
        self.assertEqual(Post.objects.count(), 13)

        self.c.force_login(self.user)
        response = self.c.post(reverse('posts:post_delete', kwargs={'pk': self.post.id}))
        self.assertEqual(Post.objects.count(), 12)
        self.assertEqual(response.status_code, 302)
