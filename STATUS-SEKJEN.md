# STATUS-SEKJEN.md - ringkasan pagi (dirawat Admin HIFDI; update tiap selesai kerjaan penting)

**Update terakhir:** 20 Nov 2026 (HIFDI: article-113 tayang, beban biaya strok dan skrining di fasyankes primer, diolah dari opini Prof. Akbar di Harian Waspada)

Portal berita HIFDI: 108 artikel internal. Nomor tertinggi article-113.

## Artikel terakhir

- **article-113** (Advokasi, 20 Nov 2026): "Negara Membayar Rp7,2 Triliun untuk Strok, tapi Skriningnya Baru Menyentuh Puskesmas". Diolah dari opini Prof. dr. Muhammad Akbar di Harian Waspada, halaman A6, 18 November 2026. Byline Redaksi Berita HIFDI, 889 kata, catatan redaksi mencantumkan sumber dan bahwa butir tuntutan adalah pengembangan redaksi.
- Lima sudut yang diangkat: pembiayaan BPJS (9,5 juta kasus, Rp7,2 triliun pada 2025, naik dari Rp2,55 triliun 2019), beban pada usia muda (IHME 19,42 persen lawan jantung iskemik 14,38 persen, 664.000 kasus baru per tahun, kenaikan 100 persen sebelum usia 70 sejak 1990), kesenjangan deteksi (90 persen dapat dicegah, capaian 11,3 persen), skrining jangan hanya di Puskesmas (inti advokasi: klinik pratama dan TPMD mitra JKN), serta tempat kerja dan literasi warga.
- Hero memakai foto konferensi pers KONAS XI PERDOSNI dan AOCN XX di Medan (Sumut Pos), atas pilihan Prinsipal. Kartu angka dipindah ke slide 1 galeri, halaman A6 Waspada jadi slide 2.
- Foto toga Prof. Akbar yang sempat dipakai pada draf pertama dibuang, berkasnya dihapus dari repo.
- Status teknis: commit 22b1c19, live https://berita.hifdi.id/article-113/ (HTTP 200), enam subjudul, satu blockquote, dua slide galeri, articleCount 108, sitemap memuat 113, caption WhatsApp Bangkit terkirim.
- Carousel Instagram 6 slide di `~/workspace/ig-113-strok/`, QR terverifikasi, dikirim ke WAG HIFDI Bangkit lewat bridge :3002 pada 20 Nov 2026 (1 pesan teks plus 6 slide). Menunggu unggahan petugas.

### Riwayat singkat

- **article-112** (Kabar HIFDI, 20 Nov 2026): "Prof. Muhammad Akbar Nakhodai PERDOSNI, HIFDI Soroti Deteksi Dini Stroke di Layanan Primer". Berita Kongres XI PERDOSNI dan AOCN XX di Medan, Rapat Pleno III 19 November 2026: Akbar 135 suara, Dr. dr. Fritz 101 suara dari 236 suara, selisih 34 suara atau 57,2 persen.
- Sudut HIFDI: beban stroke ada di hulu. Data Kemenkes 2024 (18,5 persen kematian, 11,2 persen kecacatan, prevalensi 8,3 per 1.000 penduduk SKI 2023, biaya Rp5,2 triliun, deteksi dini baru 11,3 persen dari target), lalu tiga tuntutan soal skrining di klinik pratama dan TPMD, protokol rujukan setara untuk mitra JKN, dan kolaborasi PERDOSNI dengan layanan primer.
- Bahan dari Prinsipal memuat narasi balapan MotoGP dan angka 3.005 dokter serta 31 cabang. Narasi balapan dibuang karena bukan gaya portal; angka anggota tidak dipakai karena tidak ada di pemberitaan mana pun.
- Kutipan Ketua Umum HIFDI dr. Zaenal Abidin, M.H. disusun redaksi sebagai blockquote (pola sama dengan article-109), bukan hasil wawancara.
- Galeri tiga slide di badan artikel: foto Prof. Akbar, foto Ketua Umum HIFDI (memakai berkas article-076, 588x330 sehingga agak lunak saat dibesarkan), dan kartu kutipan. Tinggi frame diseragamkan 340 px dengan object-fit agar tidak ada ruang kosong.
- Status teknis: commit e15b561, live https://berita.hifdi.id/article-112/ (HTTP 200), hero beranda berganti ke 112, articleCount 107, sitemap memuat 112, caption WhatsApp Bangkit terkirim.
- Catatan: foto Ketua Umum versi resolusi tinggi belum ada di aset; kalau Prinsipal mengirim file aslinya, ganti `images/article-112-zaenal-abidin.jpg`.
- Carousel Instagram 6 slide 1080x1350 dibuat di `~/workspace/ig-112-perdosni/`, QR terverifikasi, dan dikirim ke WAG HIFDI Bangkit lewat bridge :3002 pada 20 Nov 2026 (1 pesan teks plus 6 slide). Menunggu unggahan petugas.

