from django.db.models.signals import post_delete
from django.dispatch import receiver
from music.models import Album, Song

@receiver(post_delete, sender=Song)
def song_post_delete(sender, **kwargs):
    song = kwargs['instance']
    storage = song.file.storage
    path = song.file.path
    storage.delete(path)

@receiver(post_delete, sender=Album)
def album_post_delete(sender, **kwargs):
    album = kwargs['instance']
    storage = album.logo.storage
    path = album.logo.path
    storage.delete(path)