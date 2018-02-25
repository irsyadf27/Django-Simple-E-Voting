from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from kandidat.views import KandidatListView, KandidatCreateView, KandidatUpdateView, KandidatDeleteView

urlpatterns = [
    url(r'^$', login_required(KandidatListView.as_view()), name='list-kandidat'),
    url(r'^create/$', login_required(KandidatCreateView.as_view()), name='create-kandidat'),
    url(r'^update/(?P<pk>[0-9]+)$', login_required(KandidatUpdateView.as_view()), name='update-kandidat'),
    url(r'^delete/(?P<pk>[0-9]+)$', login_required(KandidatDeleteView.as_view()), name='delete-kandidat'),
]
