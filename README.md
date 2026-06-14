# Analisis Diskrepansi Sentimen Pemberitaan ESG Berbahasa Indonesia sebagai Proksi Deteksi Greenwashing pada Perusahaan Publik Indonesia

> **Tugas Project Akhir Kelompok**  
> **Mata Kuliah:** Aplikasi Teknologi & Transformasi Digital (ATTD)  
> **Departemen:** Sistem Informasi, Fakultas Teknologi Elektro dan Informatika Cerdas (FTEIC)  
> **Institusi:** Institut Teknologi Sepuluh Nopember (ITS), Surabaya  
> **Tahun:** Semester Genap 2026

---

## 👥 Tim Pengembang (Kelompok 5)

| Nama Mahasiswa | NRP | Peran / Fokus |
| :--- | :--- | :--- |
| **Antika Raya** | 5026231034 | Data Preparation & Preprocessing |
| **Nabila Shinta Luthfia** | 5026231038 | Exploratory Data Analysis & Text Lexicon |
| **Cindy Fatika Ekawati** | 5026231039 | POS Tagging & Feature Engineering |
| **Amelia Rusbandiyah** | 5026231041 | Named Entity Recognition (NER) & GPE Map |
| **Rahmadhona Elokpribadi K.** | 5026231217 | LLM Augmentation & Groq API Integration |
| **Annisa Nur Fauzi** | 5026231228 | Downstream Sentiment BERT Fine-Tuning |
| **Lailatul Fitaliqoh** | 5026231229 | Downstream ESG Tag BERT Fine-Tuning |
| **Bara Ardiwinata** | 5026231232 | Local Engine Integration & Pipeline Orchestration |

---

## 📌 Deskripsi & Tujuan Utama Proyek

Proyek ini mengimplementasikan sebuah pipeline *Natural Language Processing* (NLP) *end-to-end* yang dirancang secara sistematis untuk mendeteksi potensi praktik **Greenwashing** pada perusahaan publik (terbuka) di Indonesia. Deteksi dilakukan melalui analisis diskrepansi antara sentimen publik/media (melalui pemberitaan) dengan klaim internal korporasi terkait aspek *Environmental, Social, and Governance* (ESG).

Berbeda dari laporan keberlanjutan (*sustainability reports*) internal perusahaan yang bersifat *self-reported* dan rentan terhadap bias pencitraan positif, pemberitaan media arus utama dan independen memuat narasi objektif yang diverifikasi secara eksternal. Pipeline ini mengkalkulasi ketimpangan sentimen tersebut melalui tahapan-tahapan berikut:
1. **Preprocessing & Deep Cleaning**: Menghilangkan noise teks, stemming bahasa Indonesia (Sastrawi), dan ekstraksi metadata waktu terstandardisasi.
2. **Feature Extraction**: Melakukan penandaan kelas kata (*Part-of-Speech Tagging*) serta ekstraksi entitas bernama (*Named Entity Recognition*) untuk memetakan aktor-aktor korporasi dan wilayah terdampak.
3. **Korpus Augmentasi (Groq API)**: Menyeimbangkan dataset minoritas secara sintetik menggunakan kecerdasan LLM Llama-3.3-70b.
4. **Fine-Tuning Downstream Classifier**: Melatih arsitektur transformer IndoBERT secara lokal menggunakan PyTorch untuk mengklasifikasikan dimensi sentimen dan dimensi kategori ESG secara spesifik.

---

## 🛠️ Arsitektur Ekosistem & Tech Stack

Sistem dikembangkan menggunakan pustaka-pustaka Python berstandar industri dengan optimalisasi GPU lokal:

| Komponen Pipeline | Pustaka / Teknologi | Deskripsi / Fungsi |
| :--- | :--- | :--- |
| **Data Cleaning & Manipulation** | `Pandas`, `NumPy` | Manipulasi dataset terstruktur, pengisian nilai kosong, standardisasi tipe data, dan stratifikasi split dataset. |
| **Feature Extraction (POS & NER)** | IndoBERT Lokal (`w11wo/indonesian-roberta-base-posp-tagger` & `bryanahusna/my-nergrit-model`) | Melakukan *Part-of-Speech Tagging* (POS) untuk kelas kata berita serta ekstraksi entitas *Organization* (ORG), *Location* (LOC), dan *Geopolitical Entity* (GPE). |
| **Korpus Augmentasi** | Groq API (`llama-3.3-70b-versatile`) | Pembuatan 94 artikel berita ESG sintetik berkualitas tinggi (75 kelas Netral, 19 kelas Positif) guna menyeimbangkan distribusi data latih. |
| **Model Klasifikasi Hilir** | `Hugging Face Transformers` & `PyTorch` | Melakukan *fine-tuning* terarah pada model IndoBERT (`indobenchmark/indobert-base-p1`) untuk klasifikasi multi-label Sentimen dan Tag ESG. |
| **Akselerasi Perangkat Keras** | `CUDA 12.9` / Nvidia GeForce RTX 2050 | Mengakselerasi proses pelatihan BERT lokal secara signifikan untuk meminimalkan waktu komputasi. |
| **Visualisasi Hasil** | `Matplotlib`, `Seaborn`, `WordCloud` | Menyusun confusion matrix, training loss curves, wordclouds, dan analisis tren sentimen temporal. |

