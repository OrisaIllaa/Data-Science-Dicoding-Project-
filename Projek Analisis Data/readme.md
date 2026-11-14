# E-Commerce Data Analysis Dashboard

Dashboard ini dibuat menggunakan **Streamlit** untuk menampilkan hasil
analisis data e-commerce periode Januari--Desember 2017.

## 1. Persiapan

Pastikan Python sudah terpasang di komputer. Siapkan file berikut dalam
satu folder project:

``` text
Analisis data/
├── dashboard.py
└── main_data.csv
```

-   `dashboard.py` adalah file program dashboard.
-   `main_data.csv` adalah dataset yang digunakan oleh dashboard.

**Penting:** Nama file CSV harus `main_data.csv` dan letaknya harus satu
folder dengan `dashboard.py`.

## 2. Instalasi library

Buka folder project menggunakan Visual Studio Code.

Buka terminal melalui menu **Terminal → New Terminal**, kemudian
jalankan perintah berikut:

``` bash
python -m pip install streamlit pandas numpy matplotlib seaborn
```

Tunggu sampai proses instalasi selesai.

## 3. Menjalankan dashboard

Pastikan terminal berada di folder yang berisi `dashboard.py` dan
`main_data.csv`.

Jalankan perintah:

``` bash
streamlit run dashboard.py
```

Setelah perintah dijalankan:

1.  Streamlit akan memulai aplikasi dashboard.

2.  Browser biasanya akan terbuka secara otomatis.

3.  Jika browser tidak terbuka, salin alamat lokal yang ditampilkan di
    terminal, biasanya:

    `http://localhost:8501`

Dashboard dapat digunakan selama proses Streamlit masih berjalan di
terminal.

## 4. Menghentikan dashboard

Untuk menghentikan aplikasi, kembali ke terminal tempat Streamlit
berjalan, lalu tekan:

``` text
Ctrl + C
```

## 5. Jika terjadi kendala

### A. Perintah `streamlit` tidak dikenali

Coba jalankan aplikasi menggunakan:

``` bash
python -m streamlit run dashboard.py
```

### B. File `main_data.csv` tidak ditemukan

Pastikan: - File CSV bernama tepat `main_data.csv`. - File CSV berada di
folder yang sama dengan `dashboard.py`. - Nama file tidak memiliki
ekstensi ganda, misalnya `main_data.csv.csv`.

### C. Library belum terpasang

Jalankan kembali perintah instalasi library pada bagian **Instalasi
library**.

### D. Dashboard menampilkan pesan error

Periksa pesan error yang muncul di terminal VS Code. Pastikan struktur
kolom pada `main_data.csv` sesuai dengan kolom yang digunakan dalam
program.

------------------------------------------------------------------------

**Catatan:** Dashboard dijalankan secara lokal di komputer. Perintah
`streamlit run dashboard.py` digunakan untuk membuka aplikasi selama
pengembangan dan pengujian.
