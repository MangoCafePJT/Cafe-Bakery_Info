from django import forms
from .models import Post, Review, PostImage, ReviewImage
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
                'class': 'form-control',
                'style' : 'width: 600px;'
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
                'class': 'form-control',
                'style' : 'width: 600px;'
            }
        )
    )
    category = forms.ChoiceField(
        choices=Post.CATEGORY_CHOICES, 
        label='Category*', 
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-select',
                'style' : 'width: 600px;'
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
                'style' : 'width: 600px;'
            }
        )
    )
    city = forms.ChoiceField(
        choices=Post.CITY_CHOICES, 
        label='City*', 
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-select',
                'style' : 'width: 600px;'
            }
        )
    )
    tags = TaggableManager(
        help_text='태그를 입력해주세요.',
    )
    
    phone = forms.CharField(
        max_length=14, 
        required = False,
        label='Phone', 
        widget=forms.TextInput(
            attrs={
                'placeholder': '-을 포함해주세요.',
                'class': 'form-control',
                'style' : 'width: 600px;'
                
            }
        )
    )             
    parking = forms.CharField(
        label='Parking', 
        widget=forms.TextInput(
            attrs={
                'value': '가게문의',
                'class': 'form-control',
                'style' : 'width: 600px;',
            }
        )
    )
    business_time = forms.CharField(
        label='Business Time',
        widget=forms.TextInput(
            attrs={  
                'value': '가게문의',
                'class': 'form-control',
                'style' : 'width: 600px;'
            }
        )
    )
    insta = forms.CharField(
        label='Instagram', 
        required = False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Instagram 주소를 입력해주세요.', 
                'class': 'form-control',
                'style' : 'width: 600px;'
            }
        )
    )
    home = forms.CharField(
        label='Home', 
        required = False,
        widget=forms.TextInput(
            attrs={  
                'class': 'form-control',
                'style' : 'width: 600px;'
            }
        )
    )
    class Meta:
        model = Post
        fields = ('title', 'category', 'city', 'address', 'phone', 'parking', 'business_time', 'menu', 'insta', 'home', 'tags')
        widgets = {
            'tags': TagWidget(attrs={'class': 'form-control', 'style' : 'width: 600px;'}),
        }

        
class PostImageForm(forms.ModelForm):
    
    class Meta:
        model = PostImage
        fields = ('image',)
        widgets = {'image': forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control', 'style' : 'width: 600px;'})}

class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        max_length=50, 
        label='Title', 
        widget=forms.TextInput(
            attrs={
                'required': True,
                'placeholder': '제목을 입력해주세요.',
                'class': 'form-control',
                'style' : 'width: 400px;'
            }
        )
    )
    content = forms.CharField(
        max_length=200, 
        label='Content', 
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': '내용을 입력해주세요.',
                'style' : 'width: 400px;'
            }
        )
    )
    class Meta:
        model = Review
        fields = ('title', 'content',)
        

class ReviewImageForm(forms.ModelForm):
    class Meta:
        model = ReviewImage
        fields = ('image',)
        widgets = {'image': forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control', 'style' : 'width: 400px;'})}


# class EmoteReviewForm(forms.ModelForm):
#     class Meta:
#         model = Emote_review
#         fields = ('emotion',)