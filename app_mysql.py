from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_config import get_db_connection
import sqlite3

app = Flask(__name__)

# KUNCI RAHASIA
app.secret_key = 'kunci_rahasia_kangkot_dev'

# --- 1. ROUTE Cek Koneksi DB (Debugging) ---
@app.route('/cek_db')
def cek_db():
    try:
        conn = get_db_connection()
        conn.close()
        return "<h1>Sukses! Koneksi SQLite Berhasil.</h1>"
    except Exception as e:
        return f"<h1>Gagal! Error: {str(e)}</h1>"

# --- 2. ROUTE UTAMA ---
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# --- 3. AUTHENTICATION ---
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # SQLite: Menggunakan ? sebagai placeholder
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and user['password'] == password:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        return redirect(url_for('dashboard'))
    else:
        flash('Username atau Password salah!', 'error')
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash('Password tidak sama!', 'error')
            return redirect(url_for('register'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'user')", (username, password))
            conn.commit()
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('Username sudah digunakan!', 'error')
        except Exception as e:
            flash(f'Error: {e}', 'error')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- 4. DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM angkot")
    data_angkot = cursor.fetchall()
    conn.close()
    
    if session['role'] == 'admin':
        return render_template('admin_dashboard.html', angkots=data_angkot)
    else:
        return render_template('user_dashboard.html', angkots=data_angkot)

# --- 5. CRUD ADMIN ---
@app.route('/angkot/tambah', methods=['GET', 'POST'])
def tambah_angkot():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        plat_nomor = request.form['plat_nomor']
        jurusan = request.form['jurusan']
        harga = request.form['harga_per_hari']
        status = request.form['status']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO angkot (plat_nomor, jurusan, harga_per_hari, status) VALUES (?, ?, ?, ?)", 
                           (plat_nomor, jurusan, harga, status))
            conn.commit()
            flash('Angkot berhasil ditambahkan!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Gagal menambah data: {e}', 'error')
        finally:
            conn.close()

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
            cursor.execute("UPDATE angkot SET plat_nomor=?, jurusan=?, harga_per_hari=?, status=? WHERE id=?", 
                           (plat_nomor, jurusan, harga, status, id))
            conn.commit()
            flash('Data angkot berhasil diperbarui!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Gagal update data: {e}', 'error')
        finally:
            conn.close()

    cursor.execute("SELECT * FROM angkot WHERE id = ?", (id,))
    angkot = cursor.fetchone()
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
    except Exception as e:
        flash(f'Gagal menghapus: {e}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('dashboard'))

# --- 6. BOOKING ---
@app.route('/booking/<int:id>', methods=['GET', 'POST'])
def booking_angkot(id):
    if 'user_id' not in session:
        flash('Silakan login untuk booking.', 'error')
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        tanggal = request.form['tanggal_sewa']
        user_id = session['user_id']
        
        try:
            cursor.execute("INSERT INTO bookings (user_id, angkot_id, tanggal_sewa, status_booking) VALUES (?, ?, ?, 'pending')", 
                           (user_id, id, tanggal))
            cursor.execute("UPDATE angkot SET status = 'disewa' WHERE id = ?", (id,))
            conn.commit()
            flash('Booking berhasil! Menunggu konfirmasi admin.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Gagal booking: {e}', 'error')
        finally:
            conn.close()
            
    cursor.execute("SELECT * FROM angkot WHERE id = ?", (id,))
    angkot = cursor.fetchone()
    conn.close()
    return render_template('booking.html', angkot=angkot)

if __name__ == '__main__':
    app.run(debug=True)