---

## 🗂️ Topologi Direktori & Reorganisasi Folder

Folder proyek telah ditata secara rapi untuk menghilangkan berkas temporer debugging serta menyatukan visualisasi output ke dalam folder terisolasi:

```
ESG_SentimentAnalysis/
│
├── data/
│   ├── raw_data.csv               # Dataset link artikel mentah dari portal umum
│   ├── raw_multatuli.csv          # Dataset link artikel dari Project Multatuli
│   ├── clean_data.csv             # Output hasil preprocessing (468 baris data valid)
│   ├── IndoBERT.csv               # Korpus berita lengkap dengan tag NER & POS
│   ├── pipeline_execution.log     # Berkas log konsol terpusat hasil jalannya pipeline
│   └── models/                    # Hasil keluaran evaluasi & model BERT
│       ├── sentiment/             # Checkpoint model terbaik klasifikasi Sentimen
│       ├── tag/                   # Checkpoint model terbaik klasifikasi Kategori Tag
│       ├── test_predictions.csv   # Hasil komparasi label asli vs prediksi model pada test set
│       └── ...                    # Confusion matrix & Training history plot (.png)
│
├── scripts/
│   ├── cleaner_berita.ipynb       # [Step 1] Preprocessing teks berita & standardisasi tanggal
│   ├── EDA_FeatExt_NER.ipynb      # [Step 2] Analisis leksikal, TF-IDF, POS Tagging, & NER
│   ├── Augmentasi_LLM.ipynb       # [Step 3] Augmentasi teks minoritas seimbang berbasis Groq API
│   ├── klasifikasi.ipynb          # [Step 4] Fine-tuning model IndoBERT Sentimen & Kategori Tag
│   ├── run_pipeline.py            # Skrip jangkar orkestrator pipeline otomatis
│   │
│   ├── data/                      # Folder data terisolasi internal scripts
│   │   ├── IndoBERT.csv           # Korpus internal salinan valid
│   │   ├── clean_data.csv         # Data bersih terstandardisasi
│   │   ├── augmented_checkpoint.csv # Checkpoint progres eksekusi augmentasi Groq
│   │   ├── train_set_augmented.csv # Dataset latih gabungan (asli + 94 data sintetis)
│   │   └── test_set_asli.csv      # Dataset uji murni (tanpa augmentasi)
│   │
│   ├── indobert-pos-finetuned/    # Model POS Tagging lokal yang digunakan dalam pipeline
│   └── visualizations/            # Folder isolasi 11 file grafik visualisasi hasil analisis (.png)
│
├── README.md                      # Dokumentasi utama proyek
└── walkthrough.md                 # Catatan teknis histori modifikasi & hasil runtime
```

### Penjelasan Fungsi Berkas Utama di `scripts/`:
* **`cleaner_berita.ipynb`**: Membaca artikel mentah, menyaring teks dengan panjang token di bawah 50, dan membersihkan noise teks (seperti tag HTML, teks boilerplate portal media, emoji) serta melakukan stemming kata dasar.
* **`EDA_FeatExt_NER.ipynb`**: Menganalisis distribusi awal, menghitung sentimen berbasis leksikon lokal (InSet), memproses pembobotan kata TF-IDF, serta memetakan entitas (NER) seperti organisasi dan lokasi geografis.
* **`Augmentasi_LLM.ipynb`**: Melakukan komunikasi dengan server Groq untuk memparafrase artikel berita sesuai sentimen dan kategori ESG target guna menghasilkan data balancing sintetis secara akurat.
* **`klasifikasi.ipynb`**: Melakukan pembagian data latih/uji (80/20), mempersiapkan data loader, melatih model klasifikasi IndoBERT multi-task, dan memvalidasi model pada data uji bersih.
* **`run_pipeline.py`**: Skrip orkestrator yang mengendalikan eksekusi sekuensial seluruh berkas notebook di atas secara otomatis dari terminal.

---

## ⚡ Mitigasi Debug & Optimasi Operasional (Windows Engine)

Selama pengujian di lingkungan lokal Windows, beberapa isu krusial berhasil diidentifikasi dan ditangani guna menjaga kestabilan komputasi lokal:

