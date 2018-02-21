from django.shortcuts import redirect, resolve_url, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.dates import ArchiveIndexView, DateDetailView

from .models import Post, Category, Comment


class PostViewMixin:
    date_field = 'pub_date'

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
    make_object_list = True

    def get(self, request, *args, **kwargs):
        self.date_list, self.object_list = self.get_dated_items()
        context = self.get_context_data(object_list=self.object_list,
                                        date_list=self.date_list)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        object_list = kwargs.pop('object_list', self.object_list)
        date_list = kwargs.pop('date_list', self.date_list)
        context = {
            'categories': Category.objects.all(),
            'objects': zip([d.year for d in date_list], object_list)
        }
        return context

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

        object_list = []
        for date in date_list:
            object_list.append(qs.filter(pub_date__year=date.year))

        return (date_list, object_list)


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
    post = get_object_or_404(Post, pk=request.POST.get('post'))

    if not text:
        return redirect(resolve_url(post))

    c = Comment(
        author=author, text=text, post=post,
        ip_address=get_client_ip(request)
    )
    c.save()
    return redirect(resolve_url(post))
