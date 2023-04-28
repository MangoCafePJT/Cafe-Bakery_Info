from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    birthday = models.DateField(null = True, blank=True)
    def profile_image_path(instance, filename):
        return f'profile/{instance.pk}/{filename}'
    image = ProcessedImageField(upload_to=profile_image_path, blank=True, null=True, processors=[ResizeToFill(100, 100)], options={'quality':90})


# class KakaoSignInView(View):
#     def get(self, request):
#         app_key = KAKAO_REST_API_KEY
#         redirect_uri = 'http://127.0.0.1:8080/kakao-login'