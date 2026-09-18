# STATUS-SEKJEN.md — ringkasan pagi (dirawat Admin HIFDI; update tiap selesai kerjaan penting)

**Update terakhir:** 18 Sep 2026 (HIFDI: article-102 tayang, Edukasi, EIB dan kelaikan pendakian; commit 3035214 dan 0da9d8e)

## HIFDI — ARTICLE-102 TAYANG (18 Sep 2026, manual atas ACC Prinsipal)
- **Judul:** Bukan Kurang Latihan: Sesak Napas Justru Muncul Setelah Mendaki (kategori Edukasi).
- **Sasaran pembaca:** pendaki gunung, supaya istilah bronkokonstriksi akibat olahraga (EIB) dikenal di komunitas pendakian. Menyimpang dari pembaca baku portal yang pengelola fasyankes primer, dan ini keputusan Prinsipal.
- **Isi:** mekanisme EIB (ventilasi sampai sekitar 200 liter per menit, udara dingin dan kering menguapkan lapisan air saluran napas, sel mast melepas histamin, leukotrien, dan prostaglandin); kaitan konkret dengan proses mendaki (pada atlet ketahanan kapasitas aerobik turun 6,3 persen per 1.000 meter dan daya tahan sampai kelelahan turun 14,5 persen, Wehrlin dan Hallen 2006); tiga peringatan (serangan berat pada asma belum terkontrol, inhaler bisa rusak karena dingin, sesak di ketinggian tidak selalu EIB); arah kelaikan pendakian dengan uji beban termasuk VO2 Max dan pemeriksaan fungsi paru; kutipan dr. Putro S. Muhammad MH CIHL atas nama Kepala Bidang Litbangnov FMI (atas permintaan Prinsipal).
- **Sumber:** 6 referensi, 5 bertaut hidup dan sudah diuji HTTP 200 (StatPearls, PubMed Wehrlin, PubMed Durand, UIAA, GAAPP), 1 tanpa tautan karena akses ditolak otomatis (Doan dan Luks, Wilderness and Environmental Medicine 2014).
- **Gambar:** foto Wikimedia Commons (Timothy A. Gonsalves, CC BY-SA 4.0), hero 1200x675 dan og 1200x630, kredit tampil di halaman.
- **Panjang:** 658 kata badan artikel, 8 kata di atas rentang 550 sampai 650 karena tambahan materi kelaikan dan kutipan. Dilaporkan apa adanya ke Prinsipal.
- **Rakit dan publish:** via Claude Code (claude-task, akun utama) sesuai kebijakan AI. Claude kena "Reached max turns" setelah commit dan push; Hermes memverifikasi mandiri dan menemukan satu penyimpangan: Claude menulis dek versinya sendiri, lalu dek disamakan dengan naskah yang disetujui lewat commit 0da9d8e.
- **Verifikasi mandiri (Hermes):** rev-parse lokal sama dengan origin/main; halaman live 200; hero dan og:image 200; jumlah folder artikel 98 dan articleCount 98; em-dash nol di artikel; keterangan gambar tampil; kemiripan teks badan artikel dengan naskah 98,5 persen dan seluruh selisihnya hanya judul bagian.
- **Caption WhatsApp Bangkit:** terkirim sekali jalan (link preview lalu caption), state caption sekarang menunjuk article-102.

## Item yang masih butuh keputusan Prinsipal
1. **Nama bidang FMI.** Artikel memakai "Kepala Bidang Litbangnov (penelitian, pengembangan, dan inovasi) FMI" sesuai sebutan Prinsipal. Di repo Berita FMI sebutan yang sudah dipakai adalah "Pengurus FMI Bidang Litbang & Inovasi". Perlu satu penetapan supaya konsisten lintas portal.
2. **365 em-dash bawaan template di index.html root** (og:title, hero-legal, komentar kartu lama). Jumlahnya sama sebelum dan sesudah penerbitan article-101 dan 102, jadi bukan dari artikel baru. Menunggu keputusan apakah dibersihkan.
3. **Kutipan dr. Putro untuk kanal lain** (5 butir hasil diskusi dan wawancara) sudah disiapkan di `~/workspace/artikel-eib-pendaki/ARTIKEL-v5.md` bagian lampiran, belum dipakai di kanal mana pun.
