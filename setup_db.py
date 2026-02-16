import sqlite3
from db_config import get_db_connection

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("Membuka koneksi SQLite...")

    # 1. Buat Tabel Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2. Buat Tabel Angkot
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS angkot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plat_nomor TEXT NOT NULL UNIQUE,
        jurusan TEXT NOT NULL,
        harga_per_hari REAL NOT NULL,
        status TEXT DEFAULT 'tersedia',
        img_url TEXT
    )
    ''')

    # 3. Buat Tabel Bookings
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        angkot_id INTEGER,
        tanggal_sewa TEXT NOT NULL,
        status_booking TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (angkot_id) REFERENCES angkot(id)
    )
    ''')

    # 4. Seeding Data (Isi Data Awal)
    print("Mengisi data awal...")
    
    try:
        # Admin
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       ('admin', 'admin123', 'admin'))
    except sqlite3.IntegrityError:
        pass # Sudah ada

    try:
        # Angkot Dummy
        angkot_data = [
            ('B 1111 AA', 'Cengkareng - Kota', 150000, 'tersedia'),
            ('B 2222 BB', 'Kalideres - Grogol', 200000, 'tersedia')
        ]
        cursor.executemany("INSERT INTO angkot (plat_nomor, jurusan, harga_per_hari, status) VALUES (?, ?, ?, ?)", angkot_data)
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()
    print("✅ Database SQLite berhasil dibuat: kangkot.db")

if __name__ == '__main__':
    init_db()