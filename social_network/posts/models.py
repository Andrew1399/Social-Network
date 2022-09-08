from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from users.models import Profile


class Post(models.Model):
    """
    model for creating user's posts
    """
    content = models.TextField()
    image = models.ImageField(upload_to='images', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])], blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.content[:40]}"

    def number_likes(self):
        return self.liked.all().count()

    def number_comments(self):
        return self.comment_set.all().count()


class Comment(models.Model):
    """
    Model for commenting posts
    """
    content = models.TextField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return f" {str(self.pk)} - {self.content}"


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    """
    Model for liking posts
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=8, choices=LIKE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}-{self.created_at}"
