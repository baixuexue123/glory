from django.shortcuts import render
from blog.models import Post


def index(request):
    context = {
        'posts': Post.objects.published()
    }
    return render(request, "index.html", context)
