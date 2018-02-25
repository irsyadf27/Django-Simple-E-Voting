"""evoting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import KandidatListView, DashboardAdmin

urlpatterns = [
    url(r'^$', login_required(KandidatListView.as_view()), name='dashboard'),
    url(r'^dashboard/admin$', login_required(DashboardAdmin.as_view()), name='dashboard-admin'),
    url(r'^admin/', admin.site.urls),
    url(r'^akun/', include('akun.urls')),
    url(r'^kandidat/', include('kandidat.urls')),
    url(r'^pilih/', include('pilih.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
