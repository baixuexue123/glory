from django.db import models
from django.urls import reverse
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=48)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=48)
    rank = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['rank']

    def __str__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=100)
    summary = models.TextField(blank=True)
    body = models.TextField()
    body_html = models.TextField()
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(unique_for_date='pub_date')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=48)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def is_published(self):
        """
        Return True if the entry is publicly accessible.
        """
        return self.is_active and self.pub_date <= timezone.now()
