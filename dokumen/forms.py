from django import forms
from .models import Dokumen


class DokumenForm(forms.ModelForm):
    """Form untuk tambah/edit dokumen."""

    class Meta:
        model = Dokumen
        fields = ["kode", "nama", "kategori", "tanggal_upload", "file"]
        widgets = {
            "kode": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Contoh: DOC001"
            }),
            "nama": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nama dokumen"
            }),
            "kategori": forms.Select(attrs={"class": "form-select"}),
            "tanggal_upload": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class CariDokumenForm(forms.Form):
    """Form sederhana untuk pencarian dokumen berdasarkan kode."""

    kode = forms.CharField(
        max_length=20,
        label="Kode Dokumen",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Masukkan kode dokumen, contoh: DOC001"
        }),
    )
