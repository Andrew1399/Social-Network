import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import TestCase
from users.forms import ProfileModelForm


class ProfileFormTest(TestCase):
    """
    TestCase class to test the form functionality
    """
    def test_username_already_taken(self):
        User.objects.create_user(
            username='user2', email='user2@gmail.com', password='high_mountain')

        form = ProfileModelForm(
            data={
                'username': 'user2',
                'bio': 'something about me'
            },
        )

        self.assertFalse(form.is_valid())

