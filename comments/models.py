from django.db import models, transaction

from blog.models import Post


class Comment(models.Model):
    author = models.CharField(max_length=48)
    text = models.TextField(max_length=2048)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=24, default='')

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    tree_path = models.CharField(max_length=255, editable=False)

    post = models.ForeignKey(Post, related_name='comments')

    @property
    def depth(self):
        return len(self.tree_path.split('/'))

    @property
    def root_id(self):
        return int(self.tree_path.split('/')[0])

    @property
    def root_path(self):
        return Comment.objects.filter(pk__in=self.tree_path.split('/')[:-1])
