import sqlite3
from db_config import get_db_connection

def seed_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    print("🌱 Memulai proses seeding SQLite...")

    # 1. Tambah Data Users (Admin & User)
    users = [
        ('admin', 'admin123', 'admin'),
        ('kamal', 'kamal123', 'admin'),
        ('baji', 'baji123', 'user'),
        ('bondan', 'bondan123', 'user'),
        ('abid', 'abid123', 'user')
    ]
    
    for u in users:
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", u)
            print(f"   [OK] User {u[0]} berhasil dibuat.")
        except sqlite3.IntegrityError:
            print(f"   [SKIP] User {u[0]} sudah ada.")

    # 2. Tambah Data Angkot Awal
    angkots = [
        ('B 1234 KA', 'Kamal - Kalideres', 150000, 'tersedia'),
        ('B 5678 MA', 'Kamal - Cengkareng', 120000, 'tersedia'),
        ('B 9012 L', 'Rawa Buaya - Puri', 180000, 'disewa')
    ]

    for a in angkots:
        try:
            cursor.execute("INSERT INTO angkot (plat_nomor, jurusan, harga_per_hari, status) VALUES (?, ?, ?, ?)", a)
            print(f"   [OK] Angkot {a[0]} berhasil ditambahkan.")
        except sqlite3.IntegrityError:
            print(f"   [SKIP] Angkot {a[0]} sudah ada.")

    conn.commit()
    conn.close()
    print("✅ Seeding selesai! Silakan login dengan user admin.")

if __name__ == '__main__':
    seed_data()