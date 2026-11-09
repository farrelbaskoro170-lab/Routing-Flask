from flask import Flask, redirect, url_for, abort

app = Flask(__name__)

# Data dummy untuk studi kasus Toko HP
database_hp = {
    1: "Samsung Galaxy S24 Ultra",
    2: "iPhone 15 Pro Max",
    3: "Xiaomi 14"
}
user_terdaftar = ["admin", "farrel", "baskoro"]


# 1. Minimal 4 Route Statis
@app.route('/')
def beranda():
    return """
    <h1>Beranda Toko HP</h1>
    <p>Selamat datang di Toko HP Terpercaya.</p>
    <hr>
    <p><b>Menu Navigasi Test:</b></p>
    <ul>
        <li><a href="/tentang">Halaman Tentang</a></li>
        <li><a href="/layanan">Halaman Layanan</a></li>
        <li><a href="/kontak">Halaman Kontak</a></li>
        <li><a href="/cek/farrel">Cek Username 'farrel' (Valid & Terdaftar)</a></li>
        <li><a href="/cek/abc">Cek Username 'abc' (Gagal Validasi)</a></li>
        <li><a href="/produk/1">Produk ID 1 (Ada)</a></li>
        <li><a href="/produk/99">Produk ID 99 (Trigger 404)</a></li>
    </ul>
    """

@app.route('/tentang')
def tentang():
    return "<h1>Tentang Kami</h1><p>Penyedia smartphone garansi resmi sejak 2020.</p><a href='/'>&larr; Kembali ke Beranda</a>"

@app.route('/layanan')
def layanan():
    return "<h1>Layanan</h1><p>Layanan Tukar Tambah, Service Resmi, dan Garansi.</p><a href='/'>&larr; Kembali ke Beranda</a>"

@app.route('/kontak')
def kontak():
    return "<h1>Kontak</h1><p>Hubungi Customer Service: 08123456789</p><a href='/'>&larr; Kembali ke Beranda</a>"


# 2 & 4. Dynamic Route, Validasi, Redirect & url_for
@app.route('/cek/<username>')
def cek_username(username):
    # Validasi: username minimal 4 karakter dan alfanumerik
    if not username.isalnum() or len(username) < 4:
        return "<h3>Validasi Gagal</h3><p>Username harus berupa huruf/angka dan minimal 4 karakter!</p><a href='/'>&larr; Kembali ke Beranda</a>"
    
    # Syarat 4: Menggunakan redirect & url_for ke route profil_user
    return redirect(url_for('profil_user', username=username))

@app.route('/user/<username>')
def profil_user(username):
    status = "Sudah Terdaftar" if username.lower() in user_terdaftar else "Tersedia untuk Pendaftaran"
    return f"<h1>Profil User</h1><p>Username: <b>{username}</b></p><p>Status: <b>{status}</b></p><a href='/'>&larr; Kembali ke Beranda</a>"


# 3. Route Converter INT dan Abort(404)
@app.route('/produk/<int:id>')
def detail_produk(id):
    if id not in database_hp:
        abort(404)  # Melempar error 404 jika ID produk tidak ada di database
    return f"<h1>Detail Produk</h1><p>ID: {id}</p><p>Model HP: <b>{database_hp[id]}</b></p><a href='/'>&larr; Kembali ke Beranda</a>"


# 5. Custom Halaman Error 404
@app.errorhandler(404)
def error_404(e):
    return "<h1>404 - Halaman Tidak Ditemukan</h1><p>Maaf, data atau halaman Toko HP yang Anda cari tidak ada.</p><a href='/'>&larr; Kembali ke Beranda</a>", 404


if __name__ == '__main__':
    # Gunakan port 5000
    app.run(debug=True, port=5001)