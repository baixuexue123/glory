from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import LoginView

from blog.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^login/$', LoginView.as_view(template_name='login.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^gallery/', include('gallery.urls', namespace='gallery')),
    url(r'^cms/', include('cms.urls', namespace='cms')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
