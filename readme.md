# 🚌 KaNgkot - Sistem Penyewaan Angkot (Kamal Angkot)

Sistem informasi berbasis web untuk manajemen penyewaan armada angkot. Proyek ini dibangun untuk memenuhi Tugas Akhir Basis Data Lanjut dengan fokus pada implementasi CRUD, Relasi Database, dan Deployment.

**🌐 Live Demo:** [https://kamalinfokan.pythonanywhere.com](https://kamalinfokan.pythonanywhere.com)

## 🚀 Fitur Utama

### 👮 Admin Side
- **Dashboard Tabular:** Ringkasan data armada angkot.
- **Manajemen Armada:** CRUD (Create, Read, Update, Delete) data angkot (Plat Nomor, Jurusan, Harga, Status).
- **Monitoring Status:** Melihat status ketersediaan armada secara real-time.

### 👤 User Side
- **Registrasi Akun:** Memungkinkan penumpang baru mendaftar.
- **Grid View Dashboard:** Tampilan daftar angkot yang interaktif dan responsif.
- **Sistem Booking:** Melakukan pemesanan angkot berdasarkan tanggal.

## 🛠️ Teknologi yang Digunakan
- **Python 3.12**
- **Flask** (Web Framework)
- **SQLite** (Database)
- **Tailwind CSS** (Frontend via CDN)

## 📁 Struktur Proyek
```text
KaNgkot/
├── app_sqlite.py      # Entry point aplikasi Flask
├── db_config.py       # Konfigurasi database SQLite
├── setup_db.py        # Script inisialisasi tabel database
├── seeder_sqlite.py   # Script data dummy (Admin & Angkot)
├── templates/         # Folder template HTML (Jinja2)
│   ├── base.html      # Parent layout
│   ├── admin_dashboard.html
│   ├── user_dashboard.html
│   └── ...
└── static/            # Asset statis (CSS/JS/Images)
⚙️ Cara Menjalankan Secara Lokal
Clone Repository

Bash
git clone [https://github.com/username/KaNgkot.git](https://github.com/username/KaNgkot.git)
cd KaNgkot
Buat Virtual Environment

Bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
Install Dependencies

Bash
pip install flask
Inisialisasi Database

Bash
python setup_db.py
Jalankan Aplikasi

Bash
python app_sqlite.py
Buka http://127.0.0.1:5000 di browser Anda.

🔐 Akun Akses Default (Development)
Admin: admin / admin123

User: kamal / kamal123

📝 Detail Teknis Deployment (PythonAnywhere)
Proyek ini menggunakan standar WSGI. Pastikan path pada file WSGI PythonAnywhere diarahkan ke folder project dan menggunakan venv yang sesuai dengan versi Python (rekomendasi: 3.12).

Dibuat oleh: [Kamal Erlambang] - [230511075]


---

### Tips untuk Kamu:
1. **Cara Membuat di GitHub:** Masuk ke repository kamu di GitHub, klik tombol **"Add file"** -> **"Create new file"**, beri nama `README.md`, lalu tempel kode di atas.
2. **Screenshots:** Sangat disarankan untuk mengambil tangkapan layar (screenshot) halaman Login, Dashboard Admin, dan Dashboard User, lalu upload ke folder `screenshots` di GitHub agar orang bisa melihat tampilan aplikasinya tanpa harus menginstall.

Laporan sudah oke, README sudah siap. Ada lagi yang bisa saya bantu untuk menyempurnakan tugas akhir kamu? Selamat ya, Kamal! 🎓🚀