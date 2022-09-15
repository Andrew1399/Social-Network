import os
import re
import django
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network.settings')
django.setup()

from gallery.models import get_image_path
from django.contrib.auth import get_user_model
from gallery.models import Image
from users.models import Profile


class TestPath(TestCase):
    """
    TestCase class to test the path function
    """
    def test_image_path(self):

        test_list = [
            'random_image.jpeg',
            'cool_picture.png',
            'image.jpg',
            'nice.webp'
        ]
        for pattern in test_list:
            uuid_image = get_image_path(None, pattern)
            file_extension = os.path.splitext(pattern)[1]
            comp = re.compile(
                '^images/[0-9A-F]{{8}}-[0-9A-F]{{4}}-4[0-9A-F]{{3}}-'
                '[89AB][0-9A-F]{{3}}-[0-9A-F]{{12}}{extension}$'.format(extension="\\" + file_extension),
                flags=re.IGNORECASE
            )
            self.assertTrue(re.fullmatch(comp, uuid_image))


class TestImageModel(TestCase):
    """
    TestCase class to test the model functionality
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user1',
            email='test@gmail.com',
            password='high_mountain'
        )
        self.profile = Profile.objects.get(
            user=self.user,
        )
        self.profile.save()

    def test_image(self):
        image = Image.objects.create(name='test', path_to_image='/images/ec6dbc63-adf5-4037-9468-3aa240dbeafe.jpg', size=16780, author=self.profile)
        image.save()
