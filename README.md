# 🧾 Mini Project Kasir UMKM (Python CLI)

## 📌 Deskripsi
Mini Project Kasir UMKM adalah aplikasi kasir sederhana berbasis **Python (Command Line Interface)** yang dibuat untuk memenuhi tugas **Algoritma dan Pemrograman Dasar (Alpro)**.  
Aplikasi ini digunakan untuk mengelola data barang, melakukan transaksi penjualan, mencetak struk ke layar, serta menyimpan dan membaca riwayat transaksi dari file.

---

## 🎯 Tujuan Pembuatan
- Menerapkan konsep dasar algoritma dan pemrograman
- Mengimplementasikan struktur kontrol, fungsi, array, dan file handling
- Melatih logika pemrograman melalui studi kasus sistem kasir UMKM

---

## ⚙️ Fitur Utama

### 1️⃣ Master Barang
- Tambah barang (kode, nama, harga, stok)
- Tampilkan daftar barang
- Update harga dan stok barang
- Pencarian barang berdasarkan kode atau nama

### 2️⃣ Transaksi Penjualan
- Input item (kode barang dan jumlah)
- Hitung subtotal dan total transaksi
- Diskon sederhana (opsional)
- Stok barang berkurang otomatis

### 3️⃣ Struk & Riwayat Transaksi
- Cetak struk transaksi ke layar
- Simpan transaksi ke file CSV
- Tampilkan riwayat transaksi
- Rekap total pendapatan

---

## 🧠 Konsep Pemrograman yang Digunakan
- **Struktur kontrol**: `if-else`, `for`, `while`
- **Array / List**: penyimpanan data barang dan transaksi
- **Fungsi**: modularisasi program (lebih dari 5 fungsi)
- **String**: validasi input dan pencarian data
- **File Handling**:
  - JSON → data barang
  - CSV → riwayat transaksi
- **Debugging & Testing**: pengujian input, stok, dan transaksi

---

## 📁 Struktur Folder

MINI_PROJECT_ALPRO/
├── data/
│   ├── barang.json
│   └── riwayat_transaksi.csv
├── docs/
│   ├── flowchart.png
│   └── laporan.docx
├── web/
│   └── index.html
├── application.py
├── README.md
└── vercel.json


---

## ▶️ Cara Menjalankan Program

### 1️⃣ Jalankan Aplikasi Kasir (CLI)
Pastikan Python sudah terinstall.

```bash
py application.py
