from django.db import models

from blog.models import Post


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.CharField('author')
    content = models.TextField('content')
