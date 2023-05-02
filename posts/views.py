from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Review, PostImage, ReviewImage
from .forms import PostForm, ReviewForm, PostImageForm, ReviewImageForm
from django.http import JsonResponse
from django.db.models import Q
from utils.map import get_latlng_from_address
import os
from django.core.paginator import Paginator



def index(request):
    posts = Post.objects.all()
    post_images = []
    for post in posts:
        images = PostImage.objects.filter(post=post)
        if images:
            post_images.append((post, images[0]))
        else:
            post_images.append((post,''))
    context = {
        'post_images': post_images,
    }
    return render(request, 'posts/index.html', context)


@login_required
def create(request):
    post_form = PostForm()
    image_form = PostImageForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        files = request.FILES.getlist('image')
        tags = request.POST.get('tags').split(',')
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            for tag in tags:
                post.tags.add(tag.strip())
            for i in files:
                PostImage.objects.create(image=i, post=post)
            return redirect('posts:detail', post.pk)
    context = {
        'post_form': post_form,
        'image_form': image_form,
    }
    return render(request, 'posts/create.html', context)


def detail(request, post_pk):
    kakao_script_key = os.getenv('kakao_script_key')
    post = Post.objects.get(pk=post_pk)
    rating_filter = request.GET.get('rating-filter', '')
    emotion_filter = request.GET.get('emotion-filter', '')

    reviews = post.reviews.all().order_by('-created_at')

    if rating_filter:
        reviews = reviews.filter(rating=int(rating_filter))
    if emotion_filter:
        reviews = reviews.filter(emotion=int(emotion_filter))

    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    address = post.address
    latitude, longitude = get_latlng_from_address(address)
    post_form = PostForm()
    post_images = []
    images = PostImage.objects.filter(post=post)
    tags = post.tags.all()
    if images:
        post_images.append((post, images))
    else:
        post_images.append((post, ''))
    context = {
        'post': post,
        'post_images': post_images,
        'reviews': reviews,
        'latitude': latitude,
        'longitude': longitude,
        'post_form': post_form,
        'kakao_script_key': kakao_script_key,
        'tags': tags,
        'page_obj': page_obj,
    }
    return render(request, 'posts/detail.html',context)


@login_required
def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        post.delete()
    return redirect('posts:index')


@login_required
def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        files = request.FILES.getlist('image')
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            tags = request.POST.get('tags').split(',')
            for tag in tags:
                post.tags.add(tag.strip())
            for i in files:
                PostImage.objects.create(image=i, post=post)
            return redirect('posts:detail', post.pk)
    else:
        post_form = PostForm(instance=post)
        image_form = PostImageForm()
    context = {
        'post': post,
        'post_form': post_form,
        'image_form': image_form,
    }
    return render(request, 'posts/update.html', context)


@login_required
def review_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    review_form = ReviewForm()
    image_form = ReviewImageForm()
    rating = request.POST.get('rating')
    if rating is None:
        rating = 5
    else:
        try:
            rating = int(rating)
        except ValueError:
            rating = 5
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        files = request.FILES.getlist('image')
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.post = post
            review.user = request.user
            review.rating = rating
            review.emotion = request.POST.get('emotion', 3)
            review.save()
            for i in files:
                ReviewImage.objects.create(image=i, review=review)
            return redirect('posts:detail', post.pk)

    context = {
        'post': post,
        'review_form': review_form,
        'image_form': image_form,
    }
    return render(request, 'posts/review_create.html', context)


@login_required
def review_delete(request, post_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()

    return redirect('posts:detail', post_pk)


@login_required
def likes(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        is_liked = False
    else:
        post.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'likes_count': post.like_users.count(),
        }
    return JsonResponse(context)


@login_required
def review_likes(request, post_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user in review.like_users.all():
        review.like_users.remove(request.user)
        r_is_liked = False
    else:
        review.like_users.add(request.user)
        r_is_liked = True
    context = {
        'r_is_liked': r_is_liked,
        'review_likes_count': review.like_users.count(),
        }
    return JsonResponse(context)


def search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(menu__icontains=query) | Q(address__icontains=query)
        )

        post_images = []
        for post in posts:
            images = PostImage.objects.filter(post=post)
            if images:
                post_images.append((post, images[0]))
            else:
                post_images.append((post,''))

        context = {
            'query': query,
            'posts': posts,
            'post_images': post_images,
        }
    else:
        context = {}

    return render(request, 'posts/search.html', context)

from taggit.models import Tag

def tagged_posts(request, tag_pk):
    tag = Tag.objects.get(pk=tag_pk)
    posts = Post.objects.filter(tags=tag)

    post_images = []
    for post in posts:
        images = PostImage.objects.filter(post=post)
        if images:
            post_images.append((post, images[0]))
        else:
            post_images.append((post,''))

    context = {
        'tag': tag, 
        'posts': posts,
        'post_images': post_images,
        }
    return render(request, 'posts/tagged_posts.html', context)