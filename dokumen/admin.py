from django.contrib import admin
from .models import Dokumen


@admin.register(Dokumen)
class DokumenAdmin(admin.ModelAdmin):
    list_display = ("kode", "nama", "kategori", "tanggal_upload")
    search_fields = ("kode", "nama")
    list_filter = ("kategori",)
    ordering = ("kode",)
