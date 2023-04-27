from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Post(models.Model):
    CAFE = 'cafe'
    BAKERY = 'bakery'
    CATEGORY_CHOICES = [
        (CAFE, 'Cafe'),
        (BAKERY, 'Bakery'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(blank=True, null=True, processors=[ResizeToFill(100, 100)], options={'quality':90})


class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = ProcessedImageField(blank=True, null=True, processors=[ResizeToFill(100, 100)], options={'quality':90})
    DELICIOUS = 'DL'
    OKAY = 'OK'
    NOT_GOOD = 'NG'
    EMOTIONS_CHOICES = [
        (DELICIOUS, 'Delicious'),
        (OKAY, 'Okay'),
        (NOT_GOOD, 'Not good'),
    ]
    emotion = models.CharField(max_length=2, choices=EMOTIONS_CHOICES)