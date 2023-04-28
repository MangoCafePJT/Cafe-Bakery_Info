from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta,datetime
from django.conf import settings
import os

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
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=200)
    phoneNumberRegex = RegexValidator(regex=r'^0(2|[1-9]{2})-\d{3,4}-\d{3,4}$')
    phone = models.CharField(blank=True, null=True, validators = [phoneNumberRegex], max_length = 11, unique = True)
    parking = models.CharField(blank=True, null=True, max_length=50)
    time = models.TextField(blank=True, null=True)
    menu = models.TextField(blank=True, null=True)

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.strftime('%Y-%m-%d')


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def post_image_path(instance, filename):
        return f'post/{instance.post.pk}/{filename}'
    image = ProcessedImageField(
        upload_to=post_image_path,
        blank=True, 
        null=True, 
        processors=[ResizeToFill(100, 100)], 
        options={'quality':90})
    
    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(PostImage, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_post = PostImage.objects.get(id=self.id)
            if self.image != old_post.image:
                if old_post.image:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_post.image.name))
        super(PostImage, self).save(*args, **kwargs)


class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emote_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='emote_reviews', through='Emote_review')
    title = models.CharField(max_length=50)
    content = models.TextField()
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.strftime('%Y-%m-%d')
        

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def review_image_path(instance, filename):
        return f'review/{instance.review.pk}/{filename}'
    image = ProcessedImageField(
        upload_to=review_image_path,
        blank=True, 
        null=True, 
        processors=[ResizeToFill(100, 100)], 
        options={'quality':90})
    
    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(ReviewImage, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_post = ReviewImage.objects.get(id=self.id)
            if self.image != old_post.image:
                if old_post.image:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_post.image.name))
        super(ReviewImage, self).save(*args, **kwargs)


class Emote_review(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=10)