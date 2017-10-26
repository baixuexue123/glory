from django.views.generic import ListView
from django.views.generic.dates import (
    ArchiveIndexView, DateDetailView
)
from .models import Post, Category


class PostViewMixin:

    date_field = 'pub_date'
    paginate_by = 20

    def get_allow_future(self):
        return self.request.user.is_staff

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        else:
            return Post.objects.published()


class IndexView(PostViewMixin, ListView):
    model = Post
    template_name = 'index.html'
    paginate_by = 5


class PostArchiveIndexView(PostViewMixin, ArchiveIndexView):
    allow_empty = True
    date_list_period = 'year'
    template_name = 'blog/archive.html'

    def get_dated_items(self):
        """
        Return (date_list, items, extra_context) for this request.
        """
        lookup = {}
        c = self.request.GET.get('c')
        if c:
            lookup['category'] = c
        qs = self.get_dated_queryset(**lookup)
        date_list = self.get_date_list(qs, ordering='DESC')

        if not date_list:
            qs = qs.none()

        extra = {'categories': Category.objects.all()}
        return (date_list, qs, extra)


class PostDateDetailView(PostViewMixin, DateDetailView):
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev'] = Post.objects.filter(id__lt=self.object.id).order_by('id').last()
        context['next'] = Post.objects.filter(id__gt=self.object.id).order_by('id').first()
        return context
