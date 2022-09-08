from django.db import models
from users.models import Profile
from django.urls import reverse


class Album(models.Model):
    """
    Class for music album which contains songs
    """
    title = models.CharField(max_length=200, db_index=True)
    artist = models.CharField(max_length=300, db_index=True)
    year = models.CharField(max_length=4)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='images/')
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("music:detail", kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.title} - {self.artist} - {self.year}"


class Song(models.Model):
    """
    Class for songs in album
    """
    title = models.CharField(max_length=300)
    file = models.FileField(upload_to='songs/', default='')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    track_number = models.IntegerField(default=1)
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("music:detail", kwargs={'pk': self.album.id})

    def __str__(self):
        return self.title
