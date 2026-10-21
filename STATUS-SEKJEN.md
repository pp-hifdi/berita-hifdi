# STATUS-SEKJEN.md - ringkasan pagi (dirawat Admin HIFDI; update tiap selesai kerjaan penting)

**Update terakhir:** 21 Okt 2026 (HIFDI: article-106 tayang, kolom Zaenal Abidin soal meja rapat dipindah ke tengah asap dan lumpur)

Portal berita HIFDI: 102 artikel internal. Nomor tertinggi article-106.

## Artikel terakhir

- **article-106** (Advokasi, 21 Okt 2026): "Dari Ruang Ber-AC ke Tengah Asap dan Lumpur: Pindahkan Meja Rapat ke Tempat Rakyat Menanggung Derita". Naskah kiriman tokoh, byline Zaenal Abidin (Ketua Umum PB IDI 2012-2015; Ketua HIFDI), dimuat utuh 1.172 kata tanpa dipotong. Sumber asli kolom Pinisi.co.id, 21 Oktober 2026.
- Isi: pembuka kisah Umar bin Khattab memikul gandum, tesis bahwa kebijakan kesehatan dirumuskan terlalu jauh dari lokasi bencana, karhutla sebagai bencana kesehatan yang menyamar sebagai bencana lingkungan, dampak galodo Marapi dan pencemaran Citarum, tenaga kesehatan posko sebagai saksi kunci, lalu enam rekomendasi termasuk rapat di lokasi terdampak dan ruang aman berudara bersih di tingkat RT/RW.
- Kemasan: enam subjudul asli jadi heading, satu kalimat jadi blockquote, kotak referensi 3 tautan (kolom Pinisi, WHO 2016, rilis Kemenkes 21 Agustus 2026), semua HTTP 200. Gambar generated, varian rapat di kampung berasap yang dipilih Prinsipal.
- Status teknis: commit d46b5ff, live https://berita.hifdi.id/article-106/ (HTTP 200), hero beranda berganti ke 106, kartu 105 kembali masuk grid, articleCount 101 ke 102, caption WhatsApp Bangkit terkirim, wa_state.json last_article 106.
- Catatan urutan deploy: Cloudflare sempat menyajikan versi lama sekitar empat menit, artikel baru 404 sampai deploy selesai. Jangan lapor gagal dari percobaan pertama, poll sampai 200.

## Beranda (perubahan 20 Okt 2026)

- Beranda kini memakai hero artikel terbaru di bagian atas (gambar besar, label Terbaru, kategori, judul, dek, tanggal, tautan Baca selengkapnya) mengikuti pola Berita FMI.
- Grid berita dipotong 9 kartu per halaman dengan pagination bernomor plus panah sebelumnya dan berikutnya, plus teks Halaman X dari Y. Angka artikel di atas grid mengikuti jumlah hasil filter.
- Parameter URL dipakai: `?page=N` dan `?kategori=advokasi|edukasi|mutu|kabar-hifdi`, jadi halaman bisa dibagikan langsung.
- Blok profil organisasi memakai hero lama (label, judul HIFDI, deskripsi, dasar hukum SK, foto rapat yang menaut ke halaman tentang kami) dan ditempatkan di bawah pagination sebagai penutup, sebelum footer. Judulnya memakai h2 supaya halaman tetap punya satu h1 di hero berita.
- Konsekuensi untuk penerbitan berikutnya: setiap artikel baru WAJIB memperbarui blok hero (gambar, judul, dek, tanggal, tautan), mengembalikan kartu artikel sebelumnya ke grid, dan menaikkan articleCount.

## Catatan cara kerja (agar tidak terulang)

- Prinsipal minta artikel pendek dan mudah dipahami masyarakat, bukan sekadar ringkas secara teknis. Versi pertama 421 kata ditolak secara implisit ("jangan terlalu panjang"), versi tayang 223 kata dengan kalimat pendek dan istilah awam.
- Prinsipal minta gambar selalu hasil generate, bukan mencari foto stok. Foto Commons hanya dipakai kalau diminta.
- Generate gambar harus dicek mata agent sebelum ditawarkan: larangan teks, larangan palang merah, dan larangan seragam militer wajib masuk prompt.
- Artikel Advokasi tidak boleh bergantung pada satu pembicara atau satu unggahan media sosial. Prinsipal minta artikel berdiri sendiri dengan peg berita resmi.
- Naskah kiriman tokoh tidak dipotong: yang dikemas ulang hanya struktur (heading, blockquote, kotak referensi), isi kalimat penulis dibiarkan utuh.

## Item yang masih butuh keputusan Prinsipal

1. Versi Instagram carousel untuk article-106 menunggu pilihan desain dari tiga opsi yang diajukan (editorial gelap, putih bersih dengan ilustrasi, tipografi kutipan).
2. Naskah karhutla dan beban layanan primer (Advokasi) sudah selesai dan diserahkan, belum dirakit ke portal. Data masih berhenti di BNPB 12 Okt 2026, perlu pemutakhiran sebelum tayang, dan sudutnya perlu dipertajam ke pembiayaan klinik pratama serta TPMD karena kolom article-106 sudah membahas karhutla dari sisi kebijakan.
3. 365 em-dash bawaan template di index.html root (bukan dari artikel baru) belum dibersihkan, menunggu keputusan.
4. Artikel perjalanan persalinan darurat versi Mutu (sudut kesiapan fasyankes, alur rujukan maternal) selesai sebagai draf tetapi batal tayang karena sudut pandang diganti ke Advokasi. Bisa dipakai lain waktu.
