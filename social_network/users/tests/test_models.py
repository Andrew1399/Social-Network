import os
import django
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from users.models import Profile, Relationship


class TestProfileModelView(TestCase):
    """
    TestCase class to test the models functionality
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user5',
            email='test@gmail.com',
            password='top_secret'
        )
        self.profile = Profile.objects.get(
            user=self.user,
        )
        self.profile.status = 'developer'
        self.profile.country = 'USA'
        self.profile.save()

    def test_object_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertTrue(isinstance(self.profile.user, User))

    def test_return_screen_name(self):
        self.assertEqual(self.profile.get_screen_name(), self.user.username)


class TestRelationshipModelView(TestCase):
    """
    TestCase class to test the model functionality
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user1',
            email='test1@gmail.com',
            password='high_mountain'
        )
        self.user1 = get_user_model().objects.create_user(
            username='test_user2',
            email='test1@gmail.com',
            password='high_mountain'
        )
        self.profile = Profile.objects.get(
            user=self.user,
        )
        self.profile1 = Profile.objects.get(
            user=self.user1,
        )
        self.profile.save()
        self.profile1.save()

    def test_relationship(self):
        rel = Relationship.objects.create(sender=self.profile, receiver=self.profile1, status="send")
        rel.save()
