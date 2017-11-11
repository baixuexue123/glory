from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Photo


class PhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'gallery/photos.html'
    paginate_by = 20
    context_object_name = 'photos'

    def get_queryset(self):
        photos = super().get_queryset()
        title = self.request.GET.get('title')
        if title:
            photos = photos.filter(desc__contains=title)
        return photos
