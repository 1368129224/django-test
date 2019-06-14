from django.shortcuts import render
from . import models


# Create your views here.
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        models.UserInfo.objects.create(username=username, password=password)
    user_list = models.UserInfo.objects.all()
    return render(request, 'mytest/index.html', {'users': user_list})