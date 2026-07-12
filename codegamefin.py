import streamlit as st

# Setup Konfigurasi Halaman
st.set_page_config(page_title="Kereta Uang", page_icon="🚂", layout="centered")

# CSS Khusus untuk Tampilan Item dan Uang
st.markdown('''
<style>
.uang-kotak {
    display: inline-block;
    border: 2px solid #2e7d32;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 4px;
    background-color: #e8f5e9;
    color: #1b5e20;
    font-weight: 900;
    font-size: 16px;
    text-align: center;
    box-shadow: 2px 2px 0px #2e7d32;
}
.item-card {
    text-align: center;
    border: 3px dashed #1976d2;
    border-radius: 15px;
    padding: 20px;
    background-color: #e3f2fd;
    margin-bottom: 20px;
}
.item-icon { font-size: 80px; line-height: 1; margin-bottom: 10px; }
.item-title { font-size: 22px; font-weight: bold; color: #1565c0; }
.item-price { font-size: 20px; color: #d32f2f; font-weight: bold; margin-top: 5px; }
.qty-badge { background-color: #ff9800; color: white; padding: 5px 10px; border-radius: 20px; font-weight: bold; display: inline-block; margin-top: 10px; }
.cerita-box { background-color: #fff3e0; padding: 15px; border-left: 5px solid #ff9800; margin-bottom: 15px; font-size: 16px; }
</style>
''', unsafe_allow_html=True)

# Fungsi Pemecah Nominal Uang
def get_pecahan(jumlah):
    pecahan = [10000, 5000, 2000, 1000, 500, 200, 100]
    hasil = []
    sisa = jumlah
    for p in pecahan:
        while sisa >= p:
            hasil.append(p)
            sisa -= p
    return hasil

# Fungsi Render HTML untuk Uang
def render_uang_html(jumlah):
    if jumlah == 0:
        return "<div style='font-size:18px; font-weight:bold; color:#d32f2f;'>Saldo Habis (Rp0)</div>"
    pecahan_list = get_pecahan(jumlah)
    html = "<div>"
    for p in pecahan_list:
        html += f"<div class='uang-kotak'>Rp {p:,}</div>"
    html += "</div>"
    return html

# Fungsi Render HTML untuk Item
def render_item_html(icon, nama, harga, qty):
    return f'''
    <div class='item-card'>
        <div class='item-icon'>{icon}</div>
        <div class='item-title'>{nama}</div>
        <div class='item-price'>Harga: Rp {harga:,} / pcs</div>
        <div class='qty-badge'>Beli Paket: {qty} pcs</div>
    </div>
    '''

# Manajemen Status Sesi (Session State)
if 'tahap' not in st.session_state:
    st.session_state.tahap = 'input_nama'
    st.session_state.saldo = 20000
    st.session_state.gerbong_saat_ini = 0
    st.session_state.nama_tim = ""
    st.session_state.inventaris = [] # Menyimpan riwayat barang yang dibeli

# Data Gerbong Baru (Penuh Cerita Urgen)
GERBONG_DATA = [
    {
        "gerbong": 1, 
        "nama_toko": "Bengkel Stasiun", 
        "cerita": "Waduh! Ban sepeda salah satu teman kalian bocor di parkiran stasiun. Kalian butuh memompa ban, tapi tukang pompa memberikan harga paketan.",
        "barang": "Jasa Pompa Ban", "icon": "🚲", "harga": 2000, "qty": 2
    },
    {
        "gerbong": 2, 
        "nama_toko": "Koperasi Sekolah", 
        "cerita": "Gawat! Pulpen kalian hilang semua, padahal nanti ada ulangan matematika. Kalau tidak beli, kalian tidak bisa ikut ujian.",
        "barang": "Pulpen Hitam", "icon": "🖊️", "harga": 1500, "qty": 3
    },
    {
        "gerbong": 3, 
        "nama_toko": "Kantin Gerbong", 
        "cerita": "Perut keroncongan banget setelah lelah menghitung. Ada penjual gorengan lewat menawarkan paket hemat pengganjal perut.",
        "barang": "Gorengan Hangat", "icon": "🥟", "harga": 1000, "qty": 5
    },
    {
        "gerbong": 4, 
        "nama_toko": "Toko Kado", 
        "cerita": "Kalian baru ingat kalau hari ini ibu wali kelas ulang tahun! Ada hadiah bagus untuk diberikan secara patungan.",
        "barang": "Kado Buku Catatan", "icon": "🎁", "harga": 3000, "qty": 2
    },
    {
        "gerbong": 5, 
        "nama_toko": "Konter Keliling", 
        "cerita": "Kuota internet kalian mendadak habis, padahal kalian butuh memesan ojek online saat tiba di stasiun akhir nanti.",
        "barang": "Voucher Kuota", "icon": "📱", "harga": 4000, "qty": 2
    }
]

st.title("🚂 Game Kereta Uang 🚂")
st.markdown("---")

# FASE 1: Input Nama
if st.session_state.tahap == 'input_nama':
    st.subheader("Persiapan Keberangkatan")
    st.write("Kelola uang kelompok kalian agar tidak habis (Rp0) sebelum mencapai stasiun akhir.")
    nama = st.text_input("Masukkan nama kelompok kalian:")
    
    if st.button("Mulai Petualangan"):
        if nama:
            st.session_state.nama_tim = nama
            st.session_state.tahap = 'hitung_perkalian'
            st.rerun()
        else:
            st.warning("Nama tim wajib diisi!")

