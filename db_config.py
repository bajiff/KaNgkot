import mysql.connector

# --- PENGATURAN ENVIRONMENT ---
# Ubah ke False saat kode ini sudah di-upload ke PythonAnywhere
IS_LOCAL = True 

def get_db_connection():
    config = {}

    if IS_LOCAL:
        # Konfigurasi Database LOKAL (XAMPP/MAMP/Lainnya)
        config = {
            'host': 'localhost',
            'user': 'root',      # Default XAMPP biasanya 'root'
            'password': 'rVzSgBU0L!Q1KZ7/',
            'database': 'db_angkot'
        }
    else:
        # Konfigurasi Database PYTHONANYWHERE
        # Nanti Anda isi ini setelah membuat DB di dashboard PythonAnywhere
        config = {
            'host': 'namauser.mysql.pythonanywhere-services.com',
            'user': 'namauser',
            'password': 'password_db_anda',
            'database': 'namauser$db_angkot'
        }

    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None