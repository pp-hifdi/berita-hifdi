# STATUS-SEKJEN.md - ringkasan pagi (dirawat Admin HIFDI; update tiap selesai kerjaan penting)

**Update terakhir:** 20 Okt 2026 (HIFDI: article-105 tayang, kategori Advokasi, soal ukuran kemajuan kesehatan dan akses layanan primer)

Portal berita HIFDI: 101 artikel internal. Nomor tertinggi article-105.

## Artikel terakhir

- **article-105** (Advokasi, 20 Okt 2026): "10.000 Puskesmas Direnovasi, HIFDI: yang Penting Warga Bisa Sampai ke Layanan". Badan artikel 223 kata. Peg berita: pidato nota keuangan RAPBN 2027 (14 Agu 2026), rencana renovasi 10.000 puskesmas dengan sekitar Rp4 miliar per puskesmas, 514 Labkesmas, serta ambulans udara dan dokter terbang.
- Isi: kesehatan sebagai investasi tetapi gedung baru belum tentu jadi layanan baru (Mensesneg: 60 persen atau 6.000 puskesmas belum punya dokter gigi), ambulans udara menjawab jarak tetapi tidak menjawab biaya, kapitasi klinik pratama Rp9.000 sampai Rp16.000 per peserta per bulan (Permenkes 3/2023) tidak bergerak saat kunjungan naik, dan rujukan selalu dimulai di layanan primer.
- Tuntutan Posisi HIFDI: penguatan layanan primer harus mencakup klinik pratama dan TPMD mitra JKN, tarif kapitasi ditinjau sesuai biaya nyata, data akses per fasilitas dibuka.
- Gambar: ilustrasi AI (warga menempuh jalan jauh menuju klinik pratama), varian kedua yang dipilih Prinsipal. Dua varian pertama dibuang karena papan nama keluar tulisan ngawur dan ada palang merah.
- Status teknis: commit 61c9ef9, live https://berita.hifdi.id/article-105/ (HTTP 200), beranda menampilkan kartu teratas, articleCount 100 ke 101, caption WhatsApp Bangkit terkirim, wa_state.json last_article 105.

## Catatan cara kerja (agar tidak terulang)

- Prinsipal minta artikel pendek dan mudah dipahami masyarakat, bukan sekadar ringkas secara teknis. Versi pertama 421 kata ditolak secara implisit ("jangan terlalu panjang"), versi tayang 223 kata dengan kalimat pendek dan istilah awam.
- Prinsipal minta gambar selalu hasil generate, bukan mencari foto stok. Foto Commons hanya dipakai kalau diminta.
- Generate gambar harus dicek mata agent sebelum ditawarkan: larangan teks dan larangan palang merah wajib masuk prompt, dan hasilnya tetap bisa keluar tulisan ngawur di papan nama.
- Artikel Advokasi tidak boleh bergantung pada satu pembicara atau satu unggahan media sosial. Prinsipal minta artikel berdiri sendiri dengan peg berita resmi.

## Beranda (perubahan 20 Okt 2026)

- Beranda kini memakai hero artikel terbaru di bagian atas (gambar besar, label Terbaru, kategori, judul, dek, tanggal, tautan Baca selengkapnya) mengikuti pola Berita FMI.
- Grid berita dipotong 9 kartu per halaman dengan pagination bernomor plus panah sebelumnya dan berikutnya, plus teks Halaman X dari Y. Angka artikel di atas grid mengikuti jumlah hasil filter.
- Parameter URL dipakai: `?page=N` dan `?kategori=advokasi|edukasi|mutu|kabar-hifdi`, jadi halaman bisa dibagikan langsung.
- Blok profil organisasi memakai hero lama (label, judul HIFDI, deskripsi, dasar hukum SK, foto rapat yang menaut ke halaman tentang kami) dan ditempatkan di bawah pagination sebagai penutup, sebelum footer. Judulnya memakai h2 supaya halaman tetap punya satu h1 di hero berita.
- Konsekuensi untuk penerbitan berikutnya: setiap artikel baru WAJIB memperbarui blok hero (gambar, judul, dek, tanggal, tautan) dan menghapus kartu artikel itu dari grid, karena hero dan grid tidak lagi berbagi data otomatis.

## Item yang masih butuh keputusan Prinsipal

1. Naskah karhutla dan beban layanan primer (Advokasi) sudah selesai dan diserahkan, belum dirakit ke portal. Data masih berhenti di BNPB 12 Okt 2026, perlu pemutakhiran sebelum tayang.
2. 365 em-dash bawaan template di index.html root (bukan dari artikel baru) belum dibersihkan, menunggu keputusan.
3. Artikel perjalanan persalinan darurat versi Mutu (sudut kesiapan fasyankes, alur rujukan maternal) selesai sebagai draf tetapi batal tayang karena sudut pandang diganti ke Advokasi. Bisa dipakai lain waktu.
