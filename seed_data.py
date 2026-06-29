"""
Script untuk mengisi data dummy ke database ArsipKu.

Cara pakai:
  Letakkan file ini di dalam folder arsip_django/ (sejajar dengan manage.py)
  Lalu jalankan:
    python manage.py shell < seed_data.py
  ATAU:
    python seed_data.py   (jika Django sudah dikonfigurasi)
"""
import os, django, sys

# Setup Django jika dijalankan langsung (bukan via shell)
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arsipproject.settings")
    django.setup()

from dokumen.models import Dokumen

print("🗑️  Menghapus data lama...")
Dokumen.objects.all().delete()

data_dummy = [
    # (kode, nama, kategori, tanggal_upload)
    # Kode sengaja TIDAK urut — ini penting untuk menunjukkan BST bekerja!
    # BST akan menyusun ulang secara otomatis.
    ("DOC-002", "Surat Keputusan Pengangkatan Karyawan Baru",     "Surat",      "2024-01-15"),
    ("DOC-007", "Laporan Keuangan Triwulan Q1 2024",              "Laporan",    "2024-03-31"),
    ("DOC-004", "Kontrak Kerja Sama PT Maju Jaya",                "Kontrak",    "2024-02-10"),
    ("DOC-001", "Surat Undangan Rapat Koordinasi Bulanan",        "Surat",      "2024-01-05"),
    ("DOC-010", "Sertifikat ISO 9001:2015 Perusahaan",            "Sertifikat", "2023-12-20"),
    ("DOC-005", "Laporan Evaluasi Kinerja Semester I",            "Laporan",    "2024-06-30"),
    ("DOC-003", "Surat Pemberitahuan Perubahan Jadwal",           "Surat",      "2024-01-20"),
    ("DOC-009", "Kontrak Sewa Gedung Kantor 2024",                "Kontrak",    "2024-01-01"),
    ("DOC-006", "Sertifikat Penghargaan Pelayanan Terbaik",       "Sertifikat", "2024-04-17"),
    ("DOC-008", "Laporan Audit Internal Semester II",             "Laporan",    "2024-07-15"),
    ("DOC-012", "Surat Izin Operasional Cabang Baru",             "Surat",      "2024-08-01"),
    ("DOC-011", "Nota Kesepahaman MOU Bidang Teknologi",          "Kontrak",    "2024-05-22"),
]

print("📂 Menambahkan data dummy...")
for kode, nama, kategori, tgl in data_dummy:
    Dokumen.objects.create(kode=kode, nama=nama, kategori=kategori, tanggal_upload=tgl)
    print(f"  ✅ {kode} — {nama[:50]}")

print(f"\n🎉 Selesai! Total: {Dokumen.objects.count()} dokumen")
