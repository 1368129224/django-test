from django.shortcuts import render, get_object_or_404
from .models import BlogArticles

# Create your views here.
def index(request):
    return render(request, 'blog/index.html', {'articles': BlogArticles.objects.all()})

def article(request, id):
    return render(request, 'blog/article.html', {'article': get_object_or_404(BlogArticles, pk=id)})