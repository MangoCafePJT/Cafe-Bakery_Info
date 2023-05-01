from django import forms
from .models import Post, Review, PostImage, ReviewImage, Emote_review
from taggit.forms import TagField, TagWidget
from taggit.managers import TaggableManager

class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=50, 
        label='Title*', 
        widget=forms.TextInput(
            attrs={
                'required': True,
                'placeholder': '제목을 입력해주세요.',
                'class': 'form-control' 
            }
        )
        
    )
    address = forms.CharField(
        max_length=200, 
        label='Address*', 
        widget=forms.TextInput(
            attrs={
                'required': True, 
                'placeholder': '정확한 주소를 입력해주세요.', 
                'class': 'form-control'
            }
        )
    )
    category = forms.ChoiceField(
        choices=Post.CATEGORY_CHOICES, 
        label='Category*', 
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-select'
            }
        )
    )
    menu = forms.CharField(
        max_length=200, 
        label='Menu*', 
        widget=forms.Textarea(
            attrs={
                'required': True,
                'placeholder': '메뉴를 입력해주세요.', 
                'class': 'form-control',
            }
        )
    )
    city = forms.ChoiceField(
        choices=Post.CITY_CHOICES, 
        label='City*', 
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-select'
            }
        )
    )
    tags = TaggableManager(
        blank=True,
        help_text='태그를 입력해주세요.',
        
    )
    

    phone = forms.CharField(
        max_length=14, 
        required = False,
        label='Phone', 
        widget=forms.TextInput(
            attrs={
                'placeholder': '전화번호를 입력해주세요.', 
                'class': 'form-control'
                
            }
        )
    )             
    parking = forms.CharField(
        max_length=50, 
        required = False,
        label='Parking', 
        widget=forms.TextInput(
            attrs={  
                
                'class': 'form-control'
            }
        )
    )
    business_time = forms.CharField(
        label='Business Time', 
        required = False,
        widget=forms.TextInput(
            attrs={  
                'class': 'form-control'
            }
        )
    )
    insta = forms.CharField(
        label='Instagram', 
        required = False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Instagram 주소를 입력해주세요.', 
                'class': 'form-control'
            }
        )
    )
    home = forms.CharField(
        label='Home', 
        required = False,
        widget=forms.TextInput(
            attrs={  
                'class': 'form-control'
            }
        )
    )
    class Meta:
        model = Post
        fields = ('title', 'category', 'city', 'address', 'phone', 'parking', 'business_time', 'menu', 'insta', 'home', 'tags')
        widgets = {
            'tags': TagWidget(attrs={'class': 'form-control'}),
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