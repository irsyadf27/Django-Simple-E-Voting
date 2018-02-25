# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from kandidat.models import Kandidat
from pilih.models import Pilih
from pemilih.models import Pemilih

admin.site.register(Kandidat)
admin.site.register(Pilih)
admin.site.register(Pemilih)