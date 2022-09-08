from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.shortcuts import reverse
from users.utils import get_random_number
from network import settings
import os
import hashlib, urllib


class ProfileManager(models.Manager):
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        queryset = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = set([])
        for rel in queryset:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        available = [profile for profile in profiles if profile not in accepted]
        return available


class Profile(models.Model):
    """
    The page of the user, this one is created whenever a new user signs up.
    """
    first_name = models.CharField(max_length=150, db_index=True)
    last_name = models.CharField(max_length=150, db_index=True)
    email = models.EmailField(max_length=150, db_index=True)
    country = models.CharField(max_length=150, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(db_index=True, default='No information...', max_length=550)
    status = models.CharField(max_length=60, db_index=True)
    friends = models.ManyToManyField(User, db_index=True, blank=True, related_name='friends')
    image = models.ImageField(upload_to='images', default='images/avatar.jpg')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}-{self.created_at.strftime('%d-%m-%Y')}"

    def get_absolute_url(self):
        return reverse('users:profile_detail', kwargs={"slug": self.slug})

    def get_friends(self):
        return self.friends.all()[:6]

    def get_friends_list(self):
        return self.friends.all().count()

    def get_posts_list(self):
        return self.posts.all().count()

    def get_posts(self):
        return self.posts.all()[:4]

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_given_likes_list(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

    def get_received_likes_list(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    # instead of image

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_number()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):

    def invitations_received(self, receiver):
        queryset = Relationship.objects.filter(receiver=receiver, status='send')
        return queryset


class Relationship(models.Model):
    """
    Model for operations connected with user's friends, actions: send, receive, delete
    """
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
