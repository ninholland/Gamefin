import streamlit as st
import time
import random

# 1. Pengaturan Halaman & Desain Visual (Latar Belakang Biru Cerah & Teks Besar)
st.set_page_config(page_title="Tebak Kilat Kebutuhan vs Keinginan", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    /* Latar belakang diganti jadi Biru Cerah Kartun */
    .stApp { background-color: #70D6FF; } 
    
    /* Desain Beranda Awal */
    .welcome-card {
        background-color: #FF70A6;
        border: 6px solid #000000;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        color: #FFFFFF;
        box-shadow: 8px 8px 0px #000000;
        margin-bottom: 25px;
    }
    
    /* Kotak Input Nama Kelompok & Nama Barang yang Diperbesar */
    .input-container {
        background-color: #FFFFFF;
        border: 6px solid #000000;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 8px 8px 0px #000000;
        margin-bottom: 25px;
        text-align: center;
    }
    
    /* Modifikasi kolom teks bawaan Streamlit agar tulisannya raksasa */
    div.stTextInput > div > div > input {
        font-size: 30px !important;
        font-weight: bold !important;
        text-align: center !important;
        height: 70px !important;
        border: 4px solid #000000 !important;
        border-radius: 10px !important;
        background-color: #FFF !important;
        color: #000000 !important;
    }
    
    .nama-barang {
        font-size: 45px;
        font-weight: bold;
        color: #FF70A6;
        text-transform: uppercase;
        margin: 20px 0;
    }
    
    /* Papan Skor & Timer Digital */
    .skor-screen {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Courier New', monospace;
        font-size: 32px;
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

if 'game_stage' not in st.session_state:
    st.session_state.game_stage = 'home'
    st.session_state.nama_kelompok = ""
    st.session_state.skor = 0
    st.session_state.barang_sekarang = None
    st.session_state.waktu_mulai = None
    st.session_state.barang_tersisa = []
    st.session_state.list_jawaban = []

# 3. Alur Tampilan Game

# --- HALAMAN UTAMA (HOME) ---
if st.session_state.game_stage == 'home':
    st.markdown("""
    <div class='welcome-card'>
        <h1>👋 HALO ANAK-ANAK HEBAT! 👋</h1>
        <p style='font-size: 20px;'>Selamat datang di Game Tebak Kilat ⚡</p>
        <h3 style='color: #EFFF96;'>🎮 KEBUTUHAN VS KEINGINAN 🎮</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Memasukkan kolom mengetik langsung di dalam wadah kotak putih besar
    st.markdown("<div class='input-container'><p style='font-size: 22px; font-weight: bold; color: black; margin-bottom: 5px;'>✍️ KETIK NAMA KELOMPOK DI SINI:</p>", unsafe_allow_html=True)
    nama_input = st.text_input("", placeholder="Contoh: KELOMPOK 1 🐯", label_visibility="collapsed")
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
            st.error("⚠️ Nama kelompok diisi dulu ya, Kasih!")

# --- HALAMAN SAAT GAME BERJALAN ---
elif st.session_state.game_stage == 'playing':
    waktu_berjalan = time.time() - st.session_state.waktu_mulai
    waktu_sisa = max(0, 60 - int(waktu_berjalan))
    
    if waktu_sisa <= 0 or not st.session_state.barang_sekarang:
        st.session_state.game_stage = 'scoring'
        st.rerun()
    else:
        st.markdown(f"<h2 style='text-align:center; color:black;'>🔥 KELOMPOK: {st.session_state.nama_kelompok} 🔥</h2>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='skor-screen'>💰 SKOR: {st.session_state.skor}</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='skor-screen'>⏱️ WAKTU: {waktu_sisa}s</div>", unsafe_allow_html=True)
            
        # Kolom Tampilan Nama Barang
        st.markdown(f"""
        <div class='input-container'>
            <p style='color: #555; font-size: 20px; font-weight: bold;'>📦 NAMA BARANG:</p>
            <div class='nama-barang'>{st.session_state.barang_sekarang['nama']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Kolom Pilihan Tombol Kebutuhan / Keinginan
        st.markdown("<h3 style='text-align:center; color:black;'>PILIH KATEGORI:</h3>", unsafe_allow_html=True)
        col_tombol_1, col_tombol_2 = st.columns(2)
        
        with col_tombol_1:
            if st.button("👍 KEBUTUHAN", use_container_width=True, type="primary"):
                status_benar = (st.session_state.barang_sekarang['jenis'] == "Kebutuhan")
                st.session_state.skor += 100 if status_benar else -50
                
                # Hanya memasukkan nama barang saja ke dalam list riwayat (Tanpa status Benar/Salah)
                st.session_state.list_jawaban.append(f"{st.session_state.barang_sekarang['nama']}")
                
                if st.session_state.barang_tersisa:
                    st.session_state.barang_sekarang = st.session_state.barang_tersisa.pop()
                else:
                    st.session_state.barang_sekarang = None
                st.rerun()
                
        with col_tombol_2:
            if st.button("🛍️ KEINGINAN", use_container_width=True):
                status_benar = (st.session_state.barang_sekarang['jenis'] == "Keinginan")
                st.session_state.skor += 100 if status_benar else -50
                
                # Hanya memasukkan nama barang saja ke dalam list riwayat (Tanpa status Benar/Salah)
                st.session_state.list_jawaban.append(f"{st.session_state.barang_sekarang['nama']}")
                
                if st.session_state.barang_tersisa:
                    st.session_state.barang_sekarang = st.session_state.barang_tersisa.pop()
                else:
                    st.session_state.barang_sekarang = None
                st.rerun()
        
        # Kolom List Murni Barang yang Sudah Dilewati
        if st.session_state.list_jawaban:
            st.markdown("<br><h4 style='color:black;'>📋 List Barang yang Sudah Muncul:</h4>", unsafe_allow_html=True)
            for item in reversed(st.session_state.list_jawaban):
                st.markdown(f"<div style='background-color:white; padding:10px; border:2px solid black; border-radius:5px; margin-bottom:5px; font-weight:bold; color:black;'>{item}</div>", unsafe_allow_html=True)
                
        time.sleep(1)
        st.rerun()

# --- HALAMAN HITUNG SKOR AKHIR ---
elif st.session_state.game_stage == 'scoring':
    st.markdown(f"<h2 style='text-align:center; color:black;'>🎉 SESI {st.session_state.nama_kelompok} SELESAI 🎉</h2>", unsafe_allow_html=True)
    
    wadah_skor_animasi = st.empty()
    skor_target = st.session_state.skor
    
    if skor_target > 0:
        langkah = max(10, skor_target // 20)
        for angka_skor in range(0, skor_target + 1, langkah):
            wadah_skor_animasi.markdown(f"<div class='final-score-box'>🔢 {angka_skor}</div>", unsafe_allow_html=True)
            time.sleep(0.04)
    elif skor_target < 0:
        langkah = min(-10, skor_target // 20)
        for angka_skor in range(0, skor_target - 1, langkah):
            wadah_skor_animasi.markdown(f"<div class='final-score-box'>🔢 {angka_skor}</div>", unsafe_allow_html=True)
            time.sleep(0.04)
            
    wadah_skor_animasi.markdown(f"<div class='final-score-box'>✨ {skor_target} POIN ✨</div>", unsafe_allow_html=True)
    st.balloons()
    
    st.markdown("""
    <div class='welcome-card' style='background-color: #2E86C1;'>
        <h2>🎈 YEY SKOR KAMU LUAR BIASA! 🎈</h2>
        <p style='font-size: 18px;'>Pertahankan kerja keras kalian! 💪</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 KEMBALI KE BERANDA (KELOMPOK BARU)", use_container_width=True):
        st.session_state.game_stage = 'home'
        st.rerun()
                
