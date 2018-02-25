# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from django.contrib import messages
from kandidat.models import Kandidat
from pilih.models import Pilih
from pemilih.models import Pemilih

# Create your views here.
def pilih_kandidat(request, pk):
    kandidat = Kandidat.objects.get(pk=pk)
    perm = Permission.objects.get(codename='bisa_vote')
    pemilih = Pemilih.objects.get(user__pk=request.user.pk)

    try:
        plh = Pilih.objects.get(pemilih=pemilih)
        messages.warning(request, 'Anda sudah pernah memilih kandidat.')
    except Pilih.DoesNotExist:
        if request.user.has_perm('pilih.bisa_vote'):
            Pilih.objects.create(kandidat=kandidat, pemilih=pemilih)
            pemilih.user.user_permissions.remove(perm)
            pemilih.user.save()
            messages.success(request, 'Anda berhasil memilih kandidat.')

    return redirect('dashboard')