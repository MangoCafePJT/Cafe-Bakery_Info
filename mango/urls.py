"""mango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path
# from accounts.views import LoginTemplateView, MyLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('posts/', include('posts.urls')),
    path('chat/', include('chat.urls')),
    path('my_messages/', include('my_messages.urls')),
    # 구글 정보 받아오기
    # path('login/', LoginTemplateView.as_view(), name='login'),
    # path('accounts/login/', MyLoginView.as_view(), name='account_login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
