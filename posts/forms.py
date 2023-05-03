from django import forms
from .models import Post, Review, PostImage, ReviewImage
from taggit.forms import TagField, TagWidget
from taggit.managers import TaggableManager

class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=50, 
        label='가게명(필수)', 
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
        label='주소(필수)', 
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
        label='카테고리(필수)', 
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
        label='메뉴(필수)', 
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
        label='지역(필수)', 
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-select',
                'style' : 'width: 600px;'
            }
        )
    )

    phone = forms.CharField(
        max_length=14, 
        required = False,
        label='전화번호(필수)', 
        widget=forms.TextInput(
            attrs={
                'placeholder': '-을 포함해주세요.',
                'class': 'form-control',
                'style' : 'width: 600px;'
                
            }
        )
    )             
    parking = forms.CharField(
        label='주차', 
        widget=forms.TextInput(
            attrs={
                'value': '가게문의',
                'class': 'form-control',
                'style' : 'width: 600px;',
            }
        )
    )
    business_time = forms.CharField(
        label='영업시간',
        widget=forms.TextInput(
            attrs={  
                'value': '가게문의',
                'class': 'form-control',
                'style' : 'width: 600px;'
            }
        )
    )
    insta = forms.CharField(
        label='인스타그램', 
        required = False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '인스타그램 주소를 입력해주세요.', 
                'class': 'form-control',
                'style' : 'width: 600px;'
            }
        )
    )
    home = forms.CharField(
        label='홈페이지', 
        required = False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '홈페이지 주소를 입력해주세요.',
                'class': 'form-control',
                'style' : 'width: 600px;'
            }
        )
    )
    class Meta:
        model = Post
        fields = ('title', 'category', 'city', 'address', 'phone', 'parking', 'business_time', 'menu', 'insta', 'home', 'tags')
        widgets = {
            'tags': TagWidget(attrs={
                'class': 'form-control', 
                'style' : 'width: 600px;',
                'placeholder': "태그는 콤마(,)로 구분해주세요.",
                }),
        }

        
class PostImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='관련 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True, 
                'class': 'form-control', 
                'style' : 'width: 600px;'
            }
        ),
    )
    class Meta:
        model = PostImage
        fields = ('image',)

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