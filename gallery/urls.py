from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^photos/$',
        views.PhotoListView.as_view(),
        name="photos"
    )
]
