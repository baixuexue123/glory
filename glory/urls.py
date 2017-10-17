from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from .views import index

urlpatterns = [
    url(r'^$', index),
    url(r'^admin/', admin.site.urls),

    url(r'^blog/', include('blog.urls', namespace='blog')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
