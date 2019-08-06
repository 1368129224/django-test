from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo


# 写入数据库，修改记录值 - 继承 ModelForm
# 不对数据进行修改 - 继承 Form
class RegistrationFrom(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password does not match.')
        return cd['password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'birth')

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme", "avatar")

class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("avatar", )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)