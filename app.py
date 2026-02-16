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

# Route Dashboard
@app.route('/dashboard')
def dashboard():
    # Cek Login
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Ambil data angkot dari Database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Ambil semua data angkot
    cursor.execute("SELECT * FROM angkot")
    data_angkot = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Render template dengan membawa data 'angkots'
    return render_template('dashboard.html', angkots=data_angkot)

# --- ROUTE CRUD ANGKOT (ADMIN ONLY) ---

@app.route('/angkot/tambah', methods=['GET', 'POST'])
def tambah_angkot():
    # Keamanan: Hanya Admin yang boleh akses
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        plat_nomor = request.form['plat_nomor']
        jurusan = request.form['jurusan']
        harga = request.form['harga_per_hari']
        status = request.form['status']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO angkot (plat_nomor, jurusan, harga_per_hari, status) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (plat_nomor, jurusan, harga, status))
            conn.commit()
            flash('Angkot berhasil ditambahkan!', 'success')
            return redirect(url_for('dashboard'))
        except mysql.connector.Error as err:
            flash(f'Gagal menambah data: {err}', 'error')
        finally:
            cursor.close()
            conn.close()

    # Jika GET, tampilkan form kosong
    return render_template('form_angkot.html', angkot=None)

@app.route('/angkot/edit/<int:id>', methods=['GET', 'POST'])
def edit_angkot(id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        plat_nomor = request.form['plat_nomor']
        jurusan = request.form['jurusan']
        harga = request.form['harga_per_hari']
        status = request.form['status']

        try:
            query = "UPDATE angkot SET plat_nomor=%s, jurusan=%s, harga_per_hari=%s, status=%s WHERE id=%s"
            cursor.execute(query, (plat_nomor, jurusan, harga, status, id))
            conn.commit()
            flash('Data angkot berhasil diperbarui!', 'success')
            return redirect(url_for('dashboard'))
        except mysql.connector.Error as err:
            flash(f'Gagal update data: {err}', 'error')

    # Jika GET, ambil data lama untuk ditampilkan di form
    cursor.execute("SELECT * FROM angkot WHERE id = %s", (id,))
    angkot = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('form_angkot.html', angkot=angkot)

@app.route('/angkot/hapus/<int:id>')
def hapus_angkot(id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM angkot WHERE id = %s", (id,))
        conn.commit()
        flash('Angkot berhasil dihapus.', 'success')
    except mysql.connector.Error as err:
        flash(f'Gagal menghapus: {err}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('dashboard'))

# --- MAIN BLOCK ---
if __name__ == '__main__':
    # Debug=True mempermudah kita melihat error saat development
    app.run(debug=True)