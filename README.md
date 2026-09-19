# 🏷️ Data Labeling & Sentiment Classifier

Aplikasi simulasi proses kerja **Data Annotator/Data Labeler**: memberi label manual pada data teks, lalu membandingkannya dengan hasil prediksi otomatis dari sistem AI sederhana (rule-based sentiment classifier).

Project ini dibuat sebagai portofolio yang relevan dengan minat karier di bidang **Data Annotation & AI**, sekaligus melanjutkan proses belajar Software Engineering.

## Fitur

- **Labeling manual** — beri label (positif/negatif/netral) pada tiap data ulasan, mensimulasikan pekerjaan data annotator sesungguhnya
- **Prediksi otomatis** — sistem klasifikasi sentimen berbasis lexicon (kamus kata) Bahasa Indonesia
- **Perbandingan hasil** — lihat akurasi, dan data mana saja yang labelnya berbeda antara manual vs otomatis
- **Export hasil** — download hasil labeling sebagai file CSV

## Tech Stack

- **Python 3**
- **Pandas** — pengolahan data
- **Streamlit** — antarmuka web interaktif
- Custom **lexicon-based sentiment classifier** (dibuat dari nol, tanpa library eksternal)

## Struktur Project

```
sentiment_labeling/
├── data_ulasan.csv     # Dataset contoh (30 ulasan produk, data dummy)
├── classifier.py       # Modul sentiment classifier berbasis lexicon
├── app.py               # Aplikasi web Streamlit
├── requirements.txt     # Daftar library yang dibutuhkan
└── README.md
```

## Cara Menjalankan

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Jalankan aplikasi:
   ```
   streamlit run app.py
   ```

3. (Opsional) Test classifier secara terpisah lewat command line:
   ```
   python classifier.py
   ```

## Cara Kerja Classifier

Classifier ini menggunakan pendekatan **lexicon-based** — salah satu metode paling dasar dalam Natural Language Processing (NLP):

1. Teks dipecah menjadi kata-kata (tokenization)
2. Setiap kata dicocokkan dengan kamus kata positif dan kata negatif
3. Kata negasi (seperti "tidak", "bukan") dicek untuk membalik makna kata setelahnya
4. Skor akhir dihitung, lalu ditentukan label: positif, negatif, atau netral

### Keterbatasan (dan kenapa ini penting dipahami)

Dengan dataset contoh di project ini, classifier mencapai akurasi sekitar **80%** dibanding label manual. Beberapa kasus yang salah diprediksi, misalnya:

- Kalimat netral seperti *"sesuai standar, tidak ada yang istimewa"* — kata negasi "tidak" berjarak lebih dari 1 kata dari kata yang dinegasikan ("istimewa"), sehingga tidak terdeteksi oleh sistem
- Kalimat yang tidak mengandung kata dari kamus sama sekali (misal *"baru terima, belum dipakai lama"*) tidak bisa diklasifikasi dengan akurat

Ini adalah keterbatasan umum dari pendekatan rule-based, dan menjadi alasan kenapa di industri nyata biasanya digunakan model machine learning (yang dilatih dari data berlabel dalam jumlah besar) untuk hasil yang lebih akurat — di sinilah pekerjaan **Data Annotator** menjadi penting, karena model ML butuh data berlabel manusia untuk belajar.

## Data

Dataset berisi 30 ulasan produk (data dummy, berbahasa Indonesia, bertema produk kayu). Kolom:
- `id` — nomor urut
- `teks_ulasan` — isi ulasan
- `label_asli` — label sentimen (bisa diedit manual lewat aplikasi)

## Pengembangan Selanjutnya (Ide)

- Perbaiki deteksi negasi agar bisa menjangkau lebih dari 1 kata
- Perluas kamus kata positif/negatif
- Ganti dengan model machine learning yang dilatih dari data berlabel (misalnya Naive Bayes atau model berbasis transformer)
- Tambah fitur upload dataset sendiri (bukan cuma data bawaan)

---

*Project ini dibuat sebagai bagian dari proses belajar Software Engineering dan eksplorasi bidang Data Annotation/AI.*
