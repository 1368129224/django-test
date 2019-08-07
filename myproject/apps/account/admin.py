from django.contrib import admin
from .models import UserProfile, UserInfo

# Register your models here.
class UserProflieAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth', 'phone')
    list_filter = ('phone', 'user__username')

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'company', 'profession', 'address', 'aboutme', 'avatar')
    list_filter = ('school', 'company', 'profession')

admin.site.register(UserProfile, UserProflieAdmin)
admin.site.register(UserInfo, UserInfoAdmin)