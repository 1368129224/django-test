from django.shortcuts import render, get_object_or_404
from .models import BlogArticles

# Create your views here.
def index(request):
    context = {'articles': BlogArticles.objects.all(), }
    print(type(BlogArticles.objects.all()))
    return render(request, 'blog/index.html', context)

def article(request, id):
    return render(request, 'blog/article.html', {'article': get_object_or_404(BlogArticles, pk=id), })