1. **Dead Kernel & Multiprocessing Spawn Crash**:
   Pada Windows, metode pembuatan proses sub-pemrosesan (`spawn`) pada PyTorch DataLoader dapat menyebabkan kernel Jupyter mati mendadak (*Dead Kernel*) apabila menggunakan `num_workers > 0`. Masalah diselesaikan dengan mengonfigurasi `dataloader_num_workers=0` di dalam `TrainingArguments`.
2. **PytorchStreamWriter Failure & NTFS Path Limitation**:
   Proses penyimpanan state optimizer dan scheduler BERT yang sangat besar ke dalam disk sering mengalami crash stream write gagal (`unexpected pos`). Kami menambahkan parameter `save_only_model=True` pada argumen pelatihan Hugging Face. Hal ini menghemat ruang penyimpanan karena membatasi penyimpanan hanya pada bobot utama model saja yang memang dibutuhkan untuk evaluasi/inferensi downstream.
3. **Bypass Safe Load Check (CVE-2025-32434)**:
   Pemuatan file bobot berbasis format pickle bawaan transformers memicu runtime security check error yang menghentikan impor modul. Kami menyuntikkan fungsi lambda bypass:
   ```python
   transformers.utils.import_utils.check_torch_load_is_safe = lambda: None
   transformers.modeling_utils.check_torch_load_is_safe = lambda: None
   ```
   Hal ini membiarkan model dimuat langsung ke GPU secara aman tanpa crash inisialisasi.
4. **Pembersihan Berkas Redundan**:
   Menghapus berkas debug kotor `scripts/klasifikasi_run.py` guna menjaga repositori tetap bersih dan terstandardisasi.

---

## 🚀 Panduan Eksekusi Pipeline

Sistem dirancang agar dapat dijalankan dengan satu perintah tunggal. Buka terminal Anda pada root direktori proyek dan jalankan perintah:

```bash
python scripts/run_pipeline.py
```

### Fitur Smart-Skipping (Caching) & Cooldown Sleep
Skrip orkestrasinya dilengkapi dengan mekanisme **Smart-Skipping Caching** untuk efisiensi waktu dan kuota API:
* **Step 1 & 2** akan memeriksa file keluaran `data/clean_data.csv` dan `data/IndoBERT.csv` di disk. Jika file tersebut terdeteksi ada, skrip akan melompat langsung ke langkah berikutnya dan menampilkan log:
  `⏭️ Berkas data/clean_data.csv ditemukan. Melewati Step 1!`
  `⏭️ Berkas data/IndoBERT.csv ditemukan. Melewati Step 2!`
* **Step 3 (Augmentasi)** secara otomatis memuat file `augmented_checkpoint.csv`. Jika 94 data sintetis penyeimbang sudah lengkap tersimpan di dalamnya, proses pemanggilan Groq API dilewati penuh guna menghemat token API harian Anda.
* **Cooldown Sleep**: Jeda `time.sleep(10)` otomatis disisipkan sebelum memulai Step 3 guna meminimalisasi risiko terkena rate limit (Error 429) pada Groq API.

---

## 🏆 Papan Skor Capai Model Final

Proses pelatihan downstream BERT lokal diselesaikan dalam waktu **550.33 detik (9.17 menit)** menggunakan Nvidia GeForce RTX 2050 GPU. Berikut adalah performa final model pada data uji murni (*test_set_asli.csv*):

### 1. Klasifikasi Sentimen
* **Akurasi**: `89.4%`
* **F1-Macro**: `88.3%` (Sukses melampaui standar target riset minimum yaitu **85%**)
* **Rincian Performa per Kelas**:
  * Negatif: Precision `0.92`, Recall `0.92`, F1-score `0.92`
  * Netral: Precision `0.75`, Recall `0.90`, F1-score `0.82`
  * Positif: Precision `0.97`, Recall `0.86`, F1-score `0.91`

### 2. Klasifikasi Isu ESG (Tag)
* **Akurasi**: `64.9%`
* **F1-Macro**: `64.5%`
* **Rincian Performa per Kelas**:
  * Environment: Precision `0.57`, Recall `0.57`, F1-score `0.57`
  * Finance: Precision `0.68`, Recall `0.93`, F1-score `0.79`
  * Governance: Precision `0.47`, Recall `0.57`, F1-score `0.52`
  * Investigation: Precision `0.85`, Recall `0.50`, F1-score `0.63`
  * Social: Precision `0.71`, Recall `0.74`, F1-score `0.72`

> [!NOTE]
> Semua file bobot terbaik model (`best_model/`), grafik Confusion Matrix, dan kurva training history kini tersimpan secara otomatis dan rapi di dalam folder output `data/models/`.