from django.urls import path
from . import views

app_name = "dokumen"

urlpatterns = [
    path("", views.index, name="index"),
    path("tambah/", views.tambah_dokumen, name="tambah"),
    path("edit/<int:pk>/", views.edit_dokumen, name="edit"),
    path("hapus/<int:pk>/", views.hapus_dokumen, name="hapus"),
    path("cari/", views.cari_dokumen, name="cari"),
    path("traversal/<str:mode>/", views.traversal_view, name="traversal"),
]
