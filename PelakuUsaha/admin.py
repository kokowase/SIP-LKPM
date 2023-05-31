from django.contrib import admin
from .models import PelakuUsaha

# Register your models here.

class PelakuUsahaAdmin(admin.ModelAdmin):
    list_display = [
        'nib',
        'modal_kerja',
        'laki_laki',
        'perempuan',
        'kapasitas',
        'produksi'
    ]

admin.site.register(PelakuUsaha, PelakuUsahaAdmin)