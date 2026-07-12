import streamlit as st
import time
import random

# 1. Pengaturan Halaman & Desain Visual Full Warna-Warni
st.set_page_config(page_title="Tebak Kilat Kebutuhan vs Keinginan", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    /* Latar belakang cerah penuh energi */
    .stApp { background-color: #FFDE59; } 
    
    /* Desain Beranda Awal */
    .welcome-card {
        background-color: #FF5757;
        border: 6px solid #000000;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        color: #FFFFFF;
        box-shadow: 8px 8px 0px #000000;
        margin-bottom: 25px;
    }
    
    /* Kotak Wadah Barang */
    .display-box {
        background-color: #FFFFFF;
        border: 6px solid #000000;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 8px 8px 0px #000000;
        margin-bottom: 25px;
    }
    
    .nama-barang {
        font-size: 45px;
        font-weight: bold;
        color: #FF5757;
        text-transform: uppercase;
        margin: 20px 0;
    }
    
    /* Papan Skor & Timer Digital */
    .skor-screen {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Courier New', monospace;
        font-size: 30px;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        border: 3px solid #333;
    }
    
    /* Tampilan Skor Akhir Raksasa */
    .final-score-box {
        background-color: #000000;
        color: #5CE1E6;
        font-family: 'Courier New', monospace;
        font-size: 60px;
        font-weight: bold;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 5px solid #FFFFFF;
        box-shadow: 0px 0px 20px #5CE1E6;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# 2. Basis Data Barang & Variabel Game
KUMPULAN_BARANG = [
    {"nama": "🍱 Beli Cireng Bumbu", "jenis": "Keinginan"},
    {"nama": "✏️ Buku Tulis Sekolah", "jenis": "Kebutuhan"},
    {"nama": "💎 Top Up Diamond Game", "jenis": "Keinginan"},
    {"nama": "👟 Sepatu Sekolah Hitam", "jenis": "Kebutuhan"},
    {"nama": "🥤 Es Boba Kekinian", "jenis": "Keinginan"},
    {"nama": "💧 Air Minum Botol", "jenis": "Kebutuhan"},
    {"nama": "🚲 Sepeda Roda Tiga", "jenis": "Keinginan"},
    {"nama": "🩹 Plester Luka", "jenis": "Kebutuhan"},
    {"nama": "🧸 Boneka Beruang Besar", "jenis": "Keinginan"},
    {"nama": "🎒 Tas Ransel Baru (Tas Lama Rusak)", "jenis": "Kebutuhan"},
    {"nama": "🍿 Popcorn Bioskop", "jenis": "Keinginan"},
    {"nama": "🧦 Kaos Kaki Polos", "jenis": "Kebutuhan"},
]

# Inisialisasi Session State
if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 'home'
    st.session_state.nama_kelompok = ""
    st.session_state.skor = 0
    st.session_state.barang_sekarang = None
    st.session_state.waktu_mulai = None
    st.session_state.barang_tersisa = []
    st.session_state.list_jawaban = [] # Menyimpan riwayat barang yang sudah dilewati

# 3. Alur Tampilan Game

# --- HALAMAN UTAMA (HOME) ---
if st.session_state.game_stage == 'home':
    st.markdown("""
    <div class='welcome-card'>
        <h1>👋 HALO ANAK-ANAK HEBAT! 👋</h1>
        <p style='font-size: 20px;'>Selamat datang di Game Tebak Kilat ⚡</p>
        <h3 style='color: #FFDE59;'>🎮 KEBUTUHAN VS KEINGINAN 🎮</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Nama Kelompok
    st.markdown("<div class='display-box'>", unsafe_allow_html=True)
    nama_input = st.text_input("✍️ Masukkan Nama Kelompok Kasih di Sini:", placeholder="Contoh: Kelompok Harimau 🐯")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚀 MULAI GAME SEKARANG", use_container_width=True, type="primary"):
        if nama_input.strip() != "":
            st.session_state.nama_kelompok = nama_input
            st.session_state.game_stage = 'playing'
            st.session_state.skor = 0
            st.session_state.list_jawaban = []
            st.session_state.waktu_mulai = time.time()
            st.session_state.barang_tersisa = KUMPULAN_BARANG.copy()
            random.shuffle(st.session_state.barang_tersisa)
            st.session_state.barang_sekarang = st.session_state.barang_tersisa.pop()
            st.rerun()
        else:
            st.error("⚠️ Nama kelompok tidak boleh kosong ya!")

# --- HALAMAN SAAT GAME BERJALAN ---
elif st.session_state.game_stage == 'playing':
    waktu_berjalan = time.time() - st.session_state.waktu_mulai
    waktu_sisa = max(0, 60 - int(waktu_berjalan))
    
    if waktu_sisa <= 0 or not st.session_state.barang_sekarang:
        st.session_state.game_stage = 'scoring'
        st.rerun()
    else:
        # Papan Status Kelompok, Skor, dan Waktu
        st.markdown(f"<h2 style='text-align:center; color:black;'>🔥 KELOMPOK: {st.session_state.nama_kelompok} 🔥</h2>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='skor-screen'>💰 SKOR: {st.session_state.skor}</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='skor-screen'>⏱️ WAKTU: {waktu_sisa}s</div>", unsafe_allow_html=True)
            
        # Kolom Tampilan Nama Barang
        st.markdown(f"""
        <div class='display-box'>
            <p style='color: #555; font-size: 20px; font-weight: bold;'>📦 NAMA BARANG:</p>
            <div class='nama-barang'>{st.session_state.barang_sekarang['nama']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Kolom Pilihan Tombol Tindakan
        st.markdown("<h3 style='text-align:center; color:black;'>PILIH KATEGORI:</h3>", unsafe_allow_html=True)
        col_tombol_1, col_tombol_2 = st.columns(2)
        
        with col_tombol_1:
            if st.button("👍 KEBUTUHAN", use_container_width=True, type="primary"):
                status_benar = (st.session_state.barang_sekarang['jenis'] == "Kebutuhan")
                poin_dapat = 100 if status_benar else -50
                st.session_state.skor += poin_dapat
                
                # Catat ke list riwayat
                st.session_state.list_jawaban.append(f"{st.session_state.barang_sekarang['nama']} -> Pilih: Kebutuhan ({'✅ Benar' if status_benar else '❌ Salah'})")
                
                if st.session_state.barang_tersisa:
                    st.session_state.barang_sekarang = st.session_state.barang_tersisa.pop()
                else:
                    st.session_state.barang_sekarang = None
                st.rerun()
                
        with col_tombol_2:
            if st.button("🛍️ KEINGINAN", use_container_width=True):
                status_benar = (st.session_state.barang_sekarang['jenis'] == "Keinginan")
                poin_dapat = 100 if status_benar else -50
                st.session_state.skor += poin_dapat
                
                # Catat ke list riwayat
                st.session_state.list_jawaban.append(f"{st.session_state.barang_sekarang['nama']} -> Pilih: Keinginan ({'✅ Benar' if status_benar else '❌ Salah'})")
                
                if st.session_state.barang_tersisa:
                    st.session_state.barang_sekarang = st.session_state.barang_tersisa.pop()
                else:
                    st.session_state.barang_sekarang = None
                st.rerun()
        
        # Kolom List Barang Yang Sudah Ditebak
        if st.session_state.list_jawaban:
            st.markdown("<br><h4 style='color:black;'>📋 List Barang Yang Sudah Diisi:</h4>", unsafe_allow_html=True)
            for item in reversed(st.session_state.list_jawaban):
                st.write(item)
                
        time.sleep(1)
        st.rerun()

# --- HALAMAN HITUNG SKOR AKHIR (ANIMASI ANIMATED COUNT UP) ---
elif st.session_state.game_stage == 'scoring':
    st.markdown(f"<h2 style='text-align:center; color:black;'>🎉 SESI {st.session_state.nama_kelompok} SELESAI 🎉</h2>", unsafe_allow_html=True)
    
    # Elemen kosong tunggal untuk wadah angka animasi
    wadah_skor_animasi = st.empty()
    skor_target = st.session_state.skor
    
    # Mekanisme Animasi Hitung Angka (Count-up dari 0 ke target)
    if skor_target > 0:
        langkah = max(10, skor_target // 20)  # Menentukan kecepatan lompatan angka
        for angka_skor in range(0, skor_target + 1, langkah):
            wadah_skor_animasi.markdown(f"<div class='final-score-box'>🔢 {angka_skor}</div>", unsafe_allow_html=True)
            time.sleep(0.04)
    elif skor_target < 0:
        # Jika skor minus, hitung mundur ke bawah
        langkah = min(-10, skor_target // 20)
        for angka_skor in range(0, skor_target - 1, langkah):
            wadah_skor_animasi.markdown(f"<div class='final-score-box'>🔢 {angka_skor}</div>", unsafe_allow_html=True)
            time.sleep(0.04)
            
    # Mengunci tampilan angka pada skor mutlak terakhir
    wadah_skor_animasi.markdown(f"<div class='final-score-box'>✨ {skor_target} POIN ✨</div>", unsafe_allow_html=True)
    
    # Munculkan Balon Selebrasi
    st.balloons()
    
    # Teks Hasil Akhir
    st.markdown(f"""
    <div class='welcome-card' style='background-color: #2E86C1;'>
        <h2>🎈 YEY SKOR KAMU LUAR BIASA! 🎈</h2>
        <p style='font-size: 18px;'>Kerja bagus Kelompok <b>{st.session_state.nama_kelompok}</b>!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Menampilkan total riwayat akhir barang untuk bahan evaluasi Kasih di kelas
    with st.expander("🔍 Lihat Hasil Detil Pemilahan Barang"):
        for item in st.session_state.list_jawaban:
            st.write(item)
            
    if st.button("🔄 KEMBALI KE BERANDA (KELOMPOK BARU)", use_container_width=True):
        st.session_state.game_stage = 'home'
        st.rerun()
