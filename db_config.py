import sqlite3
import os

# Database akan disimpan sebagai file di folder yang sama dengan app.py
DB_NAME = 'kangkot.db'

def get_db_connection():
    # Menggunakan path absolut agar aman di server
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, DB_NAME)
    
    conn = sqlite3.connect(db_path)
    
    # PENTING: Agar hasil query bisa diakses seperti Dictionary (item['nama'])
    conn.row_factory = sqlite3.Row
    
    return conn