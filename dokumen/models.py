from django.db import models


class Dokumen(models.Model):
    """
    Model dokumen yang disimpan di database (SQLite).
    Field 'kode' bersifat unik karena digunakan sebagai
    kunci pengurutan pada Binary Search Tree.
    """

    KATEGORI_CHOICES = [
        ("Surat", "Surat"),
        ("Laporan", "Laporan"),
        ("Kontrak", "Kontrak"),
        ("Sertifikat", "Sertifikat"),
        ("Lainnya", "Lainnya"),
    ]

    kode = models.CharField(max_length=20, unique=True, verbose_name="Kode Dokumen")
    nama = models.CharField(max_length=150, verbose_name="Nama Dokumen")
    kategori = models.CharField(
        max_length=50, choices=KATEGORI_CHOICES, default="Lainnya"
    )
    tanggal_upload = models.DateField(verbose_name="Tanggal Upload")
    file = models.FileField(
        upload_to="dokumen_files/", blank=True, null=True, verbose_name="File Dokumen"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["kode"]

    def __str__(self):
        return f"{self.kode} - {self.nama}"

    def to_dict(self):
        """Konversi ke dict untuk dimasukkan ke BST."""
        return {
            "id": self.id,
            "kode": self.kode,
            "nama": self.nama,
            "kategori": self.kategori,
            "tanggal": self.tanggal_upload.strftime("%d-%m-%Y") if self.tanggal_upload else "-",
            "file_url": self.file.url if self.file else None,
        }
