from django.db import models

from blog.models import Post


class Comment(models.Model):
    author = models.CharField(max_length=48)
    text = models.TextField()
    approved = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    post = models.ForeignKey(Post, related_name='comments')
