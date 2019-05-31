from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField('分类', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

class Tag(models.Model):
    name = models.CharField('标签', max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name

class Entry(models.Model):
    title = models.CharField('文章标题', max_length=128)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    body = models.TextField('正文', )
    visiting = models.PositiveIntegerField('访问量', default=0)