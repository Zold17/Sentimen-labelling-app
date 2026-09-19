"""
Modul Sentiment Classifier Sederhana (Lexicon-Based)
------------------------------------------------------
Menggunakan pendekatan kamus kata (lexicon) untuk memprediksi sentimen
teks Bahasa Indonesia. Setiap kata dicocokkan dengan daftar kata
positif dan negatif, lalu dihitung skornya.

Ini adalah pendekatan paling dasar dalam NLP/text classification,
sering dipakai sebagai baseline sebelum menggunakan model machine
learning yang lebih kompleks.
"""

import re

# Kamus kata positif dan negatif (Bahasa Indonesia)
# Bisa terus ditambah/dikembangkan sesuai kebutuhan domain
KATA_POSITIF = {
    "bagus", "puas", "cepat", "aman", "elegan", "cocok", "recommended",
    "ramah", "responsif", "sesuai", "kokoh", "halus", "rapi", "terima kasih",
    "istimewa", "solid", "memuaskan", "berkualitas", "oke", "mantap",
    "keren", "terbaik", "suka", "senang", "top", "worth", "nyaman",
}

KATA_NEGATIF = {
    "rusak", "kecewa", "lama", "retak", "buruk", "kasar", "mahal",
    "lambat", "penyok", "mengecewakan", "jelek", "cacat", "salah",
    "gagal", "komplain", "kurang", "tidak sesuai", "kecil", "serpihan",
    "biasa saja", "tidak akan beli lagi",
}

# Kata negasi yang bisa membalik makna (contoh: "tidak bagus" jadi negatif)
KATA_NEGASI = {"tidak", "bukan", "kurang", "belum"}


def bersihkan_teks(teks):
    """Ubah ke huruf kecil dan hapus tanda baca."""
    teks = teks.lower()
    teks = re.sub(r"[^\w\s]", "", teks)
    return teks


def prediksi_sentimen(teks):
    """
    Memprediksi sentimen dari sebuah teks: 'positif', 'negatif', atau 'netral'.
    Mengembalikan tuple (label, skor) di mana skor > 0 condong positif,
    skor < 0 condong negatif, skor == 0 netral.
    """
    teks_bersih = bersihkan_teks(teks)
    kata_kata = teks_bersih.split()

    skor = 0
    for i, kata in enumerate(kata_kata):
        # Cek apakah kata tepat sebelumnya adalah kata negasi
        # (pendekatan sederhana; negasi yang berjarak lebih dari 1 kata
        # seperti "tidak ada yang istimewa" tidak terdeteksi -- ini
        # keterbatasan yang wajar untuk lexicon-based approach)
        negasi = i > 0 and kata_kata[i - 1] in KATA_NEGASI

        if kata in KATA_POSITIF:
            skor += -1 if negasi else 1
        elif kata in KATA_NEGATIF:
            skor += 1 if negasi else -1

    if skor > 0:
        label = "positif"
    elif skor < 0:
        label = "negatif"
    else:
        label = "netral"

    return label, skor


if __name__ == "__main__":
    # Contoh penggunaan / testing cepat
    contoh_teks = [
        "Produk sangat bagus dan pengiriman cepat",
        "Barang rusak, saya sangat kecewa",
        "Sesuai standar, tidak ada yang istimewa",
        "Kualitas tidak bagus, mengecewakan",
    ]

    for teks in contoh_teks:
        label, skor = prediksi_sentimen(teks)
        print(f"'{teks}' -> {label} (skor: {skor})")
