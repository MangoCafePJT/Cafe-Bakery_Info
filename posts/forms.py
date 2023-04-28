from django import forms
from .models import Post, Review, PostImage, ReviewImage, Emote_review


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'address', 'phone', 'parking', 'time', 'menu',)
        widgets = {
            'category': forms.Select(choices=Post.CATEGORY_CHOICES),
        }

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)
        widgets = {'image': forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'})}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'content',)

class ReviewImageForm(forms.ModelForm):
    class Meta:
        model = ReviewImage
        fields = ('image',)
        widgets = {'image': forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'})}


class EmoteReviewForm(forms.ModelForm):
    class Meta:
        model = Emote_review
        fields = ('emotion',)


class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')