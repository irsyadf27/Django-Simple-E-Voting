# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from kandidat.models import Kandidat
from pilih.models import Pilih

# Create your views here.
class KandidatListView(ListView):
    model = Kandidat
    queryset = Kandidat.objects.all().order_by('no_urut')
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(KandidatListView, self).get_context_data(**kwargs)
        context['socket_ip'] = settings.WEBSOCKET_IP
        context['socket_port'] = settings.WEBSOCKET_PORT
        return context
        
class DashboardAdmin(TemplateView):
    template_name = 'dashboard/dashboard_admin.html'

    def __init__(self, **kwargs):
        super(DashboardAdmin, self).__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardAdmin, self).get_context_data(**kwargs)
        context['kandidat'] = Kandidat.objects.all()
        context['socket_ip'] = settings.WEBSOCKET_IP
        context['socket_port'] = settings.WEBSOCKET_PORT
        return context