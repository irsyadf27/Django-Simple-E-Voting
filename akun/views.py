# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing 
from reportlab.graphics.barcode.qr import QrCodeWidget 
from io import BytesIO

from akun.forms import AdminForm, PemilihForm, LoginPemilihForm
from pemilih.models import Pemilih

# Create your views here.
def login(request):
    if request.user.is_authenticated():
        return redirect('dashboard')
    return render(request, 'akun/login.html')

class LoginPemilihView(FormView):
    form_class = LoginPemilihForm
    success_url = reverse_lazy('dashboard')
    template_name = 'akun/login_pemilih.html'

    def get_form_kwargs(self):
        kwargs = super(LoginPemilihView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        print form.login()
        return super(LoginPemilihView, self).form_valid(form)

@method_decorator(staff_member_required(login_url='dashboard'), name='dispatch')
class AdminListView(ListView):
    model = User
    queryset = User.objects.filter(is_staff=True)
    template_name = 'akun/admin/list.html'
    paginate_by = 10

@method_decorator(staff_member_required(login_url='dashboard'), name='dispatch')
class AdminCreateView(CreateView):
    form_class = AdminForm
    model = User
    success_url = reverse_lazy('list-admin')
    template_name = 'akun/admin/create.html'

@method_decorator(staff_member_required(login_url='dashboard'), name='dispatch')
class AdminUpdateView(UpdateView):
    form_class = AdminForm
    model = User
    success_url = reverse_lazy('list-admin')
    template_name = 'akun/admin/update.html'

@method_decorator(staff_member_required(login_url='dashboard'), name='dispatch')
class AdminDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('list-admin')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@method_decorator(staff_member_required(login_url='dashboard'), name='dispatch')
class PemilihListView(ListView):
    model = User
    #queryset = Pemilih.objects.all()
    queryset = Pemilih.objects.order_by('id')
    template_name = 'akun/pemilih/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PemilihListView, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context

@method_decorator(staff_member_required(login_url='dashboard'), name='dispatch')
class PemilihCreateView(FormView):
    form_class = PemilihForm
    success_url = reverse_lazy('list-pemilih')
    template_name = 'akun/pemilih/create.html'

    def form_valid(self, form):
        form.generate_akun()
        return super(PemilihCreateView, self).form_valid(form)

@method_decorator(staff_member_required(login_url='dashboard'), name='dispatch')
class PemilihDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('list-pemilih')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@staff_member_required(login_url='dashboard')
def delete_all_pemilih(request):
    User.objects.filter(is_staff=False).delete()
    return redirect('list-pemilih')

def buat_kotak(c, nomor, height, baris, kolom, string):
    awal = 35 + (130 * (kolom - 1)) + (5 * (kolom - 1))
    panjang = awal + 130

    brs = height - (60 + (115 * (baris - 1)))
    brs2 = height - (165 + (115 * (baris - 1)))

    c.line(awal, brs, panjang, brs)
    c.line(awal, brs, awal, brs2)
    c.line(awal, brs2, panjang, brs2)
    c.line(panjang, brs2, panjang, brs)

    qrw = QrCodeWidget(string) 
    b = qrw.getBounds()

    w=b[2]-b[0] 
    h=b[3]-b[1] 

    d = Drawing(100,100,transform=[100./w,0,0,100./h,0,0]) 
    d.add(qrw)

    renderPDF.draw(d, c, awal + 15, brs - 90)
    c.setFont('Helvetica', 12)
    c.drawString(awal + 6, brs - 92, string)
    c.setFont('Helvetica', 6)
    c.drawString(awal + 2, brs2 + 2, str(nomor))

@staff_member_required(login_url='dashboard')
def pemilih_export(request, cetak):
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setLineWidth(1)
    width, height = letter
    c.drawString(30, height-20, 'Daftar Akun Pemilih')
    c.drawString(width-50, height-20, str(c.getPageNumber()))
    c.line(30,height-25,width-30,height-25)

    if cetak == 'belum':
        daftar_pemilih = Pemilih.objects.filter(cetak=False)
    else:
        daftar_pemilih = Pemilih.objects.all()

    daftar_pemilih.update(cetak=True)

    baris = 1
    kolom = 1
    nomor = 1
    counter = 1
    for i in daftar_pemilih:
        buat_kotak(c, nomor, height, baris, kolom, i.user.username)
        kolom += 1
        nomor +=1
        counter += 1
        if kolom > 4:
            baris += 1
            kolom = 1

        if counter % 25 == 0:
            c.showPage()
            c.drawString(30, height-20, 'Daftar Akun Pemilih')
            c.drawString(width-50, height-20, str(c.getPageNumber()))
            c.line(30,height-25,width-30,height-25)
            baris = 1
            kolom = 1
            counter = 1

    c.save()
    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

