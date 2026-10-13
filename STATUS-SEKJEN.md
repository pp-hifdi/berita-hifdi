# STATUS-SEKJEN.md - ringkasan pagi (dirawat Admin HIFDI; update tiap selesai kerjaan penting)

**Update terakhir:** 13 Okt 2026 (HIFDI: article-104 tayang, kategori Advokasi, soal dokter yang harus nyambi jadi pengemudi)

Portal berita HIFDI: 100 artikel internal. Nomor tertinggi article-104.

## Artikel terakhir
- **article-104** (Advokasi, 13 Okt 2026): "Heroik, tapi Tidak Seharusnya Terjadi: Kenapa Dokter Sampai Harus Nyambi". Pemantik: kisah Dokter Rosa, dokter umum yang menyambi pengemudi taksi online di Surabaya (19 Jan 2026) dan membantu penumpangnya melahirkan di mobil. Isi: kritik pembiayaan layanan primer, kapitasi Rp9.000 sampai Rp16.000 per peserta per bulan (Permenkes 3/2023, tidak naik sejak 2023), ilustrasi Rp45 juta sebulan per klinik 5.000 peserta, insentif Rp30 juta sebulan untuk satu dokter spesialis di daerah terpencil, usulan pendapatan minimum IDI yang masih dikaji. Nada: pemantik heroik dipakai untuk menarik simpati lalu dibelokkan ke kritik kebijakan, dan dalih "suka-suka orang mencari uang lebih" dibantah di awal.
- Sudut pandang: bukan soal hak dokter mencari nafkah, tetapi sistem yang membuat pilihan itu terasa wajib. Prinsipal minta penekanan: negara jangan menunggangi niat baik tenaga medis.
- Gaya yang dipakai dan disetujui Prinsipal: pembuka dan penutup formal, bagian tengah ringan, kalimat pendek, detail tetap lengkap (nomor regulasi, tahun, angka). Badan artikel 260 kata.
- Gambar: ilustrasi digital (dokter perempuan menyetir dengan jas putih dan stetoskop, penumpang ibu hamil di kursi belakang). Prinsipal memilih varian pertama. Generate lewat skrip cadangan karena kuota Qwen image habis.

## Catatan cara kerja (agar tidak terulang)
- Prinsipal menolak heading "Yang HIFDI tuntut" (dinilai norak) dan menolak diksi njelimet. Detail, tanggal, dan nomor regulasi tetap wajib ada.
- Ilustrasi: model gambar cenderung membuat semua orang tersenyum dan sosok dokter laki-laki. Perlu dinyatakan tegas "not smiling", "woman doctor", "pregnant woman on the back seat".
- Urutan kerja yang dipakai: draf naskah, ACC Prinsipal, rakit article-XXX dari template tertinggi, kartu di posisi teratas, articleCount naik manual, commit dan push, verifikasi live, jalankan skrip caption WhatsApp sekali, update berkas ini.

## Item yang masih butuh keputusan Prinsipal
1. 365 em-dash bawaan template di index.html root (bukan dari artikel baru) belum dibersihkan, menunggu keputusan.
2. Artikel perjalanan persalinan darurat versi Mutu (sudut kesiapan fasyankes, alur rujukan maternal) sudah selesai sebagai draf di workspace tetapi batal ditayangkan karena sudut pandangnya diganti ke Advokasi. Bisa dipakai lain waktu.
