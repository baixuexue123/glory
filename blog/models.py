from django.db import models
from django.urls import reverse
from django.utils import timezone

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from uuslug import uuslug


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


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.active().filter(pub_date__lte=timezone.now())

    def active(self):
        return self.filter(is_active=True)


class Post(models.Model):

    title = models.CharField(max_length=100)
    summary = models.TextField()
    body = models.TextField()
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(unique_for_date='pub_date', editable=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    author = models.CharField(max_length=48)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='blog')
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(400, 205)],
                                     format='JPEG', options={'quality': 60})

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'year': self.pub_date.year,
            'month': self.pub_date.strftime('%b').lower(),
            'day': self.pub_date.strftime('%d').lower(),
            'slug': self.slug,
        }
        return reverse('blog:detail', kwargs=kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def is_published(self):
        """
        Return True if the post is publicly accessible.
        """
        return self.is_active and self.pub_date <= timezone.now()
    is_published.boolean = True
