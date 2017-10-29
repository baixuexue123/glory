from django.db import models


class Image(models.Model):

    image = models.ImageField(upload_to='cms/images/%Y/%m')
    pub_date = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        return self.image.url
