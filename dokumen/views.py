import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Dokumen
from .forms import DokumenForm, CariDokumenForm
from .bst import BinarySearchTree


def build_bst():
    """
    Membangun BST dari seluruh data dokumen yang ada di database.
    """
    tree = BinarySearchTree()
    for dok in Dokumen.objects.all():
        tree.insert(dok.to_dict())
    return tree


def bst_to_json(node):
    """Konversi BST ke JSON untuk visualisasi di frontend."""
    if node is None:
        return None
    return {
        "kode": node.data["kode"],
        "nama": node.data["nama"],
        "left": bst_to_json(node.left),
        "right": bst_to_json(node.right),
    }


def index(request):
    """Halaman utama: dashboard ringkas + traversal in-order (terurut)."""
    tree = build_bst()
    daftar_dokumen = tree.inorder()

    # Stats per kategori
    kategori_count = {}
    for dok in daftar_dokumen:
        k = dok.get("kategori", "Lainnya")
        kategori_count[k] = kategori_count.get(k, 0) + 1

    tree_json = json.dumps(bst_to_json(tree.root))

    context = {
        "daftar_dokumen": daftar_dokumen,
        "jumlah_dokumen": tree.count(),
        "tinggi_tree": tree.height(),
        "kategori_count_json": json.dumps(kategori_count),
        "tree_json": tree_json,
    }
    return render(request, "dokumen/index.html", context)


def tambah_dokumen(request):
    """Tambah dokumen baru. Validasi keunikan kode dicek lewat BST.insert()."""
    if request.method == "POST":
        form = DokumenForm(request.POST, request.FILES)
        if form.is_valid():
            dok_baru = form.save(commit=False)

            # Validasi menggunakan logika BST (selain unique constraint DB)
            tree = build_bst()
            ok, pesan = tree.insert(dok_baru.to_dict())

            if not ok:
                messages.error(request, pesan)
            else:
                dok_baru.save()
                messages.success(
                    request, f"Dokumen '{dok_baru.nama}' berhasil ditambahkan ke arsip."
                )
                return redirect("dokumen:index")
        else:
            messages.error(request, "Form tidak valid. Periksa kembali isian Anda.")
    else:
        form = DokumenForm()

    return render(request, "dokumen/form_dokumen.html", {
        "form": form,
        "judul": "Tambah Dokumen Baru",
    })


def edit_dokumen(request, pk):
    """Edit dokumen yang sudah ada."""
    dokumen = get_object_or_404(Dokumen, pk=pk)

    if request.method == "POST":
        form = DokumenForm(request.POST, request.FILES, instance=dokumen)
        if form.is_valid():
            form.save()
            messages.success(request, f"Dokumen '{dokumen.nama}' berhasil diperbarui.")
            return redirect("dokumen:index")
    else:
        form = DokumenForm(instance=dokumen)

    return render(request, "dokumen/form_dokumen.html", {
        "form": form,
        "judul": f"Edit Dokumen - {dokumen.kode}",
    })


def cari_dokumen(request):
    """
    Mencari dokumen berdasarkan kode menggunakan algoritma BST.search.
    """
    hasil = None
    langkah = None
    kode_dicari = None
    search_path = []

    if request.method == "POST":
        form = CariDokumenForm(request.POST)
        if form.is_valid():
            kode_dicari = form.cleaned_data["kode"].strip()
            tree = build_bst()
            hasil, langkah = tree.search(kode_dicari)

            # Build search path for visualization
            node = tree.root
            steps = 0
            while node:
                steps += 1
                direction = None
                if kode_dicari == node.data["kode"]:
                    search_path.append({"kode": node.data["kode"], "result": "found", "step": steps})
                    break
                elif kode_dicari < node.data["kode"]:
                    direction = "left"
                    search_path.append({"kode": node.data["kode"], "result": "go_left", "step": steps})
                    node = node.left
                else:
                    direction = "right"
                    search_path.append({"kode": node.data["kode"], "result": "go_right", "step": steps})
                    node = node.right

            if hasil is None:
                messages.warning(
                    request,
                    f"Dokumen dengan kode '{kode_dicari}' tidak ditemukan "
                    f"(dicek dalam {langkah} langkah)."
                )
            else:
                messages.success(
                    request,
                    f"Dokumen ditemukan dalam {langkah} langkah pencarian!"
                )
    else:
        form = CariDokumenForm()

    return render(request, "dokumen/cari.html", {
        "form": form,
        "hasil": hasil,
        "langkah": langkah,
        "kode_dicari": kode_dicari,
        "search_path_json": json.dumps(search_path),
    })


def hapus_dokumen(request, pk):
    """
    Menghapus dokumen. Konfirmasi dulu (GET), baru hapus (POST).
    """
    dokumen = get_object_or_404(Dokumen, pk=pk)

    if request.method == "POST":
        nama = dokumen.nama
        kode = dokumen.kode

        # Ilustrasi: jalankan delete pada BST in-memory (struktur edukatif)
        tree = build_bst()
        tree.delete(kode)

        dokumen.delete()
        messages.success(request, f"Dokumen '{nama}' (kode: {kode}) berhasil dihapus.")
        return redirect("dokumen:index")

    return render(request, "dokumen/hapus_confirm.html", {"dokumen": dokumen})


def traversal_view(request, mode):
    """
    Menampilkan hasil traversal BST sesuai mode.
    """
    tree = build_bst()

    if mode == "preorder":
        data = tree.preorder()
        judul = "Pre-Order Traversal (Root - Kiri - Kanan)"
    elif mode == "postorder":
        data = tree.postorder()
        judul = "Post-Order Traversal (Kiri - Kanan - Root)"
    else:
        data = tree.inorder()
        judul = "In-Order Traversal (Terurut Berdasarkan Kode)"
        mode = "inorder"

    return render(request, "dokumen/traversal.html", {
        "data": data,
        "judul": judul,
        "mode": mode,
        "jumlah_dokumen": tree.count(),
        "tinggi_tree": tree.height(),
    })
