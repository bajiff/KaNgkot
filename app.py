from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from db_config import get_db_connection

app = Flask(__name__)

# KUNCI RAHASIA (Wajib untuk Session/Login)
# Di production nanti, ganti ini dengan string acak yang panjang
app.secret_key = 'kunci_rahasia_kangkot_dev'

# --- 1. ROUTE Cek Koneksi DB (Hanya untuk Debugging Awal) ---
@app.route('/cek_db')
def cek_db():
    conn = get_db_connection()
    if conn:
        conn.close()
        return "<h1>Sukses! Koneksi Database Berhasil.</h1>"
    else:
        return "<h1>Gagal! Tidak bisa konek ke Database. Cek db_config.py</h1>"

# --- 2. ROUTE UTAMA (Login Page) ---
@app.route('/')
def index():
    # Jika user sudah login, arahkan ke dashboard (Nanti kita buat)
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# --- 3. ROUTE AUTHENTICATION (Placeholder) ---
@app.route('/login', methods=['POST'])
def login():
    # 1. Ambil data dari form HTML
    username = request.form['username']
    password = request.form['password']

    # 2. Buka koneksi ke database
    conn = get_db_connection()
    if not conn:
        flash('Gagal koneksi ke database!', 'error')
        return redirect(url_for('index'))

    # 3. Cek apakah user ada di database
    cursor = conn.cursor(dictionary=True) # dictionary=True agar hasil query berupa Dict {'id': 1, ...}
    
    # Query aman dari SQL Injection
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    # 4. Verifikasi Password (Sederhana dulu: String comparison)
    # Catatan: Di production nanti WAJIB pakai hash (bcrypt/pbkdf2)
    if user and user['password'] == password:
        # Login Sukses: Simpan data penting di Session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        
        return redirect(url_for('dashboard'))
    else:
        # Login Gagal
        flash('Username atau Password salah!', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return f"Halo, {session['username']}! (Role: {session['role']})"

# --- MAIN BLOCK ---
if __name__ == '__main__':
    # Debug=True mempermudah kita melihat error saat development
    app.run(debug=True)