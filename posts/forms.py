from django import forms
from .models import Post, Review, PostImage, ReviewImage, Emote_review


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=50, label='Title*', widget=forms.TextInput(attrs={'required': True}))
    address = forms.CharField(max_length=200, label='Address*', widget=forms.TextInput(attrs={'required': True, 'placeholder': 'Enter address', 'class': 'form-control'}))
    category = forms.ChoiceField(choices=Post.CATEGORY_CHOICES, label='Category*', widget=forms.Select(attrs={'required': True}))
    class Meta:
        model = Post
        fields = ('title', 'category', 'address', 'phone', 'parking', 'time', 'menu',)

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