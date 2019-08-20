import os
import base64
from django.conf import settings
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import RegistrationFrom, UserProfileForm, UserInfoForm, UserForm
from .models import UserInfo, UserProfile

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = RegistrationFrom(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponseRedirect(reverse('account:login'))
        else:
            return render(request, 'account/register.html', {'form': user_form, 'profile_form': userprofile_form})
    else:
        user_form = RegistrationFrom()
        userprofile_form = UserProfileForm()
        return render(request, 'account/register.html', {'form': user_form, 'profile_form': userprofile_form})

@login_required()
def my_info(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user, 'userprofile') else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user, 'userinfo') else UserInfo.objects.create(user=request.user)
    return render(request, "account/my_info.html", {"user":request.user, "userinfo":userinfo, "userprofile":userprofile, 'avatar': settings.MEDIA_URL + userinfo.avatar})

@login_required(login_url='/account/login/')
def change_my_info(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user,'userprofile') else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user,'userinfo') else UserInfo.objects.create(user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            request.user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            request.user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-info/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth, "phone": userprofile.phone})
        userinfo_form = UserInfoForm(
            initial={"school": userinfo.school, "company": userinfo.company, "profession": userinfo.profession,
                     "address": userinfo.address, "aboutme": userinfo.aboutme})
        return render(request, "account/change_my_info.html",
                      {"user_form": user_form, "userprofile_form": userprofile_form, "userinfo_form": userinfo_form})

@login_required(login_url='/account/login/')
def my_avatar(request):
    # userinfo = get_object_or_404(UserInfo, id=request.user.id)
    userinfo = UserInfo.objects.get(user_id=request.user.id)
    if request.method == 'POST':

        # 传Base64方式
        avatar = request.POST['avatar']
        avatar_str = avatar.replace('data:image/png;base64,', '')
        img = base64.b64decode(avatar_str)
        img_name = str(request.user.id) + '.png'
        if userinfo.avatar != os.path.join('avatar', 'Avatar.jpg'):
            old_avatar = userinfo.avatar
            avatar_path = os.path.join(settings.MEDIA_ROOT, old_avatar)
            print(avatar_path)
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
                print('Deleted old avatar.')
        with open(os.path.join(os.path.join(settings.MEDIA_ROOT,'avatar'), img_name), 'wb')as f:
            f.write(img)
        userinfo.avatar = os.path.join('avatar', img_name)
        userinfo.save()
        return HttpResponse('1')
    else:
        return render(request, 'account/change_avatar.html', {'avatar': settings.MEDIA_URL + userinfo.avatar})


