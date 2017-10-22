from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Photo(models.Model):

    image = models.ImageField(upload_to='gallery')
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(300, 300)],
                                     format='JPEG', options={'quality': 60})
    desc = models.CharField(max_length=128)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __str__(self):
        return self.desc
