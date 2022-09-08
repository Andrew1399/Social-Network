import os
import re
import django
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import Profile
from music.models import Album, Song


class TestAlbumModelView(TestCase):
    """
    TestCase class to test the path function
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

    def test_album(self):
        self.album = Album.objects.create(title='test', artist='test', year=2022,
                                          logo="images/3cc33455-bd2f-4f48-8e32-cd3bf582466f.jpg",
                                          user=self.profile)
        self.album.save()


class TestSongModelView(TestCase):
    """
    TestCase class to test the path function
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user2',
            email='test@gmail.com',
            password='high_mountain'
        )
        self.profile = Profile.objects.get(
            user=self.user,
        )
        self.profile.save()
        self.album = Album.objects.create(title='test', artist='test', year=2022,
                                          logo="images/3cc33455-bd2f-4f48-8e32-cd3bf582466f.jpg",
                                          user=self.profile)
        self.album.save()

    def test_album(self):
        song = Song.objects.create(title='test', track_number=1,
                                   file="ACDC_-_Shoot_to_Thrill_47830035.mp3", album=self.album)
        song.save()
