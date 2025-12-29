import json
import csv
import os
from datetime import datetime


DATA_DIR = "data"
BARANG_FILE = os.path.join(DATA_DIR, "barang.json")
TRANSAKSI_FILE = os.path.join(DATA_DIR, "transaksi.csv")

APP_VERSION = "v1.1"
APP_NAME = "SISTEM KASIR UMKM IKMI CIREBON"

# =========================
# UTILITIES
# =========================
def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def input_non_empty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input tidak boleh kosong.")

def input_int(prompt: str, min_val=None, max_val=None) -> int:
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"Nilai minimal adalah {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Nilai maksimal adalah {max_val}.")
                continue
            return val
        except ValueError:
            print("Harus berupa bilangan bulat.")

def input_float(prompt: str, min_val=None) -> float:
    while True:
        try:
            val = float(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"Nilai minimal adalah {min_val}.")
                continue
            return val
        except ValueError:
            print("Harus berupa angka (contoh: 12000 atau 12000.5).")

def format_rupiah(x: float) -> str:
    return f"{int(round(x)):,}".replace(",", ".")

def garis():
    print("=" * 70)

# =========================
# DATA BARANG (JSON)
# =========================
def load_barang() -> list[dict]:
    ensure_data_dir()
    if not os.path.exists(BARANG_FILE):
        save_barang([])
        return []
    with open(BARANG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_barang(barang_list: list[dict]) -> None:
    ensure_data_dir()
    with open(BARANG_FILE, "w", encoding="utf-8") as f:
        json.dump(barang_list, f, ensure_ascii=False, indent=2)

def find_barang_by_kode(barang_list: list[dict], kode: str):
    kode = kode.strip().lower()
    for b in barang_list:
        if b["kode"].lower() == kode:
            return b
    return None

def tampil_barang(barang_list: list[dict]) -> None:
    if not barang_list:
        print("\n[!] Data barang masih kosong.\n")
        return
    print("\n=== DAFTAR BARANG ===")
    print(f"{'No':<4} {'Kode':<10} {'Nama':<25} {'Harga':>12} {'Stok':>6}")
    print("-" * 65)
    for i, b in enumerate(barang_list, start=1):
        print(f"{i:<4} {b['kode']:<10} {b['nama']:<25} {format_rupiah(b['harga']):>12} {b['stok']:>6}")
    print("-" * 65)

def tambah_barang(barang_list: list[dict]) -> None:
    print("\n=== TAMBAH BARANG ===")
    kode = input_non_empty("Kode barang: ").upper()
    if find_barang_by_kode(barang_list, kode) is not None:
        print("[!] Kode sudah ada.")
        return
    nama = input_non_empty("Nama barang: ")
    harga = input_float("Harga: ", min_val=0)
    stok = input_int("Stok awal: ", min_val=0)
    barang_list.append({"kode": kode, "nama": nama, "harga": harga, "stok": stok})
    save_barang(barang_list)
    print("[✓] Barang berhasil ditambahkan.")

def update_barang(barang_list: list[dict]) -> None:
    print("\n=== UPDATE BARANG ===")
    kode = input_non_empty("Kode barang: ").upper()
    b = find_barang_by_kode(barang_list, kode)
    if b is None:
        print("[!] Barang tidak ditemukan.")
        return
    print(f"{b['nama']} | Harga {format_rupiah(b['harga'])} | Stok {b['stok']}")
    print("1) Update harga")
    print("2) Update stok")
    pilih = input_int("Pilih: ", 1, 2)
    if pilih == 1:
        b["harga"] = input_float("Harga baru: ", min_val=0)
    else:
        delta = input_int("Perubahan stok (+/-): ")
        if b["stok"] + delta < 0:
            print("[!] Stok tidak boleh negatif.")
            return
        b["stok"] += delta
    save_barang(barang_list)
    print("[✓] Data barang diperbarui.")

def cari_barang(barang_list: list[dict]) -> None:
    keyword = input_non_empty("Cari kode/nama: ").lower()
    hasil = [b for b in barang_list if keyword in b["kode"].lower() or keyword in b["nama"].lower()]
    if not hasil:
        print("[!] Tidak ada hasil.")
        return
    tampil_barang(hasil)

# =========================
# TRANSAKSI
# =========================
def init_transaksi_file_if_needed():
    ensure_data_dir()
    if not os.path.exists(TRANSAKSI_FILE):
        with open(TRANSAKSI_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["waktu","id_transaksi","kode","nama","qty","harga","subtotal","total_transaksi"])

def generate_id_transaksi():
    return datetime.now().strftime("TRX%Y%m%d%H%M%S")

def proses_transaksi(barang_list: list[dict]) -> None:
    print("\n=== TRANSAKSI PENJUALAN ===")
    keranjang = []
    while True:
        kode = input("Kode barang (SELESAI): ").upper()
        if kode == "SELESAI":
            break
        b = find_barang_by_kode(barang_list, kode)
        if not b:
            print("[!] Barang tidak ditemukan.")
            continue
        print(f"{b['nama']} | Harga {format_rupiah(b['harga'])} | Stok {b['stok']}")
        qty = input_int("Qty: ", 1)
        if qty > b["stok"]:
            print("[!] Stok kurang.")
            continue
        subtotal = qty * b["harga"]
        keranjang.append({"kode": b["kode"], "nama": b["nama"], "qty": qty, "harga": b["harga"], "subtotal": subtotal})
        b["stok"] -= qty

    if not keranjang:
        print("[!] Transaksi dibatalkan.")
        return

    total = sum(i["subtotal"] for i in keranjang)
    bayar = input_float(f"Total Rp{format_rupiah(total)} | Bayar: ", min_val=total)
    kembalian = bayar - total

    init_transaksi_file_if_needed()
    trx_id = generate_id_transaksi()
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TRANSAKSI_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for i in keranjang:
            writer.writerow([waktu,trx_id,i["kode"],i["nama"],i["qty"],i["harga"],i["subtotal"],total])

    save_barang(barang_list)
    print(f"[✓] Transaksi berhasil | Kembalian Rp{format_rupiah(kembalian)}")

def tampil_riwayat_transaksi():
    init_transaksi_file_if_needed()
    with open(TRANSAKSI_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        print("[!] Belum ada transaksi.")
        return
    print("\n=== RIWAYAT TRANSAKSI ===")
    for r in rows[-10:]:
        print(r["waktu"], r["id_transaksi"], r["kode"], format_rupiah(float(r["subtotal"])))

def rekap_total_pendapatan():
    init_transaksi_file_if_needed()
    total = 0
    ids = set()
    with open(TRANSAKSI_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            ids.add(r["id_transaksi"])
            total += float(r["total_transaksi"])
    print("\n=== REKAP ===")
    print("Jumlah transaksi:", len(ids))
    print("Total pendapatan: Rp", format_rupiah(total))

# =========================
# MENU
# =========================
def menu():
    barang_list = load_barang()
    while True:
        garis()
        print(f"{APP_NAME} {APP_VERSION}")
        print(datetime.now().strftime("%d %B %Y %H:%M:%S"))
        print(f"Total barang terdaftar: {len(barang_list)}")
        garis()
        print("1) Tampilkan barang      - Lihat semua data barang")
        print("2) Tambah barang         - Input barang baru")
        print("3) Update barang         - Edit harga / stok")
        print("4) Cari barang           - Cari cepat barang")
        print("5) Transaksi penjualan   - Proses kasir")
        print("6) Riwayat transaksi     - Lihat transaksi")
        print("7) Rekap pendapatan      - Total penjualan")
        print("0) Keluar")
        garis()

        pilih = input_non_empty("Pilih menu: ")

        if pilih == "1":
            tampil_barang(barang_list)
        elif pilih == "2":
            tambah_barang(barang_list)
        elif pilih == "3":
            update_barang(barang_list)
        elif pilih == "4":
            cari_barang(barang_list)
        elif pilih == "5":
            proses_transaksi(barang_list)
            barang_list = load_barang()
        elif pilih == "6":
            tampil_riwayat_transaksi()
        elif pilih == "7":
            rekap_total_pendapatan()
        elif pilih == "0":
            if input("Yakin keluar? (y/n): ").lower() == "y":
                print("Terima kasih 🙏")
                break
        else:
            print("[!] Menu tidak valid.")

if __name__ == "__main__":
    menu()
