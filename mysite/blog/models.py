from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Users(models.Model):
    id = models.UUIDField('user_id')
    name = models.CharField(max_length=64)
    passwd = models

class Posts(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.deletion.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

