import os
import django
from django.test import TestCase
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.urls import reverse
from posts.models import Post, Comment, Like
from users.models import Profile


class CommentModelViewTest(TestCase):
    """
    TestCase class to test the model functionality
    """
    c = Client()

    def setUp(self):
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

    def test_comment(self):
        post = Post.objects.create(author=self.profile, content='Test post 1')
        Comment.objects.create(content='Test post 1 comment', user=self.profile,
                               post=post).save()

        self.c.force_login(self.user)
        self.c.post(reverse('posts:main'))


class LikeModelTest(TestCase):
    """
    TestCase class to test the model functionality
    """
    c = Client()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user1',
            email='test1@gmail.com',
            password='high_mountain'
        )
        self.profile = Profile.objects.get(
            user=self.user,
        )
        self.profile.status = 'developer'
        self.profile.country = 'USA'

    def test_like_model(self):
       simple_post = Post.objects.create(author=self.profile, content="Test post")
       Like.objects.create(user=self.profile, post=simple_post, value="Like")
