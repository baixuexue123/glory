from django.db import models


class Image(models.Model):

    image = models.ImageField(upload_to='cms')
    pub_date = models.DateTimeField(auto_now_add=True)
