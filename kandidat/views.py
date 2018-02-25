# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from kandidat.models import Kandidat

# Create your views here.
@method_decorator(staff_member_required(login_url='dashboard'), name='dispatch')
class KandidatListView(ListView):
    model = Kandidat
    queryset = Kandidat.objects.all().order_by('no_urut')
    template_name = 'kandidat/list.html'
    paginate_by = 10

@method_decorator(staff_member_required(login_url='dashboard'), name='dispatch')
class KandidatCreateView(CreateView):
    model = Kandidat
    fields = ['no_urut', 'nama', 'foto', ]
    success_url = reverse_lazy('list-kandidat')
    template_name = 'kandidat/create.html'

@method_decorator(staff_member_required(login_url='dashboard'), name='dispatch')
class KandidatUpdateView(UpdateView):
    model = Kandidat
    fields = ['no_urut', 'nama', 'foto', ]
    success_url = reverse_lazy('list-kandidat')
    template_name = 'kandidat/update.html'


@method_decorator(staff_member_required(login_url='dashboard'), name='dispatch')
class KandidatDeleteView(DeleteView):
    model = Kandidat
    success_url = reverse_lazy('list-kandidat')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)