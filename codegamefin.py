import streamlit as st
import time

# 1. Konfigurasi Halaman & CSS Khusus (Tema POV Masinis)
st.set_page_config(page_title="Kereta Uang POV", page_icon="🚂", layout="centered")

st.markdown("""
<style>
    /* Latar belakang keseluruhan */
    .stApp { background-color: #87CEEB; } /* Warna Langit */
    
    /* Area Jendela POV (Tempat GIF/Gambar) */
    .pov-window {
        background-color: #228B22; /* Warna Tanah (Placeholder) */
        border: 10px solid #2F4F4F;
        border-radius: 20px 20px 0 0;
        height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 2px 2px 4px #000000;
        margin-bottom: -20px;
    }
    
    /* Area Dasbor Masinis (Hitam/Gelap) */
    .dashboard-panel {
        background-color: #2C3E50;
        padding: 30px;
        border-radius: 0 0 20px 20px;
        color: white;
        box-shadow: 0px -5px 15px rgba(0,0,0,0.5);
    }
    
    /* Kotak Pop-up Pertanyaan */
    .popup-box {
        background-color: #FFFACD;
        border: 4px solid #000000;
        border-radius: 15px;
        padding: 20px;
        color: #000000;
        text-align: center;
        box-shadow: 5px 5px 0px #000000;
        margin-bottom: 20px;
    }
    
    /* Tampilan Layar Digital Dasbor */
    .digital-screen {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Courier New', Courier, monospace;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        border: 2px solid #555;
    }
</style>
""", unsafe_allow_html=True)

# 2. Manajemen Status Sesi (Session State)
if 'tahap' not in st.session_state:
    st.session_state.tahap = 'mulai'
    st.session_state.saldo = 20000
    st.session_state.pos_saat_ini = 0
    st.session_state.inventaris = []

# Data Pos (Pertanyaan & Hitungan)
DATA_POS = [
    {"pos": 1, "masalah": "Ban sepeda bocor!", "barang": "Pompa", "harga": 2000, "qty": 1},
    {"pos": 2, "masalah": "Buku hilang sebelum ujian!", "barang": "Buku Tulis", "harga": 3000, "qty": 2},
    {"pos": 3, "masalah": "Perut sangat lapar!", "barang": "Roti", "harga": 1500, "qty": 3},
]

# 3. Logika Antarmuka (UI)
if st.session_state.tahap == 'mulai':
    st.markdown("<div class='pov-window'>🚂 KERETA UANG SIAP BERANGKAT 🚂</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='dashboard-panel'>
        <h2 style='text-align:center;'>Sistem Dinyalakan</h2>
        <p style='text-align:center;'>Bawa kereta sampai stasiun akhir dengan saldo tersisa. Semakin besar saldo, semakin banyak hadiah Superstar!</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Mulai Perjalanan (Tarik Tuas)", use_container_width=True):
        st.session_state.tahap = 'perjalanan'
        st.rerun()

elif st.session_state.tahap == 'perjalanan':
    idx = st.session_state.pos_saat_ini
    data = DATA_POS[idx]
    total_harga = data['harga'] * data['qty']
    
    # Visual Jendela (Bisa diganti dengan st.image untuk GIF POV Kereta)
    st.markdown(f"<div class='pov-window'>Melintasi Pos {data['pos']}...</div>", unsafe_allow_html=True)
    
    # Area Dasbor
    st.markdown("<div class='dashboard-panel'>", unsafe_allow_html=True)
    
    # Layar Status Saldo
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='digital-screen'>SALDO: Rp {st.session_state.saldo:,}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='digital-screen'>POS: {data['pos']} / {len(DATA_POS)}</div>", unsafe_allow_html=True)
    
    st.write("---")
    
    # Kotak Pop Up Masalah (Tengah Dasbor)
    st.markdown(f"""
    <div class='popup-box'>
        <h3>🚨 PERINGATAN!</h3>
        <p style='font-size: 18px;'><b>{data['masalah']}</b></p>
        <p>Beli {data['qty']} <b>{data['barang']}</b> (Harga: Rp {data['harga']}/pcs)?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hitungan Matematika
    st.write(f"Hitung total harga {data['qty']} {data['barang']}:")
    jawaban_harga = st.number_input("Total Harga (Rp)", min_value=0, step=500, key=f"hitung_{idx}")
    
    if jawaban_harga > 0:
        if jawaban_harga == total_harga:
            st.success("✅ Hitungan Benar! Pilih tindakan:")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔴 BELI (Potong Saldo)", use_container_width=True):
                    if st.session_state.saldo >= total_harga:
                        st.session_state.saldo -= total_harga
                        st.session_state.inventaris.append(data['barang'])
                        st.session_state.tahap = 'evaluasi_pos'
                        st.rerun()
                    else:
                        st.error("Saldo tidak cukup!")
            with c2:
                if st.button("🟢 LEWATI (Simpan Uang)", use_container_width=True):
                    st.session_state.tahap = 'evaluasi_pos'
                    st.rerun()
        else:
            st.error("❌ Hitungan salah! Coba lagi.")
            
    st.markdown("</div>", unsafe_allow_html=True) # Tutup Dasbor

elif st.session_state.tahap == 'evaluasi_pos':
    if st.session_state.pos_saat_ini < len(DATA_POS) - 1:
        st.session_state.pos_saat_ini += 1
        st.session_state.tahap = 'perjalanan'
    else:
        st.session_state.tahap = 'akhir'
    st.rerun()

elif st.session_state.tahap == 'akhir':
    st.balloons()
    st.markdown("<div class='pov-window'>🏁 STASIUN AKHIR 🏁</div>", unsafe_allow_html=True)
    
    saldo_akhir = st.session_state.saldo
    if saldo_akhir >= 10000:
        superstar = 10
    elif saldo_akhir >= 5000:
        superstar = 5
    elif saldo_akhir >= 1000:
        superstar = 2
    else:
        superstar = 0
        
    st.markdown(f"""
    <div class='dashboard-panel'>
        <h2 style='text-align:center;'>Laporan Perjalanan</h2>
        <div class='digital-screen' style='font-size:24px; margin-bottom:20px;'>SISA SALDO: Rp {saldo_akhir:,}</div>
        <div class='popup-box' style='background-color:#E8F8F5;'>
            <h3 style='color:#2E86C1;'>🎁 HADIAH: {superstar} SUPERSTAR 🎁</h3>
        </div>
        <p><b>Barang Dibeli:</b> {', '.join(st.session_state.inventaris) if st.session_state.inventaris else 'Tidak ada'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Main Lagi"):
        st.session_state.clear()
        st.rerun()
    
