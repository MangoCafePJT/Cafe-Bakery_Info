from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Review
from .forms import PostForm, ReviewForm
from django.http import JsonResponse

def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'posts/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:detail', post.pk)
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'posts/create.html', context)


def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    review_form = ReviewForm()
    reviews = post.review_set.all()
    context = {
        'post': post,
        'review_form': review_form,
        'reviews': reviews,
        'emotions_choices': Review.EMOTIONS_CHOICES,
    }
    return render(request, 'posts/detail.html', context)


@login_required
def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        post.delete()
    return redirect('posts:index')


@login_required
def review_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    review_form = ReviewForm(request.POST, request.FILES)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.post = post
        review.user = request.user
        review_form.save()
        return redirect('posts:detail', post.pk)
    context = {
        'post': post,
        'review_form': review_form,
    }
    return render(request, 'posts/detail.html', context)


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