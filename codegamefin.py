def main():
    print("="*40)
    print("🚂 SELAMAT DATANG DI KERETA UANG 🚂")
    print("="*40)
    
    # 1. Input Nama Tim
    nama_tim = input("Masukkan nama kelompok kalian: ")
    saldo = 10000
    
    print(f"\nSelamat datang, {nama_tim}!")
    print(f"Kalian memulai perjalanan dengan Saldo Awal: Rp{saldo}")
    print("Kelola uang kalian di setiap gerbong agar tidak bangkrut!\n")
    
    # 2. Data Gerbong (Daftar Barang dan Harga)
    gerbong_data = [
        {"gerbong": 1, "nama_toko": "Toko Minuman", "barang": "Air mineral botol kecil", "harga": 1000, "qty": 3},
        {"gerbong": 2, "nama_toko": "Toko Buku/Komik", "barang": "Buku komik mini", "harga": 1500, "qty": 2},
        {"gerbong": 3, "nama_toko": "Penjual Camilan", "barang": "Keripik kentang", "harga": 500, "qty": 5},
        {"gerbong": 4, "nama_toko": "Toko Buah", "barang": "Buah apel segar", "harga": 2000, "qty": 2},
        {"gerbong": 5, "nama_toko": "Suvenir Akhir", "barang": "Gantungan kunci kereta", "harga": 2500, "qty": 2}
    ]
    
    # 3. Looping / Perulangan untuk setiap gerbong
    for data in gerbong_data:
        print("-" * 40)
        print(f"🚂 GERBONG {data['gerbong']}: {data['nama_toko']} 🚂")
        print(f"Barang: {data['barang']}")
        print(f"Harga: Rp{data['harga']} / satuan")
        print(f"Ketentuan: Harus membeli {data['qty']} satuan sekaligus.")
        
        total_harga_asli = data['harga'] * data['qty']
        
        # Lapis 1: Hitung Total Harga (Wajib Benar)
        while True:
            try:
                tebakan_harga = int(input(f"Berapa total harga paket ini? (Ketik angkanya saja): "))
                if tebakan_harga == total_harga_asli:
                    print("✅ Jawaban benar! Toko terbuka.")
                    break
                else:
                    print("❌ Hitungan salah, coba hitung lagi ya!")
            except ValueError:
                print("⚠️ Harap masukkan angka yang valid.")
                
        # Lapis 2: Keputusan Beli atau Lewati
        while True:
            keputusan = input("Apakah kalian ingin membeli ini? (Ketik 'beli' atau 'lewati'): ").lower()
            if keputusan in ['beli', 'lewati']:
                break
            else:
                print("⚠️ Ketik 'beli' atau 'lewati' saja.")
                
        # Eksekusi Keputusan
        if keputusan == 'beli':
            if saldo < total_harga_asli:
                print("⚠️ Saldo kalian tidak cukup untuk membeli barang ini! Kalian terpaksa melewati gerbong ini.")
                continue # Langsung lanjut ke gerbong berikutnya
                
            # Tantangan Pengurangan (Wajib Benar)
            sisa_saldo_asli = saldo - total_harga_asli
            while True:
                try:
                    print(f"\nSaldo kalian saat ini Rp{saldo}. Total belanjaan Rp{total_harga_asli}.")
                    tebakan_saldo = int(input("Berapa sisa saldo kalian jika membeli ini? (Ketik angkanya): "))
                    if tebakan_saldo == sisa_saldo_asli:
                        print("✅ Transaksi berhasil!")
                        saldo = sisa_saldo_asli
                        break
                    else:
                        print("❌ Hitungan kembalian salah, coba hitung lagi!")
                except ValueError:
                    print("⚠️ Harap masukkan angka yang valid.")
        else:
            print("Kalian memilih untuk melewati toko ini. Saldo aman.")
            
        print(f"💰 Saldo Sementara: Rp{saldo}")
        print("-" * 40)
        
    # 4. Layar Akhir
    print("="*40)
    print("🏁 KERETA TIBA DI STASIUN AKHIR 🏁")
    print(f"Kelompok {nama_tim} berhasil menyelesaikan perjalanan!")
    print(f"Sisa Saldo Akhir Kalian: Rp{saldo}")
    print("="*40)

if __name__ == "__main__":
    main()
