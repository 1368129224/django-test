from django import template
register = template.Library()

from article.models import ArticlePost
from django.db.models import Count

from django.utils.safestring import mark_safe
import markdown

@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

@register.simple_tag
def author_article_num(user):
    return user.article.count()

@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by('-created')[:n]
    return {'latest_articles': latest_articles}

@register.simple_tag
def most_commented_articles(n=3):
    ranked_articles = ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")
    not_zero_articles = [ranked_article for ranked_article in ranked_articles if ranked_article.total_comments != 0]
    return not_zero_articles

@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))