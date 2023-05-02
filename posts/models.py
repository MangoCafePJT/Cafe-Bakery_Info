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
from taggit.managers import TaggableManager
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    CAFE = 'cafe'
    BAKERY = 'bakery'
    CATEGORY_CHOICES = [
        (CAFE, 'Cafe'),
        (BAKERY, 'Bakery'),
    ]
    SEOUL = '서울'
    INCHEON = '인천'
    BUSAN = '부산'
    ULSAN = '울산'
    DAEGU = '대구'
    GWANGJU = '광주'
    DAEJEON = '대전'
    JEJU = '제주도'
    GYEONGGI = '경기도'
    GANGWON = '강원도'
    CHUNGBUK = '충청북도'
    CHUNGNAM = '충청남도'
    JEONBUK = '전라북도'
    JEONNAM = '전라남도'
    GYEONGBUK = '경상북도'
    GYEONGNAM = '경상남도'    
    CITY_CHOICES = [
        (SEOUL, '서울'), (INCHEON, '인천'), (BUSAN, '부산'), (ULSAN, '울산'), (DAEGU, '대구'), (GWANGJU, '광주'), (DAEJEON, '대전'), (JEJU, '제주도'), (GYEONGGI, '경기도'), (GANGWON, '강원도'), (CHUNGBUK, '충청북도'), (CHUNGNAM, '충청남도'), (JEONBUK, '전라북도'), (JEONNAM, '전라남도'), (GYEONGBUK, '경상북도'),(GYEONGNAM, '경상남도'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=200)
    phoneNumberRegex = RegexValidator(regex=r'^0[1-9]\d{0,2}-\d{3,4}-\d{4}$')
    phone = models.CharField(validators=[phoneNumberRegex], max_length=14)
    parking = models.CharField(max_length=50, default='가게 문의')
    business_time = models.CharField(max_length=50, default='가게 문의')
    menu = models.TextField()
    insta = models.URLField(blank=True, null=True)
    home = models.URLField(blank=True, null=True)
    city = models.CharField(max_length=10, choices=CITY_CHOICES)
    tags = TaggableManager()
    rating = models.DecimalField(default=0, max_digits=5, decimal_places=1)

    slug = models.SlugField(unique=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

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
    
    def delete(self, *args, **kargs):
        images = self.postimage_set.all()
        for image in images:
            image.delete()
        super(Post, self).delete(*args, **kargs)
        
    # def save(self, *args, **kwargs):
    #     if self.id:
    #         old_post = self.postimage_set.all()
    #         for image in old_post:
    #             image.delete()
    #     super(Post, self).save(*args, **kwargs)

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def post_image_path(instance, filename):
        return f'post/{instance.post.pk}/{filename}'
    image = ProcessedImageField(
        upload_to=post_image_path,
        blank=True, 
        null=True,)
    
    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(PostImage, self).delete(*args, **kargs)


class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    EMOTIONS = (
        (1, '별로에요'),
        (2, '괜찮아요'),
        (3, '맛있어요'),
    )
    emotion = models.IntegerField(choices=EMOTIONS, default=3)
    title = models.CharField(max_length=50)
    content = models.TextField()
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
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
    
    def save(self, *args, **kwargs):
        self.post.rating = (self.post.rating*self.post.reviews.count() + self.rating) / (self.post.reviews.count() + 1)
        self.post.save()
        super(Review, self).save(*args, **kwargs)
        

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def review_image_path(instance, filename):
        return f'review/{instance.review.pk}/{filename}'
    image = ProcessedImageField(
        upload_to=review_image_path,
        blank=True, 
        null=True, 
        processors=[ResizeToFill(100, 100)], 
        options={'quality':100})
    
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
