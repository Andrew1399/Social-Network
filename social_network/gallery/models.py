import os
import uuid
from django.db import models
from django.utils.timezone import now
from users.models import Profile


def get_image_path(instance, file):
    return "images/{0}{1}".format(uuid.uuid4(), os.path.splitext(file)[1])


class Image(models.Model):
    """
    Class for image gallery
    """
    name = models.CharField(max_length=100)
    path_to_image = models.ImageField(upload_to=get_image_path)
    datetime = models.DateTimeField(default=now)
    size = models.IntegerField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.name
