"""
============================================================
 STRUKTUR DATA: BINARY SEARCH TREE (BST)
 Untuk Sistem Arsip Dokumen Digital
============================================================
Modul ini berisi implementasi murni struktur data BST yang
digunakan untuk mengelola data dokumen berdasarkan field
'kode' sebagai kunci pengurutan.

Operasi yang didukung:
 - insert(dok)        : menambahkan dokumen baru
 - search(kode)        : mencari dokumen, mengembalikan node + jumlah langkah
 - delete(kode)        : menghapus dokumen
 - inorder()           : traversal terurut (ascending berdasarkan kode)
 - preorder()          : traversal pre-order
 - postorder()         : traversal post-order
 - count()             : jumlah total node
 - height()            : tinggi tree
============================================================
"""


class Node:
    """Node BST yang menyimpan satu data dokumen (dict)."""

    def __init__(self, data: dict):
        self.data = data          # dict: {kode, nama, kategori, tanggal}
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary Search Tree berdasarkan field 'kode' (string)."""

    def __init__(self):
        self.root = None

    # ------------------------------------------------------
    # INSERT
    # ------------------------------------------------------
    def insert(self, data: dict):
        """Menambahkan dokumen baru ke BST berdasarkan kode."""
        if self.root is None:
            self.root = Node(data)
            return True, "Dokumen berhasil ditambahkan."

        return self._insert_rec(self.root, data)

    def _insert_rec(self, node: Node, data: dict):
        if data["kode"] == node.data["kode"]:
            return False, f"Kode dokumen '{data['kode']}' sudah ada."

        if data["kode"] < node.data["kode"]:
            if node.left is None:
                node.left = Node(data)
                return True, "Dokumen berhasil ditambahkan."
            return self._insert_rec(node.left, data)
        else:
            if node.right is None:
                node.right = Node(data)
                return True, "Dokumen berhasil ditambahkan."
            return self._insert_rec(node.right, data)

    # ------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------
    def search(self, kode: str):
        """
        Mencari dokumen berdasarkan kode.
        Mengembalikan tuple: (node_data atau None, jumlah_langkah)
        """
        return self._search_rec(self.root, kode, 0)

    def _search_rec(self, node, kode, langkah):
        if node is None:
            return None, langkah

        langkah += 1
        if kode == node.data["kode"]:
            return node.data, langkah
        elif kode < node.data["kode"]:
            return self._search_rec(node.left, kode, langkah)
        else:
            return self._search_rec(node.right, kode, langkah)

    # ------------------------------------------------------
    # DELETE
    # ------------------------------------------------------
    def delete(self, kode: str):
        """Menghapus dokumen berdasarkan kode. Return (berhasil: bool)."""
        self.root, deleted = self._delete_rec(self.root, kode)
        return deleted

    def _delete_rec(self, node, kode):
        if node is None:
            return node, False

        if kode < node.data["kode"]:
            node.left, deleted = self._delete_rec(node.left, kode)
            return node, deleted
        elif kode > node.data["kode"]:
            node.right, deleted = self._delete_rec(node.right, kode)
            return node, deleted
        else:
            # Node ditemukan
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True

            # Kedua anak ada -> cari successor (min dari subtree kanan)
            successor = self._find_min(node.right)
            node.data = successor.data
            node.right, _ = self._delete_rec(node.right, successor.data["kode"])
            return node, True

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    # ------------------------------------------------------
    # TRAVERSAL
    # ------------------------------------------------------
    def inorder(self):
        """Kiri - Root - Kanan (terurut ascending berdasarkan kode)."""
        hasil = []
        self._inorder_rec(self.root, hasil)
        return hasil

    def _inorder_rec(self, node, hasil):
        if node:
            self._inorder_rec(node.left, hasil)
            hasil.append(node.data)
            self._inorder_rec(node.right, hasil)

    def preorder(self):
        """Root - Kiri - Kanan."""
        hasil = []
        self._preorder_rec(self.root, hasil)
        return hasil

    def _preorder_rec(self, node, hasil):
        if node:
            hasil.append(node.data)
            self._preorder_rec(node.left, hasil)
            self._preorder_rec(node.right, hasil)

    def postorder(self):
        """Kiri - Kanan - Root."""
        hasil = []
        self._postorder_rec(self.root, hasil)
        return hasil

    def _postorder_rec(self, node, hasil):
        if node:
            self._postorder_rec(node.left, hasil)
            self._postorder_rec(node.right, hasil)
            hasil.append(node.data)

    # ------------------------------------------------------
    # STATISTIK
    # ------------------------------------------------------
    def count(self):
        return self._count_rec(self.root)

    def _count_rec(self, node):
        if node is None:
            return 0
        return 1 + self._count_rec(node.left) + self._count_rec(node.right)

    def height(self):
        return self._height_rec(self.root)

    def _height_rec(self, node):
        if node is None:
            return -1
        return 1 + max(self._height_rec(node.left), self._height_rec(node.right))
