from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('city/', views.city, name='city'),
    path('filtering/<str:sort>/', views.filtering, name='filtering'),
    path('city/filtering/<str:sort>/', views.city_filtering, name='city_filtering'),
    path('create/', views.create, name='create'),
    path('<int:post_pk>/', views.detail, name='detail'),
    path('<int:post_pk>/likes/', views.likes, name='likes'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/update/', views.update, name='update'),
    path('<int:post_pk>/reviews/', views.review_create, name='review_create'),
    path('<int:post_pk>/reviews/<int:review_pk>', views.review_update, name='review_update'),
    path('<int:post_pk>/reviews/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:post_pk>/reviews/<int:review_pk>/likes/', views.review_likes, name='review_likes'),
    path('search/', views.search, name='search'),
    path('tags/<int:tag_pk>/', views.tagged_posts, name='tagged_posts'),
]