### Riwayat singkat

- **article-111** (Advokasi, 18 Nov 2026): "Butuh Berapa Banyak Contoh Lagi: Potret Kesejahteraan Tenaga Medis Indonesia". Esai naskah kiriman Gigih Pratama, dokter lulusan Universitas Palangka Raya, Wakil Chief Nasional PIDI. Naskah dimuat utuh 1.140 kata, empat subjudul ditambahkan sebagai kemasan, satu blockquote dari kalimat penulis sendiri, tujuh butir referensi bertaut.
- Lima koreksi pada naskah kiriman: (1) rasio dokter "0,47 sampai 0,69" diganti 0,76 per 1.000 penduduk (Kemenkes, Des 2025) plus 0,19 untuk dokter spesialis; (2) angka 62 persen kekerasan kerja dipertahankan karena cocok dengan rilis PAHO 24 Sep 2026 (sempat dikira salah, ternyata benar); (3) klaim "Working for Health diinisiasi 2024" dibuang karena program ILO/OECD/WHO itu jalan sejak 2018; (4) "Badan Penjamin Jasa Kesehatan (BPJS)" dibetulkan jadi Badan Penyelenggara Jaminan Sosial dan klaim perlindungan hukum disandarkan ke Pasal 273 ayat (1) UU 17/2023; (5) kasus NTT dipertegas (RS Leona, TTU, 13 Jun 2026, tiga anggota DPRD berstatus tersangka, praperadilan ditolak Okt 2026).
- Foto penulis tidak dipasang di tengah narasi. Atas koreksi Prinsipal, foto dipotong persegi 96 px dan diletakkan di samping kiri kotak "Tentang penulis" di kaki artikel, di atas kotak referensi.
- Hero bukan ilustrasi AI melainkan kartu desain dari kit HIFDI (tiga angka kunci: 0,76, 733, 62 persen), karena kuota gambar DashScope balas 403 dan OpenRouter 402.
- Status teknis: commit cdf483a, live https://berita.hifdi.id/article-111/ (HTTP 200), hero beranda berganti ke 111, articleCount 106, sitemap memuat 111, caption WhatsApp Bangkit terkirim, wa_state.json last_article 111.

### Riwayat singkat (article-108 sampai 110)

- **article-108** (Kabar HIFDI, Okt 2026): "Empat Tahun HIFDI: Enam Langkah supaya Layanan Primer Tidak Berhenti di Kertas", Redaksi Berita HIFDI.
- **article-109** (Kabar HIFDI, 24 Okt 2026): "76 Tahun IDI, HIFDI Soroti Tiga Pekerjaan Rumah di Layanan Primer", lengkap dengan galeri dua slide.
- **article-110** (Kabar HIFDI, 28 Okt 2026): "Sumpah Pemuda ke-98: Pemuda Paling Rentan Depresi, Paling Jarang Berobat".
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

0. Caption WhatsApp untuk article-108, 109, dan 110 tidak pernah terkirim (wa_state.json berhenti di 107). Saat menerbitkan article-111, state dinaikkan ke 110 supaya grup tidak dibanjiri tiga artikel lama. Kirim susulan bila Prinsipal mau.
   - Carousel Instagram article-111 (6 slide 1080x1350, tipografi, QR terverifikasi) sudah dibuat di `~/workspace/ig-111-nakes/`, dikirim ke WAG HIFDI Bangkit lewat bridge :3002 pada 18 Nov 2026, dan atas permintaan Prinsipal ikut ditanam di badan artikel sebagai galeri geser kanan-kiri (bagian "Ringkasan dalam enam slide", sebelum kotak referensi). Menunggu unggahan petugas.
1. Versi Instagram carousel untuk article-106 menunggu pilihan desain dari tiga opsi yang diajukan (editorial gelap, putih bersih dengan ilustrasi, tipografi kutipan).
2. Naskah karhutla dan beban layanan primer (Advokasi) sudah selesai dan diserahkan, belum dirakit ke portal. Data masih berhenti di BNPB 12 Okt 2026, perlu pemutakhiran sebelum tayang, dan sudutnya perlu dipertajam ke pembiayaan klinik pratama serta TPMD karena kolom article-106 sudah membahas karhutla dari sisi kebijakan.
3. 365 em-dash bawaan template di index.html root (bukan dari artikel baru) belum dibersihkan, menunggu keputusan.
4. Artikel perjalanan persalinan darurat versi Mutu (sudut kesiapan fasyankes, alur rujukan maternal) selesai sebagai draf tetapi batal tayang karena sudut pandang diganti ke Advokasi. Bisa dipakai lain waktu.
