# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Kandidat(models.Model):
    nama = models.CharField(max_length=100)
    no_urut = models.IntegerField()
    foto = models.ImageField(upload_to='foto_kandidat', null=True, blank=True)

    def __unicode__(self):
        return self.nama