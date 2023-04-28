from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Review, PostImage, ReviewImage, Emote_review
from .forms import PostForm, ReviewForm, PostImageForm, ReviewImageForm, EmoteReviewForm, PostSearchForm
from django.http import JsonResponse
from django.db.models import Q
from utils.map import get_latlng_from_address
import os


def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'posts/index.html', context)


@login_required
def create(request):
    post_form = PostForm()
    image_form = PostImageForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        files = request.FILES.getlist('image')
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            for i in files:
                PostImage.objects.create(image=i, post=post)
            return redirect('posts:detail', post.pk)
    context = {
        'post_form': post_form,
        'image_form': image_form,
    }
    return render(request, 'posts/create.html', context)


def detail(request, post_pk):
    kakao_script_key = os.environ.get('kakao_script_key')
    post = Post.objects.get(pk=post_pk)
    reviews = post.review_set.all()
    address = post.address
    latitude, longitude = get_latlng_from_address(address)
    post_form = PostForm()
    post_images = []
    images = PostImage.objects.filter(post=post)
    if images:
        post_images.append((post, images))
    else:
        post_images.append((post, ''))
    context = {
        'post':post,
        'post_images':post_images,
        'reviews':reviews,
        'latitude': latitude,
        'longitude': longitude,
        'post_form': post_form,
        'kakao_script_key': kakao_script_key,
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
    emote_review_form = EmoteReviewForm()
    image_form = ReviewImageForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        files = request.FILES.getlist('image')
        emote_review_form = EmoteReviewForm(request.POST)

        if review_form.is_valid() and emote_review_form.is_valid():
            review = review_form.save(commit=False)
            review.post = post
            review.user = request.user
            review.rating = int(request.POST.get('rating', 0))
            review.save()

            emote_review = emote_review_form.save(commit=False)
            emote_review.emotion = request.POST.get('emotion')
            emote_review.review = review
            emote_review.user = request.user
            emote_review.save()
            
            for i in files:
                ReviewImage.objects.create(image=i, review=review)
            return redirect('posts:detail', post.pk)

    context = {
        'post': post,
        'review_form': review_form,
        'image_form': image_form,
        'emote_review_form': emote_review_form,
        'emotions': EMOTIONS,
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
    else:
        review.like_users.add(request.user)
    return redirect('posts:detail', post_pk)


def search(request):
    keyword = request.GET.get('keyword','')
    posts = Post.objects.all()
    if keyword:
        posts = posts.filter(
            Q(title__icontains=keyword)|
            Q(menu__icontains=keyword))
    
    post_images = []
    for post in posts:
        images = PostImage.objects.filter(post=post)
        if images:
            post_images.append((post, images[0]))
        else:
            post_images.append((post,''))
            
    context = {
        'keyword': keyword,
        'posts': posts,
        'post_images': post_images,
    }
    return render(request, 'posts/search.html', context)


# from django.views.generic.edit import FormView

# class SearchFormView(FormView):
#     form_class = PostSearchForm
#     template_name = 'posts/search.html'

#     def form_valid(self, form):
#         searchWord = form.cleaned_data['search_word']
#         post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(menu__icontains=searchWord)).distinct()

#         context = {}
#         context['form'] = form
#         context['search_term'] = searchWord
#         context['object_list'] = post_list

#         return render(self.request, self.template_name, context)