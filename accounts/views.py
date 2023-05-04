from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm, CustomPasswordChangeForm
from django.http import JsonResponse

def login(request):
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:index')
      
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('posts:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def delete(request):
    request.user.delete()
    return redirect('posts:index')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile',request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('posts:index')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)



from django.contrib.auth import get_user_model

def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user

    if you != me:
        if me in you.followers.all():
            you.followers.remove(me)
            is_followed = False
        else:
            you.followers.add(me)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followings_count': you.followings.count(),
            'followers_count': you.followers.count(),
            'followings': [{'username': f.username, 'pk': f.pk} for f in you.followings.all()],
            'followers': [{'username': f.username,'pk': f.pk} for f in you.followers.all()]
        }
        
        return JsonResponse(context)
    return redirect('accounts:profile', you.username)

def follower(request, user_pk):
    User = get_user_model()
    user = User.objects.get(pk=user_pk)
    followers = [{'username': f.username, 'pk': f.pk} for f in user.followers.all()]
    return JsonResponse({'followers': followers})



# 구글 로그인 사용자 정보 받아오기
# from django.views.generic import TemplateView
# from allauth.account.views import LoginView
# from allauth.socialaccount.models import SocialAccount

# class MyLoginView(LoginView):
#     template_name = 'login.html'

#     def get_success_url(self):
#         # 로그인 후 사용자 정보 저장
#         user = self.request.user
#         social_account = SocialAccount.objects.get(user=user, provider='google')
#         extra_data = social_account.extra_data

#         # extra_data에서 사용자 정보 추출
#         first_name = extra_data.get('given_name')
#         last_name = extra_data.get('family_name')
#         email = extra_data.get('email')

#         # 데이터베이스에 저장
#         user.first_name = first_name
#         user.last_name = last_name
#         user.email = email
#         user.save()

#         return super().get_success_url()

# class LoginTemplateView(TemplateView):
#     template_name = 'login.html'

#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('home')
#         return super().get(request, *args, **kwargs)

# from django.views.generic import TemplateView

# class HomeView(TemplateView):
#     template_name = 'home.html'

#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return super().get(request, *args, **kwargs)
#         return redirect('account_login')