# FASE 2: Perjalanan Gerbong
elif st.session_state.tahap in ['hitung_perkalian', 'keputusan_beli', 'hitung_pengurangan']:
    idx = st.session_state.gerbong_saat_ini
    data = GERBONG_DATA[idx]
    total_harga_asli = data['harga'] * data['qty']
    
    st.subheader(f"🚂 Gerbong {data['gerbong']}: {data['nama_toko']}")
    
    # Menampilkan Cerita Konteks
    st.markdown(f"<div class='cerita-box'><b>Kondisi:</b> {data['cerita']}</div>", unsafe_allow_html=True)
    
    # Tampilan Saldo dengan Visual Pecahan Uang
    st.markdown("### 💰 Dompet Kalian Saat Ini:")
    st.markdown(render_uang_html(st.session_state.saldo), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tampilan Barang dengan Visual Card
    st.markdown(render_item_html(data['icon'], data['barang'], data['harga'], data['qty']), unsafe_allow_html=True)
    
    # Lapis 1: Hitung Perkalian
    if st.session_state.tahap == 'hitung_perkalian':
        st.info("Hitung total harga paket di atas untuk membuka pilihan keputusan.")
        tebakan_harga = st.number_input("Total harga (Rp):", min_value=0, step=100)
        
        if st.button("Kunci Jawaban"):
            if tebakan_harga == total_harga_asli:
                st.success("✅ Benar! Silakan ambil keputusan.")
                st.session_state.tahap = 'keputusan_beli'
                st.rerun()
            else:
                st.error("❌ Hitungan salah! Coba periksa lagi perkaliannya.")
                
    # Lapis 2: Keputusan Beli / Lewati
    elif st.session_state.tahap == 'keputusan_beli':
        st.success(f"Harga Total: **Rp {total_harga_asli:,}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛒 BELI BARANG INI", use_container_width=True):
                if st.session_state.saldo < total_harga_asli:
                    st.error("⚠️ Uang tidak cukup! Terpaksa lewati.")
                else:
                    st.session_state.tahap = 'hitung_pengurangan'
                    st.rerun()
        with col2:
            if st.button("⏭️ LEWATI SAJA", use_container_width=True):
                if st.session_state.gerbong_saat_ini < len(GERBONG_DATA) - 1:
                    st.session_state.gerbong_saat_ini += 1
                    st.session_state.tahap = 'hitung_perkalian'
                else:
                    st.session_state.tahap = 'finish'
                st.rerun()
                
    # Lapis 3: Hitung Kembalian / Pengurangan
    elif st.session_state.tahap == 'hitung_pengurangan':
        sisa_saldo_asli = st.session_state.saldo - total_harga_asli
        
        st.warning("Hitung sisa uang kalian sebelum membayar ke kasir.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Uang Saat Ini:**")
            st.markdown(render_uang_html(st.session_state.saldo), unsafe_allow_html=True)
        with col_b:
            st.write("**Uang yang Dibayarkan:**")
            st.markdown(render_uang_html(total_harga_asli), unsafe_allow_html=True)
            
        tebakan_saldo = st.number_input("Berapa sisa uang kalian sekarang?", min_value=0, step=100)
        
        if st.button("Bayar & Lanjut"):
            if tebakan_saldo == sisa_saldo_asli:
                st.success("✅ Hitungan tepat! Transaksi berhasil.")
                st.session_state.saldo = sisa_saldo_asli
                # Masukkan ke daftar inventaris
                st.session_state.inventaris.append(f"{data['icon']} {data['barang']} ({data['qty']} pcs)")
                
                # Cek Kondisi Game Over
                if st.session_state.saldo <= 0:
                    st.session_state.tahap = 'game_over'
                elif st.session_state.gerbong_saat_ini < len(GERBONG_DATA) - 1:
                    st.session_state.gerbong_saat_ini += 1
                    st.session_state.tahap = 'hitung_perkalian'
                else:
                    st.session_state.tahap = 'finish'
                st.rerun()
            else:
                st.error("❌ Hitungan sisa uang salah! Coba kurangi dengan teliti.")

# FASE GAME OVER (Uang Habis)
elif st.session_state.tahap == 'game_over':
    st.error("💀 GAME OVER! 💀")
    st.header("BANGKRUT!")
    st.write(f"Sayang sekali, **Kelompok {st.session_state.nama_tim}** kehabisan uang di tengah jalan.")
    st.write("Uang kalian saat ini mencapai **Rp0**. Kalian tidak bisa melanjutkan perjalanan.")
    
    st.markdown("### 🛒 Barang yang sempat terbeli:")
    if len(st.session_state.inventaris) > 0:
        for item in st.session_state.inventaris:
            st.write(f"- {item}")
    else:
        st.write("- Belum membeli apa-apa.")
        
    if st.button("Main Lagi dari Awal"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# FASE 3: Akhir Perjalanan (Berhasil Selamat)
elif st.session_state.tahap == 'finish':
    st.balloons()
    st.header("🏁 STASIUN AKHIR 🏁")
    st.write(f"Selamat, **Kelompok {st.session_state.nama_tim}** telah menyelesaikan perjalanan!")
    
    st.markdown("### 💰 SISA UANG KALIAN:")
    st.markdown(render_uang_html(st.session_state.saldo), unsafe_allow_html=True)
    
    st.markdown("### 🛒 Daftar Belanjaan Kalian:")
    if len(st.session_state.inventaris) > 0:
        for item in st.session_state.inventaris:
            st.write(f"- {item}")
    else:
        st.write("- *Wow! Kalian super hemat dan tidak membeli apa pun.*")
    
    st.info("Silakan lapor ke Guru kalian untuk membandingkan sisa uang dan daftar barang dengan kelompok lain.")
    
    if st.button("Main Lagi dari Awal"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
