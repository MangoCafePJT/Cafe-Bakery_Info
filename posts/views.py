from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Review, PostImage, ReviewImage
from .forms import PostForm, ReviewForm, PostImageForm, ReviewImageForm
from django.http import JsonResponse
from django.db.models import Q
from utils.map import get_latlng_from_address
import os
from django.db.models import Count

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
    # reviews = post.reviews.all()
    rating_filter = request.GET.get('rating-filter', '')
    if rating_filter:
        reviews = post.reviews.filter(rating=int(rating_filter))
    else:
        reviews = post.reviews.all()
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
    }
    return render(request, 'posts/detail.html',context)


from django.template.loader import render_to_string

def reviews_filter(request, post_pk):
    rating = request.GET.get('rating')
    if rating:
        reviews = Review.objects.filter(post_id=post_pk, rating=rating)
    else:
        reviews = Review.objects.filter(post_id=post_pk)
    context = {
        'reviews': reviews,
    }
    review_list = render_to_string('posts/detail.html', context)
    return JsonResponse(review_list, safe=False)

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


EMOTIONS = [
    {'label': '😁', 'value': 1},
    {'label': '☹', 'value': 2},
    {'label': '😡', 'value': 3},
]


@login_required
def review_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    review_form = ReviewForm()
    # emote_review_form = EmoteReviewForm()
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
        # emote_review_form = EmoteReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.post = post
            review.user = request.user
            # review.rating = int(request.POST.get('rating', 0))
            review.rating = rating
            review.save()

            # emote_review = emote_review_form.save(commit=False)
            # emote_review.emotion = request.POST.get('emotion')
            # emote_review.review = review
            # emote_review.user = request.user
            # emote_review.save()
            
            for i in files:
                ReviewImage.objects.create(image=i, review=review)
            return redirect('posts:detail', post.pk)

    context = {
        'post': post,
        'review_form': review_form,
        'image_form': image_form,
        # 'emotions': EMOTIONS,
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
