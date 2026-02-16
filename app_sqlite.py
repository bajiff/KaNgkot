
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
    cursor = conn.cursor() # dictionary=True agar hasil query berupa Dict {'id': 1, ...}
    
    # Query aman dari SQL Injection
    query = "SELECT * FROM users WHERE username = ?"
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

# --- ROUTE REGISTER (PENUMPANG BARU) ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Jika user submit form (POST)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm_password']

        # Validasi Password
        if password != confirm:
            flash('Password tidak sama!', 'error')
            return redirect(url_for('register'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Role default otomatis 'user'
            query = "INSERT INTO users (username, password, role) VALUES (?, ?, 'user')"
            cursor.execute(query, (username, password))
            conn.commit()
            
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('index')) # Kembali ke login
            
        except mysql.connector.IntegrityError:
            # Error jika username sudah ada
            flash('Username sudah digunakan! Cari nama lain.', 'error')
        except Exception as e:
            flash(f'Error: {e}', 'error')
        finally:
            cursor.close()
            conn.close()

    # Jika user baru buka halaman (GET)
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Route Dashboard
@app.route('/dashboard')
def dashboard():
    # 1. Cek Login
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # 2. Ambil data angkot
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM angkot")
    data_angkot = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # 3. Logika Pemisahan File Template
    # Jika Admin, render file admin_dashboard.html
    if session['role'] == 'admin':
        return render_template('admin_dashboard.html', angkots=data_angkot)
    
    # Jika User, render file user_dashboard.html
    else:
        return render_template('user_dashboard.html', angkots=data_angkot)

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
            query = "INSERT INTO angkot (plat_nomor, jurusan, harga_per_hari, status) VALUES (?, ?, ?, ?)"
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
    cursor = conn.cursor()

    if request.method == 'POST':
        plat_nomor = request.form['plat_nomor']
        jurusan = request.form['jurusan']
        harga = request.form['harga_per_hari']
        status = request.form['status']

        try:
            query = "UPDATE angkot SET plat_nomor=?, jurusan=?, harga_per_hari=?, status=? WHERE id=?"
            cursor.execute(query, (plat_nomor, jurusan, harga, status, id))
            conn.commit()
            flash('Data angkot berhasil diperbarui!', 'success')
            return redirect(url_for('dashboard'))
        except mysql.connector.Error as err:
            flash(f'Gagal update data: {err}', 'error')

    # Jika GET, ambil data lama untuk ditampilkan di form
    cursor.execute("SELECT * FROM angkot WHERE id = ?", (id,))
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
        cursor.execute("DELETE FROM angkot WHERE id = ?", (id,))
        conn.commit()
        flash('Angkot berhasil dihapus.', 'success')
    except mysql.connector.Error as err:
        flash(f'Gagal menghapus: {err}', 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('dashboard'))

# --- ROUTE BOOKING (WAJIB ADA AGAR TIDAK ERROR) ---
@app.route('/booking/<int:id>', methods=['GET', 'POST'])
def booking_angkot(id):
    # 1. Cek Login
    if 'user_id' not in session:
        flash('Silakan login untuk booking.', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # 2. Ambil data angkot
    cursor.execute("SELECT * FROM angkot WHERE id = ?", (id,))
    angkot = cursor.fetchone()

    # 3. Proses Booking
    if request.method == 'POST':
        tanggal = request.form['tanggal_sewa']
        user_id = session['user_id']
        
        try:
            # Simpan ke tabel bookings
            query_booking = "INSERT INTO bookings (user_id, angkot_id, tanggal_sewa, status_booking) VALUES (?, ?, ?, 'pending')"
            cursor.execute(query_booking, (user_id, id, tanggal))
            
            # Update status angkot jadi 'disewa'
            query_update = "UPDATE angkot SET status = 'disewa' WHERE id = ?"
            cursor.execute(query_update, (id,))
            
            conn.commit()
            flash('Booking berhasil! Menunggu konfirmasi admin.', 'success')
            return redirect(url_for('dashboard'))
            
        except mysql.connector.Error as err:
            flash(f'Gagal booking: {err}', 'error')
        finally:
            cursor.close()
            conn.close()
            
    # Jika GET, tampilkan halaman konfirmasi
    cursor.close()
    conn.close()
    return render_template('booking.html', angkot=angkot)

# --- MAIN BLOCK ---
if __name__ == '__main__':
    # Debug=True mempermudah kita melihat error saat development
    app.run(debug=True)