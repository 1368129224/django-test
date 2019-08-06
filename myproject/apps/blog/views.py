from django.shortcuts import render, get_object_or_404
from .models import BlogArticles

def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, 'blog/index.html', {'blogs':blogs})

def blog_article(request, article_id):
    article = get_object_or_404(BlogArticles, id=article_id)
    pub = article.publish
    return render(request, "blog/article.html", {"article":article, "publish":pub })