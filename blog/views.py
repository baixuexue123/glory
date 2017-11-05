from django.shortcuts import redirect, resolve_url, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.dates import (
    ArchiveIndexView, DateDetailView
)
from .models import Post, Category, Comment


class PostViewMixin:

    date_field = 'pub_date'
    paginate_by = 20

    def get_allow_future(self):
        return self.request.user.is_staff

    def get_queryset(self):
        if self.request.user.is_staff:
            posts = Post.objects.all()
        else:
            posts = Post.objects.published()
        title = self.request.GET.get('title')
        if title:
            posts = posts.filter(title__contains=title)
        return posts


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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@require_POST
def add_comment(request):
    author = request.POST.get('author', '').strip() or '某人'
    text = request.POST.get('text').strip()
    parent = request.POST.get('parent')

    if parent is not None:
        parent = get_object_or_404(Comment, pk=parent)
    post = get_object_or_404(Post, pk=request.POST.get('post'))

    if not text:
        return redirect(resolve_url(post))

    c = Comment(
        author=author, text=text,
        parent=parent, post=post,
        ip_address=get_client_ip(request)
    )
    c.save()
    return redirect(resolve_url(post))
