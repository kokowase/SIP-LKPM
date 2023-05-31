from django.db import models

# Create your models here.

class PelakuUsaha(models.Model):
    kecamatan = models.CharField(max_length=100, null=True)
    nib = models.CharField(max_length=100, null=False)
    modal_kerja = models.IntegerField(null=True, blank=True)
    laki_laki = models.IntegerField(blank=True, null=True)
    perempuan = models.IntegerField(blank=True, null=True)
    produksi = models.CharField(max_length=100,blank=True, null=True)
    tanggal_input = models.DateField(auto_now=True,blank=True,null=True)
    kapasitas = models.CharField(max_length=20, null=True)
    nama_pelaku_usaha = models.CharField(max_length=100,null=True)
    no_telp = models.CharField(max_length=100)
