from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from PelakuUsaha.models import PelakuUsaha
from .forms import SearchDataForm, PickDateForm
from django.core.paginator import Paginator
import pandas as pd



# Create your views here.

def home(request):
    if request.user.is_superuser:
        Data_usaha = PelakuUsaha.objects.order_by('-id')[:5]
    else:
        Data_usaha = PelakuUsaha.objects.filter(kecamatan=request.user.first_name).order_by('-id')[:5]
    User = request.user

    context = {
        'data_usaha': Data_usaha,
        'User':User
    }

    return render(request, 'Dashboard/home.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, 'Login Berhasil')
            return redirect('home')
        else:
            messages.error(request, 'Username atau Password Salah')
            return redirect('login')
    else:
        return render(request, 'Dashboard/login.html')
    
def export_to_excel(start_date, end_date):

    # datausaha = PelakuUsaha.objects.all()
    # df = pd.DataFrame(list(datausaha.values()))

    # form = PickDateForm()
    # if request.method == 'GET':
    #     form = PickDateForm(request.GET)
    #     if form.is_valid():
    #         start_date = form.cleaned_data['start_date']
    #         end_date = form.cleaned_data['end_date']
    #         print(start_date)
    #         print(end_date)
    #         datausaha = PelakuUsaha.objects.filter(tanggal_input__range=[start_date, end_date])
    datausaha = PelakuUsaha.objects.filter(tanggal_input__range=[start_date, end_date])
    df = pd.DataFrame(list(datausaha.values()))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="detail_sj_keluar.xlsx"'
    df.to_excel(response, index=False)

    return response

def RekapData(request):

    if request.user.is_superuser:
        data = PelakuUsaha.objects.all()
    else:
        data = PelakuUsaha.objects.filter(kecamatan=request.user.first_name)
    
    form = SearchDataForm()
    
    selected_nib = None
    if request.method == 'POST':
        form = SearchDataForm(request.POST or None)
        form2 = PickDateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            nib = cd.get('nib')
            kecamatan = cd.get('kecamatan')
            selected_nib = nib
            if request.user.is_superuser:
               
                if nib and kecamatan:
                    data = data.filter(nib=nib, kecamatan=kecamatan)
                elif nib:
                    data = data.filter(nib=nib)
                elif kecamatan:
                    data = data.filter(kecamatan=kecamatan)
            else:
                data = data.filter(nib=nib)
        if form2.is_valid():
            start_date = form2.cleaned_data['start_date']
            end_date = form2.cleaned_data['end_date']
            print(start_date)
            print(end_date)

            if start_date and end_date:
                data = data.filter(tanggal_input__range=[start_date, end_date])
            download = export_to_excel(start_date,end_date)   
            return download 
    data2 = data.order_by('-nib')
    
    paginator = Paginator(data2,25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    pilih_nib = PelakuUsaha.objects.values_list('nib', flat=True).distinct()
    pilih_kec = None
    if request.user.is_superuser:
        pilih_kec = PelakuUsaha.objects.values_list('kecamatan',flat=True).distinct
    form2 = PickDateForm()
    # if request.method == 'POST':
        
    #     if form2.is_valid():
    #         cd = form.cleaned_data
    #         start_date = cd.get('start_date')
    #         end_date = cd.get('end_date')
    #         print(start_date)
    #         print(end_date)
            
    #         download = export_to_excel(start_date,end_date)
    #         return download
    
    context = {
        'data':page_obj,
        'form':form,
        'form2':form2,
        'pilih_nib':pilih_nib,
        'selected_nib':selected_nib,
        'pilih_kec':pilih_kec

    }
    return render(request, 'Dashboard/RekapData.html', context)


