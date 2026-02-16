ada dua config yaitu

db_config.py -- isinya config ke sqlite
db_config2.py -- isinya config ke mysql

app_sqlite.py -- isinya route yang sesuai dengan sqlite
app_mysql.py -- isinya rote yang sesuai dengan mysql

jangan lupa seeder dulu dan ada dua seedernya
seeder_mysql.py
seeder_sqlite.py

jadi tinggal pilih aja, sekarang defautlnya saya make app.py (sqlite) karena saya ingin deploy ke PythonAnyWhere dan itu gratis kalau make sqlite sedangkan mysql bayar