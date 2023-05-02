from django.shortcuts import render, redirect
from posts.models import Post, PostImage

def main(request):
    posts = Post.objects.order_by('-rating')
    post_images = []
    for post in posts[:5]:
        images = PostImage.objects.filter(post=post)
        if images:
            post_images.append((post, images[0]))
        else:
            post_images.append((post,''))
    context = {
    'post_images': post_images,
    }
    return render(request, 'main.html', context)