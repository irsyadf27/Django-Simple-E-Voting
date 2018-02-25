# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from kandidat.models import Kandidat
#from django.contrib.auth.models import User
from pemilih.models import Pemilih
# Create your models here.
class Pilih(models.Model):
    kandidat = models.ForeignKey(Kandidat, related_name='dipilih')
    #pemilih = models.ForeignKey(User, related_name='memilih')
    pemilih = models.OneToOneField(Pemilih, related_name='memilih')
    waktu = models.DateTimeField(default=timezone.now)

    class Meta:
        permissions = (
            ("bisa_vote", "Pemilih bisa melakukan vote"),
        )