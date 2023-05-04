from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm,  PasswordChangeForm
from django.contrib.auth import get_user_model
import datetime


years = [x for x in range(1940, datetime.datetime.now().year + 1)]

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '아이디를 입력하세요',
                'style' : 'width: 400px;'
            }
        ),
    )
    email = forms.EmailField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일을 입력하세요',
            }
        ),
    )
    last_name = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이름을 입력하세요',
            }
        ),
    )

    birthday = forms.DateField(
        initial=datetime.date(2000, 1, 1),
        label=False,
        widget=forms.DateInput(
            attrs={
                'type':'date',
                'class': 'form-control',
            }
        ),
    )
    password1 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호를 입력하세요',
            }
        ),
    )
    password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호를 다시 입력하세요',
            }
        ),
    )

    REGION_CHOICES = [
        ('서울', '서울'), ('인천', '인천'), ('부산', '부산'), ('울산', '울산'), ('대구', '대구'), ('광주', '광주'), ('대전', '대전'), ('제주도', '제주도'), ('경기도', '경기도'), ('강원도', '강원도'), ('충청북도', '충청북도'), ('충청남도', '충청남도'), ('전라북도', '전라북도'), ('전라남도', '전라남도'), ('경상북도', '경상북도'),('경상남도', '경상남도'),
    ]

    region = forms.ChoiceField(
        choices=REGION_CHOICES,
        label=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'last_name', 'password1', 'password2', 'region', 'birthday')


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(
        label= False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일을 입력하세요',
                'style' : 'width: 400px;'
            }
        )
    )
    last_name = forms.CharField(
        label= False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이름을 입력하세요',
                'style' : 'width: 400px;'
            }
        )
    )
    REGION_CHOICES = [
        ('서울', '서울'), ('인천', '인천'), ('부산', '부산'), ('울산', '울산'), ('대구', '대구'), ('광주', '광주'), ('대전', '대전'), ('제주도', '제주도'), ('경기도', '경기도'), ('강원도', '강원도'), ('충청북도', '충청북도'), ('충청남도', '충청남도'), ('전라북도', '전라북도'), ('전라남도', '전라남도'), ('경상북도', '경상북도'),('경상남도', '경상남도'),
    ]

    region = forms.ChoiceField(
        choices=REGION_CHOICES,
        label=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    
    birthday = forms.DateField(
        initial=datetime.date(2000, 1, 1),
        label=False,
        widget=forms.DateInput(
            attrs={
                'type':'date',
                'class': 'form-control',
            }
        ),
    )
    password=None

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'last_name', 'region', 'birthday')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '아이디',
                'style' : 'width:400px;'
            }
        )
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '비밀번호',
                'style' : 'width:400px;'
            }
        )
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '기존 비밀번호',
                'style' : 'width:400px;'
            }
        )
    )
    new_password1 = forms.CharField(
        label=False,
        widget= forms.PasswordInput(
        attrs = {
                'class': 'form-control',
                'placeholder' : '새 비밀번호',
                'style' : 'width:400px;'
            }
        ),
        help_text='',
    )
    new_password2 = forms.CharField(
        label=False,
        widget= forms.PasswordInput(
        attrs = {
                'class': 'form-control',
                'placeholder' : '새 비밀번호(확인)',
                'style' : 'width:400px;'
            }
        ),
        help_text='',
    )