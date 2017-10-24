from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^editor/$', views.editor, name="editor"),
    url(r'^upload-image/$', views.upload_image, name="upload_image"),
    url(r'^detail/$', views.detail, name="detail"),
]
