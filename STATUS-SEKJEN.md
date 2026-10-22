# STATUS-SEKJEN.md - ringkasan pagi (dirawat Admin HIFDI; update tiap selesai kerjaan penting)

**Update terakhir:** 22 Okt 2026 (HIFDI: article-107 tayang, naskah kiriman Dr. Lucy Widasari soal perubahan iklim dan kesehatan ibu, dengan galeri geser)

Portal berita HIFDI: 103 artikel internal. Nomor tertinggi article-107.

## Artikel terakhir

- **article-107** (Advokasi, 22 Okt 2026): "Ketika Bumi Memanas, Rahim Ibu Ikut Menanggung Luka". Naskah kiriman Dr. dr. Lucy Widasari, M.Si. (praktisi kesehatan, dosen, pemerhati kesehatan dan gizi, anggota Healthy Mother Healthy Babies), dimuat utuh 957 kata. Empat subjudul asli dipertahankan.
- Isi: ketidakadilan iklim, dampak panas ekstrem dan PM2,5 sejak dalam kandungan, peran layanan primer sebagai garda terdepan, dan seruan agar krisis tidak diwariskan. Klaim tinjauan Bekkar dkk (2020) sudah diverifikasi ke sumber aslinya: 68 studi, 57 signifikan, total 32.798.152 kelahiran.
- **Galeri geser kanan kiri** di badan artikel, pola meniru IHSC: empat slide berisi ilustrasi hero, infografis Bu Lucy, foto USAID Indonesia (domain publik) soal ibu hamil didampingi tenaga kesehatan, dan foto sawah retak karya Joko Wardani (CC BY-SA 4.0). Ada panah, penghitung 1/4, dan thumbnail. Caption di bawah gambar, bukan overlay.
- Gambar hero: ilustrasi generated, bidan memeriksa ibu hamil di klinik pratama saat panas. Prinsipal meminta perut ibu tertutup pakaian, jadi ilustrasi dibuat ulang dengan gaun hamil panjang.
- Status teknis: commit 690c428 (terbit) dan db7cc14 (revisi), live https://berita.hifdi.id/article-107/ (HTTP 200), hero beranda berganti ke 107, kartu 106 kembali ke grid, articleCount 103, caption WhatsApp Bangkit terkirim, wa_state.json last_article 107.
- **Revisi 22 Okt 2026 (hasil audit):** struktur paragraf diperbaiki (sempat tergabung jadi 6 blok panjang, sekarang 27 paragraf sesuai naskah), ditambah dua paragraf data yaitu SKI 2023 (anemia 27,7 persen, risiko KEK 16,9 persen, konsumsi TTD 44,2 persen) dan data WHO (3,6 miliar orang di kawasan rentan, kematian panas usia di atas 65 tahun naik 70 persen dalam dua dekade), dek diberi tanda petik karena mengutip kalimat penulis, kotak referensi bertambah jadi 4 butir, plus catatan redaksi di akhir artikel. Naskah penulis tidak diubah, 27 blok naskah terverifikasi masih utuh.
- **Carousel Instagram 6 slide sudah disiapkan** di `~/workspace/ig-107-lucy/`: cover, dampak sejak dalam kandungan, data Indonesia, lalu dua slide diagram rantai dampak, dan penutup dengan QR ke artikel. Infografis Bu Lucy tidak dipotong lagi, isinya digambar ulang sebagai diagram portrait 1080x1350 (bagian 1: panas sampai plasenta, bagian 2: luaran kehamilan, faktor non-biologis, kelompok rentan, plus strip trimester), dengan kredit "digambar ulang dari infografik Dr. dr. Lucy Widasari". Semua slide ada logo HIFDI dan nomor, QR sudah diuji baca.

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
