from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm, UserProfileForm
from .models import UserProfile, UserInfo

# Create your views here.
def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponse("Wellcome You.You have been authenticated successfully")
            else:
                return HttpResponse("Sorry. Your username or password is not right.")
        else:
            return HttpResponse("Invalid login")

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})

def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponse('succeed')
        else:
            return HttpResponse('info error')
    else:
        user_form = RegistrationForm
        userprofile_form = UserProfileForm
        return render(request, 'account/registeration.html', {'form': user_form, 'profile_form': userprofile_form})

@login_required()
def myself(request):
    userprofile = UserProfile.objects.get(user=request.user) if \
        hasattr(request.user, 'userprofile') else \
        UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if \
        hasattr(request.user, 'userinfo') else \
        UserInfo.objects.create(user=request.user)
    return render(request, "account/myself.html", {"user":request.user, "userinfo":userinfo, "userprofile":userprofile})