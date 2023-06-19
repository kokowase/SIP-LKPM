from django.shortcuts import render, redirect
from PelakuUsaha.models import PelakuUsaha
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from .forms import PelakuUsahaForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from django.contrib.auth.decorators import login_required
import os
# Create your views here.

@login_required (login_url='login')
def LaporanUsaha(request):
    form = PelakuUsahaForm(request.POST or None)
    if request.POST or form.is_valid():
        cd = form.save()
        messages.success(request,'Laporan Berhasil dibuat')
        return redirect('tandaterima', nib=cd.nib)
        
    
    context={
        'form':form
    }
    return render(request, 'PelakuUsaha/BuatLaporan.html',context)

@login_required (login_url='login')
def TandaTerima(request,nib):
    data = PelakuUsaha.objects.get(nib=nib)
    context={
        'data':data
    }
    return render(request, 'PelakuUsaha/TandaTerima.html',context)

def generate_pdf(request,nib):
    # Fetch data from the database
    pelaku_usaha = PelakuUsaha.objects.get(nib=nib)

    # Create a new PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tanda_terima.pdf"'

    # Create the PDF content using ReportLab
    p = canvas.Canvas(response, pagesize=letter)

    letterhead_image_path = os.path.join(settings.STATIC_ROOT + '/img/logo.png')
    letterhead_image = ImageReader(letterhead_image_path)
    p.drawImage(letterhead_image, 230, 120, width=200, height=200)

    # Set the font
    p.setFont("Times-Roman", 12)
    canvas_width = p._pagesize[0]
    
    
    # title_width = p.stringWidth(title, "Times-Roman", 25)
    # title_x = (canvas_width - title_width) / 2

    # Set the font size for the secondtitle
    # p.setFont("Times-Roman", 25)
    p.setFont("Times-Bold", 18)

    # Write the second title
    second_title = "Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu"
    second_title_height = 750 # Height of the second title text
    #second_title_y = 700 - second_title_height - 10  # Adjust the value as needed
    p.drawCentredString(canvas_width / 2, second_title_height, second_title)


    # Write the third title
    p.setFont("Times-Bold", 18)
    title3 = "Kabupaten Cilacap"
    #title_height3 = 10  # Height of the title text
    title_y3 = second_title_height - 18  # Adjust the value as needed
    p.drawCentredString(canvas_width / 2, title_y3, title3)

    # Set the font size for first the title
    p.setFont("Times-Roman", 15)

    # Write the first title
    title = "Tanda Terima Input LKPM"
    title_height = title_y3 - 40 # Height of the title text
    #title_y = title_height3 - title_height - 10  # Adjust the value as needed
    p.drawCentredString(canvas_width / 2, title_height, title)

    # Reset the font size back to default
    p.setFont("Times-Roman", 12)

    # Write the data from the PelakuUsaha model
    y = 600  # Initial y-coordinate for data
    p.drawString(50, y + 20, "Data Yang Telah diinput ;")
    p.drawString(50, y, f"Nama                ")
    p.drawString(150, y, f":  {pelaku_usaha.nama_pelaku_usaha}")
    p.drawString(50, y - 20, f"NIB                     ")
    p.drawString(150, y - 20, f":  {pelaku_usaha.nib}")
    p.drawString(50, y - 40, f"Kecamatan       ")
    p.drawString(150, y - 40, f":  {pelaku_usaha.kecamatan}")
    p.drawString(50, y - 60, f"Modal              ")
    p.drawString(150, y - 60, f":  {pelaku_usaha.modal_kerja}")
    p.drawString(50, y - 80, f"Produksi        ")
    p.drawString(150, y - 80, f":  {pelaku_usaha.produksi}")
    p.drawString(50, y - 100, f"Kapasitas      ")
    p.drawString(150, y - 100, f":  {pelaku_usaha.kapasitas}")
    p.drawString(50, y - 120, f"Tanggal Input ")
    p.drawString(150, y - 120, f":  {pelaku_usaha.tanggal_input}")
    p.drawString(50, y - 140, f"No Telepon ")
    p.drawString(150, y - 140, f":  {pelaku_usaha.no_telp}")
    p.drawString(50, y - 160, f"Tenaga Kerja ")
    p.drawString(150, y - 160, f";  ")
    p.drawString(50, y - 180, f"Laki-Laki ")
    p.drawString(150, y - 180, f":  {pelaku_usaha.laki_laki}")
    p.drawString(50, y - 200, f"Perempuan ")
    p.drawString(150, y - 200, f":  {pelaku_usaha.perempuan}")



# Draw the "Permasalahan" field as multiline text
    p.drawString(50, y - 220, "Permasalahan           :")
    styles = getSampleStyleSheet()
    permasalahan = pelaku_usaha.permasalahan.replace('<br />' ,'\n' )
    permasalahan_paragraph = Paragraph(permasalahan, styles["Normal"])
    permasalahan_paragraph.wrapOn(p, 400, 250)
    permasalahan_paragraph_height = permasalahan_paragraph.wrap(400, 220)[1]  # Get the height of the multiline text
    permasalahan_y = y - 210 - permasalahan_paragraph_height  # Adjust the y-coordinate to make space for multiline text
    permasalahan_paragraph.drawOn(p, 160, permasalahan_y)



    p.showPage()
    p.save()

    return response