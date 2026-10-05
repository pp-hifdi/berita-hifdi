# STATUS-SEKJEN.md - ringkasan pagi (dirawat Admin HIFDI; update tiap selesai kerjaan penting)

**Update terakhir:** 5 Okt 2026 (HIFDI: article-103 tayang, kategori Mutu, penolakan pasien di ruang gawat darurat; commit 2ae415e)

## HIFDI: ARTICLE-103 TAYANG (5 Okt 2026, manual atas ACC Prinsipal)

- **Judul:** Pasien Menolak Diperiksa Dokter Umum: Yang Wajib Dilakukan Fasyankes (kategori Mutu).
- **Asal isu:** unggahan akun @medicstory.id 5 Okt 2026 tentang pasien yang menolak diperiksa karena dokternya "cuma dokter umum". Prinsipal menetapkan sudut yang diangkat bukan polemik umum lawan spesialis, melainkan kewajiban dokter dan fasyankes.
- **Penting, status sumber:** unggahan itu tidak menyebut rumah sakit, tanggal, maupun sumber primer, jadi artikel menyatakannya tegas sebagai diskursus media sosial, bukan peristiwa terverifikasi. Jangan dipakai sebagai rujukan kasus nyata.
- **Isi:** kewajiban melayani lebih dulu (Pasal 174 UU 17/2023: wajib memberi pelayanan gawat darurat, dilarang menolak, dilarang minta uang muka, dilarang menunda karena administrasi); kewajiban pertolongan pertama (Pasal 275 ayat 1) dan perlindungan dari tuntutan ganti rugi (ayat 2); penanggung jawab pelayanan kegawatdaruratan adalah dokter atau dokter gigi, dan lampiran Permenkes 47/2018 menyebut dokter umum berkompetensi kegawatdaruratan sebagai Dokter Penanggung Jawab Pelayanan; lima langkah saat pasien menolak (triase tetap jalan, informasi lengkap sesuai Pasal 276, dokumentasi sesuai Pasal 296 dan Permenkes 24/2022, tawarkan jalan keluar, stabilisasi lalu rujuk); empat kesiapan fasyankes primer (penanggung jawab tertulis, kewenangan klinis, pelatihan berkala, alur rujukan).
- **Sumber:** 4 tautan, semuanya diuji HTTP 200 (UU 17/2023 di peraturan.bpk.go.id, Permenkes 47/2018 di persi.or.id, Permenkes 24/2022 di keslan.kemkes.go.id, unggahan @medicstory.id).
- **Gambar:** ilustrasi digital HIFDI (pasien duduk menolak dengan tangan bersedekap dan wajah menoleh menjauh, dokter menawarkan pemeriksaan), hero 1200x675 dan og 1200x630. Dipilih Prinsipal setelah beberapa kali revisi ekspresi.
- **Panjang:** 643 kata badan artikel. Em-dash nol.
- **Verifikasi mandiri (Hermes):** HEAD sama dengan origin/main (2ae415e); halaman live 200; hero dan og:image 200; beranda menampilkan kartu article-103 di posisi teratas dengan artikelCount 99; struktur lengkap (5 subjudul, 1 blockquote, kotak referensi, footer, div seimbang).
- **Caption WhatsApp Bangkit:** link preview lalu caption, terkirim sekali jalan. State caption sekarang menunjuk article-103.
- **Catatan proses gambar:** generator Qwen image kena batas kuota gratis (HTTP 403), produksi memakai jalur cadangan `~/bin/genimg.py` (model Wan). Pelajaran prompt sudah dicatat di skill visual-design-production.

## Riwayat singkat

- **article-102** (18 Sep 2026, Edukasi): EIB pada pendaki gunung, 658 kata, publish via Claude Code lalu diverifikasi Hermes, commit 3035214 dan 0da9d8e.
- **article-101** (11 Sep 2026, Advokasi): keracunan MBG Karo.

## Item yang masih butuh keputusan Prinsipal

1. **Nama bidang FMI.** Artikel memakai "Kepala Bidang Litbangnov (penelitian, pengembangan, dan inovasi) FMI" sesuai sebutan Prinsipal. Di repo Berita FMI sebutan yang sudah dipakai adalah "Pengurus FMI Bidang Litbang & Inovasi". Perlu satu penetapan supaya konsisten lintas portal.
2. **365 em-dash bawaan template di index.html root** (og:title, hero-legal, komentar kartu lama). Jumlahnya sama sebelum dan sesudah penerbitan article-101, 102, dan 103, jadi bukan dari artikel baru. Menunggu keputusan apakah dibersihkan.
3. **Kutipan dr. Putro untuk kanal lain** (5 butir hasil diskusi dan wawancara EIB) sudah disiapkan di `~/workspace/artikel-eib-pendaki/ARTIKEL-v5.md` bagian lampiran, belum dipakai di kanal mana pun.
