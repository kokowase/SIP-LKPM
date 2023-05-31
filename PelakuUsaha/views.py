from django.shortcuts import render, redirect
from PelakuUsaha.models import PelakuUsaha
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import PelakuUsahaForm
# Create your views here.

def LaporanUsaha(request):
    form = PelakuUsahaForm(request.POST or None)
    if request.POST or form.is_valid():
        form.save()
        messages.success(request,'Laporan Berhasil dibuat')
        return redirect ('home')
    
    context={
        'form':form
    }
    return render(request, 'PelakuUsaha/BuatLaporan.html',context)
