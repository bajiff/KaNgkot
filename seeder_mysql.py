import mysql.connector
from db_config import get_db_connection

def seed_data():
    conn = get_db_connection()
    if not conn:
        print("Gagal koneksi ke database.")
        return

    cursor = conn.cursor()

    print("🌱 Memulai proses seeding data...")

    # --- 1. DATA USERS ---
    # Format: (username, password, role)
    # Catatan: Password masih plain text sesuai tutorial saat ini.
    users_data = [
        ('Kamal', 'kamal123', 'admin'),
        ('supir_budi', 'budi123', 'user'),
        ('penumpang_ani', 'ani123', 'user')
    ]

    print(f"   Menambahkan {len(users_data)} user...")
    
    user_query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    
    for user in users_data:
        try:
            cursor.execute(user_query, user)
            print(f"   [OK] User '{user[0]}' berhasil dibuat.")
        except mysql.connector.IntegrityError:
            print(f"   [SKIP] User '{user[0]}' sudah ada.")
        except Exception as e:
            print(f"   [ERROR] Gagal membuat user '{user[0]}': {e}")

    # --- 2. DATA ANGKOT ---
    # Format: (plat_nomor, jurusan, harga_per_hari, status)
    angkot_data = [
        ('B 1234 CD', 'Kamal - Cengkareng', 150000, 'tersedia'),
        ('B 5678 EF', 'Kalideres - Kota', 200000, 'disewa'),
        ('B 9012 GH', 'Pasar Cengkareng - Kapuk', 120000, 'perbaikan'),
        ('B 3456 IJ', 'Grogol - Slipi', 180000, 'tersedia'),
        ('B 7890 KL', 'Rawa Buaya - Puri', 160000, 'tersedia')
    ]

    print(f"   Menambahkan {len(angkot_data)} angkot...")

    angkot_query = "INSERT INTO angkot (plat_nomor, jurusan, harga_per_hari, status) VALUES (%s, %s, %s, %s)"

    for angkot in angkot_data:
        try:
            cursor.execute(angkot_query, angkot)
            print(f"   [OK] Angkot '{angkot[0]}' berhasil ditambahkan.")
        except mysql.connector.IntegrityError:
            print(f"   [SKIP] Angkot '{angkot[0]}' sudah ada.")
        except Exception as e:
            print(f"   [ERROR] Gagal menambahkan angkot '{angkot[0]}': {e}")

    # --- COMMIT & CLOSE ---
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Seeding selesai!")

if __name__ == '__main__':
    seed_data()