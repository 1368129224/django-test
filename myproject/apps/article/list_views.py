import redis
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.views.generic import View
from django.utils.decorators import method_decorator
from .models import ArticleColumn, ArticlePost, Comment
from .forms import CommentForm
from django.contrib.auth.models import User

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PASSWORD)

class article_titles(View):
    def get(self, request, username=None):
        if username:
            user = User.objects.get(username=username)
            article_title = ArticlePost.objects.filter(author=user)
            try:
                userinfo = user.userinfo
            except:
                userinfo = None
        else:
            article_title = ArticlePost.objects.all()
        paginator = Paginator(article_title, 6)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
            articles = current_page.object_list
        except PageNotAnInteger:
            current_page = paginator.page(1)
            articles = current_page.object_list
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
            articles = current_page.object_list

        if username is not None:
            return render(request, 'article/list/author_articles.html',
                          {'articles': articles, 'page': current_page, 'userinfo': userinfo, 'user': user,
                           'avatar': settings.MEDIA_URL + userinfo.avatar})
        return render(request, 'article/list/article_titles.html', {'articles': articles, 'page': current_page})

class article_detail(View):
    def get(self, request, id, slug):
        article = get_object_or_404(ArticlePost, id=id, slug=slug)
        total_views = r.incr('article:{}:views'.format(article.id))
        r.zincrby('article_rank', 1, article.id)
        article_rank = r.zrange('article_rank', 0, -1, desc=True)[:10]
        article_rank_ids = [int(id) for id in article_rank]
        most_viewed = list(ArticlePost.objects.filter(id__in=article_rank_ids))
        most_viewed.sort(key=lambda x: article_rank_ids.index(x.id))
        most_viewed = most_viewed[0:5]
        comment_form = CommentForm()
        article_tags_ids = article.article_tag.values_list('id', flat=True)
        similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
        similar_articles = similar_articles.annotate(same_tags=Count('article_tag')).order_by('-same_tags', '-created')
        return render(request, 'article/list/article_content.html',
                      {'article': article, 'total_views': total_views, 'most_viewed': most_viewed,
                       'comment_form': comment_form, 'similar_articles': similar_articles})

    def post(self, request, id, slug):
        article = get_object_or_404(ArticlePost, id=id, slug=slug)
        total_views = r.incr('article:{}:views'.format(article.id))
        r.zincrby('article_rank', 1, article.id)
        article_rank = r.zrange('article_rank', 0, -1, desc=True)[:10]
        article_rank_ids = [int(id) for id in article_rank]
        most_viewed = list(ArticlePost.objects.filter(id__in=article_rank_ids))
        most_viewed.sort(key=lambda x: article_rank_ids.index(x.id))
        most_viewed = most_viewed[0:5]
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
        article_tags_ids = article.article_tag.values_list('id', flat=True)
        similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
        similar_articles = similar_articles.annotate(same_tags=Count('article_tag')).order_by('-same_tags', '-created')
        return render(request, 'article/list/article_content.html',
                      {'article': article, 'total_views': total_views, 'most_viewed': most_viewed,
                       'comment_form': comment_form, 'similar_articles': similar_articles})

class like_article(View):
    @method_decorator(login_required(login_url='/account/login/'))
    def post(self, request):
        article_id = request.POST.get('id')
        action = request.POST.get('action')
        if article_id and action:
            try:
                article = ArticlePost.objects.get(id=article_id)
                if action == 'like':
                    article.user_like.add(request.user)
                    return HttpResponse('1')
                else:
                    article.user_like.remove(request.user)
                    return HttpResponse('0')
            except:
                return HttpResponse('-1')
