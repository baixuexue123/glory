from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$',
        views.PostDateDetailView.as_view(),
        name="detail"
    ),
    url(
        r'^archives/$',
        views.PostArchiveIndexView.as_view(),
        name="archives"
    )
]
