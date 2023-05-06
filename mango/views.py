from django.shortcuts import render, redirect
from posts.models import Post, PostImage

def main(request):
    cafe_posts = Post.objects.filter(category='cafe').order_by('-rating')
    bakery_posts = Post.objects.filter(category='bakery').order_by('-rating')

    post_images = []
    for post in cafe_posts[:5]:
        images = PostImage.objects.filter(post=post)
        if images:
            post_images.append((post, images[0]))
        else:
            post_images.append((post,''))

    bakery_post_images = []
    for post in bakery_posts[:5]:
        images = PostImage.objects.filter(post=post)
        if images:
            bakery_post_images.append((post, images[0]))
        else:
            bakery_post_images.append((post,''))
            
    context = {
    'post_images': post_images,
    'bakery_post_images' : bakery_post_images,
    }
    return render(request, 'main.html', context)