# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
import qrcode
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# Create your models here.
def random_code(string_length=16):
    random = str(uuid.uuid4()).upper().replace("-","")
    return random[0:string_length]

class Pemilih(models.Model):
    user = models.OneToOneField(User, related_name='pemilih')
    #code = models.CharField(max_length=200, default=random_code, unique=True)
    cetak = models.BooleanField(default=False)
    def __unicode__(self):
        return self.user.username

    @property
    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=0,
        )
        qr.add_data(self.user.username)
        qr.make(fit=True)
        img = qr.make_image()
        output = StringIO()
        img.save(output, "PNG")
        contents = output.getvalue().encode("base64")
        output.close()
        return contents