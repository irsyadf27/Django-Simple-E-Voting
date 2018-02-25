from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from akun.views import AdminListView, AdminCreateView, AdminUpdateView, AdminDeleteView, \
    PemilihListView, PemilihCreateView, PemilihDeleteView, delete_all_pemilih, \
    pemilih_export, login, LoginPemilihView


urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^login_pemilih/$', LoginPemilihView.as_view(), name='login-pemilih'),
    url(r'^login_panitia/$', auth_views.login, {'template_name': 'akun/login_panitia.html'}, name='login-panitia'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    # Crud admin
    url(r'^admin/$', login_required(AdminListView.as_view()), name='list-admin'),
    url(r'^admin/create/$', login_required(AdminCreateView.as_view()), name='create-admin'),
    url(r'^admin/update/(?P<pk>[0-9]+)$', login_required(AdminUpdateView.as_view()), name='update-admin'),
    url(r'^admin/delete/(?P<pk>[0-9]+)$', login_required(AdminDeleteView.as_view()), name='delete-admin'),

    # Crud pemilih
    url(r'^pemilih/$', login_required(PemilihListView.as_view()), name='list-pemilih'),
    url(r'^pemilih/create/$', login_required(PemilihCreateView.as_view()), name='create-pemilih'),
    url(r'^pemilih/delete/(?P<pk>[0-9]+)$', login_required(PemilihDeleteView.as_view()), name='delete-pemilih'),
    url(r'^pemilih/all_delete/$', login_required(delete_all_pemilih), name='delete-all-pemilih'),
    url(r'^pemilih/export/(?P<cetak>[a-z]+)$', login_required(pemilih_export), name='export-pemilih'),
]
