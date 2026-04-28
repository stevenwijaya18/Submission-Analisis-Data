# Data Analysis Dashboard ✨

Ini adalah dashboard interaktif berbasis web yang dibangun menggunakan **Streamlit** untuk memvisualisasikan hasil pemrosesan dan analisis data Polusi Udara (PM2.5) di Beijing. Proyek ini merupakan tugas akhir kapabilitas sertifikasi Dicoding.

## Setup Lingkungan (Local) - Windows

1. Buka Terminal / Command Prompt Anda.
2. Navigasikan (cd) terminal Anda ke dalam *root folder* dari sistem (`Submission_Analisis Data/`).
3. Buat dan aktifkan *Virtual Environment* Anda dengan perintah berikut:
   ```bash
   py -m venv env
   .\env\Scripts\activate
   ```
4. Install library yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan Dashboard Streamlit

Didalam *environment* yang sudah aktif tadi, jalankan aplikasi web menggunakan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan otomatis terbuka dan diluncurkan di Browser default Anda, biasanya pada link `http://localhost:8501`.

## Struktur Direktori
* `/dashboard` - Folder penampung file dashboard eksekusi (`dashboard.py`) beserta aset dataset bersih (`main_data.csv`).
* `/data` - Dataset cuaca/polusi asli.
* `Proyek_Analisis_Data.ipynb` - Proses end-to-end data mulai dari assessing, cleaning, hingga Exploratory Data Analysis dan visualisasi.
* `requirements.txt` - File esensial yang diperlukan untuk Deployment ke server cloud.
