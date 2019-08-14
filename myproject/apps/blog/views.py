from django.shortcuts import render, get_object_or_404
from .models import BlogArticles
from myproject.settings import MEDIA_URL
from account.models import UserInfo

def blog_title(request):
    blogs = BlogArticles.objects.all()
    if request.user.is_authenticated:
        userinfo = UserInfo.objects.get(user_id=request.user.id) if hasattr(request.user,'userinfo') else UserInfo.objects.create(user=request.user)
        return render(request, 'blog/index.html', {'blogs':blogs, 'userinfo':userinfo, 'avatar': MEDIA_URL + userinfo.avatar})
    else:
        return render(request, 'blog/index.html', {'blogs': blogs})

def blog_article(request, article_id):
    article = get_object_or_404(BlogArticles, id=article_id)
    pub = article.publish
    return render(request, "blog/article.html", {"article":article, "publish":pub })