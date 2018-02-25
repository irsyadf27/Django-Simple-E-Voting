from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login
from pemilih.models import Pemilih
import uuid

class LoginPemilihForm(forms.Form):
    kode = forms.CharField(widget=forms.TextInput(attrs={'class':'input-kode'}), required=True)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(LoginPemilihForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(LoginPemilihForm, self).clean()
        cek = Pemilih.objects.filter(user__username=cleaned_data['kode']).exists()
        if not cek:
            raise forms.ValidationError({'kode': ["Kode tidak valid!",]})
        return cleaned_data

    def login(self):
        akun = User.objects.get(username=self.cleaned_data['kode'])
        login(self.request, akun)
        
class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    repeat_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

    def clean(self):
        cleaned_data = super(AdminForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("repeat_password")

        if User.objects.filter(email__iexact=cleaned_data.get("email")).exclude(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError(
                {'email': ["Email sudah ada yang menggunakan.",]}
            )

        if password != confirm_password:
            raise forms.ValidationError(
                {'password': ["Password dan Konfirmasi Password tidak sama.",]}
            )

    def save(self, commit=True):
        user = super(AdminForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        user.is_staff = True
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

"""
class PemilihForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        
        ]

    def clean(self):
        cleaned_data = super(PemilihForm, self).clean()

    def save(self, commit=True):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        usr, created = User.objects.update_or_create(username=username)
        if created:
            usr.set_password(password)
            p = Permission.objects.get(codename='bisa_vote')
            usr.user_permissions.add(p)
        usr.save()
        return usr
"""
def random_code(string_length=16):
    random = str(uuid.uuid4()).upper().replace("-","")
    return random[0:string_length]

class PemilihForm(forms.Form):
    jumlah_akun = forms.IntegerField(required=True)

    def clean(self):
        cleaned_data = super(PemilihForm, self).clean()

    def generate_akun(self):
        for i in range(0, self.cleaned_data['jumlah_akun']):
            usr, created = User.objects.update_or_create(username=random_code)
            if created:
                p = Permission.objects.get(codename='bisa_vote')
                usr.user_permissions.add(p)
                Pemilih.objects.create(user=usr)
            usr.save()