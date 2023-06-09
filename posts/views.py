from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Review, PostImage, ReviewImage
from .forms import PostForm, ReviewForm, PostImageForm, ReviewImageForm, DeleteImageForm, DeleteReviewImageForm
from django.http import JsonResponse
from django.db.models import Prefetch, Q
from utils.map import get_latlng_from_address
import os
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Count
from django.core.cache import cache
from taggit.models import Tag


@login_required
def index(request):
    posts = Post.objects.order_by('-pk')
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
def city(request):
    posts = Post.objects.order_by('-pk')
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
    return render(request, 'posts/index_city.html', context)

@login_required
def filtering(request, sort):
    posts = Post.objects.all()
    if sort == '별점순':
        posts = Post.objects.order_by('-rating')
        post_images = []
        for post in posts:
            images = PostImage.objects.filter(post=post)
            if images:
                post_images.append((post, images[0]))
            else:
                post_images.append((post,''))
    elif sort == '리뷰순':
        posts = Post.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
        post_images = []
        for post in posts:
            images = PostImage.objects.filter(post=post)
            if images:
                post_images.append((post, images[0]))
            else:
                post_images.append((post,''))
    elif sort == '좋아요순':
        posts = Post.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')
        post_images = []
        for post in posts:
            images = PostImage.objects.filter(post=post)
            if images:
                post_images.append((post, images[0]))
            else:
                post_images.append((post,''))
    return render(request, 'posts/index.html', {'post_images': post_images})

@login_required
def city_filtering(request, sort):
    posts = Post.objects.all()
    if sort == '별점순':
        posts = Post.objects.order_by('-rating')
        post_images = []
        for post in posts:
            images = PostImage.objects.filter(post=post)
            if images:
                post_images.append((post, images[0]))
            else:
                post_images.append((post,''))
    elif sort == '리뷰순':
        posts = Post.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
        post_images = []
        for post in posts:
            images = PostImage.objects.filter(post=post)
            if images:
                post_images.append((post, images[0]))
            else:
                post_images.append((post,''))
    elif sort == '좋아요순':
        posts = Post.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')
        post_images = []
        for post in posts:
            images = PostImage.objects.filter(post=post)
            if images:
                post_images.append((post, images[0]))
            else:
                post_images.append((post,''))
    return render(request, 'posts/index_city.html', {'post_images': post_images})

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


@login_required
def detail(request, post_pk):
    kakao_script_key = os.getenv('kakao_script_key')
    post = Post.objects.select_related('user').prefetch_related(
        Prefetch('reviews', queryset=Review.objects.select_related('user'))
    ).get(pk=post_pk)
    address = post.address
    latitude, longitude = get_latlng_from_address(address)
    rating_filter = request.GET.getlist('rating-filter')
    emotion_filter = request.GET.getlist('emotion-filter')
    filter_args = Q()
    # rating 값이 존재하면 필터 추가
    if rating_filter:
        rating_filter_q = Q()
        for rating in rating_filter:
            if rating:
                rating_filter_q |= Q(rating=int(rating))
        filter_args &= rating_filter_q 
    # emotion 값이 존재하면 필터 추가
    if emotion_filter:
        emotion_filter_q = Q()
        for emotion in emotion_filter:
            if emotion:
                emotion_filter_q |= Q(emotion=int(emotion))
        filter_args &= emotion_filter_q
        
    reviews = post.reviews.filter(filter_args).order_by('-created_at')

    hit_count = request.session.get('hit_count_{}'.format(post_pk), 0)
    hit_count += 1
    request.session['hit_count_{}'.format(post_pk)] = hit_count

    post_form = PostForm()
    review_form = ReviewForm()
    post_images = []
    images = post.postimage_set.all()
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
        'review_form': review_form,
        'hit_count': hit_count,
    }
    return render(request, 'posts/detail.html', context)

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
        delete_ids = request.POST.getlist('delete_images')
        delete_form = DeleteImageForm(post=post, data=request.POST) 
        if post_form.is_valid() and delete_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            post.tags.clear()
            tags = request.POST.get('tags').split(',')
            for tag in tags:
                post.tags.add(tag.strip())
            for delete_id in delete_ids:
                post.postimage_set.filter(pk=delete_id).delete()
            for i in files:
                PostImage.objects.create(image=i, post=post)
            return redirect('posts:detail', post.pk)
    else:
        post_form = PostForm(instance=post)
        delete_form = DeleteImageForm(post=post)
    if post.postimage_set.exists():
        image_form = PostImageForm(instance=post.postimage_set.first())
    else:
        image_form = PostImageForm()
    context = {
        'post': post,
        'post_form': post_form,
        'image_form': image_form,
        'delete_form': delete_form,
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
        image_form = ReviewImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if review_form.is_valid() and image_form.is_valid():
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
def review_update(request, post_pk, review_pk):
    post = Post.objects.get(pk=post_pk)
    review = Review.objects.get(pk=review_pk)
    review_form = ReviewForm(instance=review)
    image_form = ReviewImageForm()
    delete_form = DeleteReviewImageForm(review=review)
    rating = request.POST.get('rating')
    if rating is None:
        rating = 5
    else:
        try:
            rating = int(rating)
        except ValueError:
            rating = 5
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        files = request.FILES.getlist('image')
        delete_ids = request.POST.getlist('delete_images')
        delete_form = DeleteReviewImageForm(review=review, data=request.POST)
        if review_form.is_valid() and delete_form.is_valid():
            review = review_form.save(commit=False)
            review.post = post
            review.user = request.user
            review.rating = rating
            review.emotion = request.POST.get('emotion', 3)
            review.save()
            for delete_id in delete_ids:
                review.reviewimage_set.filter(pk=delete_id).delete()
            for i in files:
                ReviewImage.objects.create(image=i, review=review)
            return redirect('posts:detail', post.pk)
    if review.reviewimage_set.exists():
        image_form = ReviewImageForm(instance=review.reviewimage_set.first())
    else:
        image_form = ReviewImageForm()
    context = {
        'post': post,
        'review': review,
        'review_form': review_form,
        'image_form': image_form,
        'delete_form': delete_form,
    }
    return render(request, 'posts/review_update.html', context)



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

        page = request.GET.get('page', '1')
        per_page = 8
        paginator = Paginator(post_images, per_page)
        page_obj = paginator.get_page(page)

        context = {
            'query': query,
            'posts': posts,
            'post_images': page_obj,
        }
    else:
        context = {}

    return render(request, 'posts/search.html', context)



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

    page = request.GET.get('page', '1')
    per_page = 8
    paginator = Paginator(post_images, per_page)
    page_obj = paginator.get_page(page)

    context = {
        'tag': tag, 
        'posts': posts,
        'post_images': page_obj,
        }
    return render(request, 'posts/tagged_posts.html', context)