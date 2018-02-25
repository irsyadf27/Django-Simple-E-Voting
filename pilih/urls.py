from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from pilih.views import pilih_kandidat

urlpatterns = [
    url(r'^kandidat/(?P<pk>[0-9]+)$', pilih_kandidat, name='pilih-kandidat'),
]
