from django import forms
from .models import Post, Review


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'content', 'category')
        widgets = {
            'category': forms.Select(choices=Post.CATEGORY_CHOICES),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'image', 'content', 'emotion')
        widgets = {
            'emotion': forms.Select(choices=Review.EMOTIONS_CHOICES),
        }