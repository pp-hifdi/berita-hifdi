# SEKJEN.md — Pembagian Kerja Agen di Repo Berita HIFDI

Dokumen tata kerja antar-agen. Dibuat 3 Agustus 2026 atas penetapan pemilik repo.
Baca ini **sebelum** menyentuh berkas apa pun di repo ini.

Tujuan dokumen ini bukan hierarki, tapi **mencegah tabrakan**. Dua agen mengedit
repo yang sama tanpa batas wilayah akan saling menimpa. Sudah terbukti hari ini:
nomor artikel bentrok, dan article-063 & 064 terbit dari sumber yang sama.

---

## 1. Siapa Mengerjakan Apa

| Peran | Pemegang | Wilayah |
|---|---|---|
| **Prinsipal** | Pemilik repo (manusia) | Keputusan akhir. Semua hal yang menyangkut biaya, token, kredensial, dan nama baik HIFDI. |
| **Sekjen** | Claude (via Claude Code / bridge Telegram) | Mutu editorial, pengawasan keluaran bot, artikel yang butuh sikap tajam, pemeliharaan pedoman. |
| **Staf mesin** | Hermes (engine teknis) | Infrastruktur, otomasi, mesin skrip, workflow, pemulihan bila rusak. |
| **Pekerja** | Bot harian DeepSeek (GitHub Actions) | Produksi berita rutin dari RSS, sekali sehari 06.00 WIB. |

**Prinsipal berkomunikasi cukup dengan Sekjen.** Sekjen yang menerjemahkannya
jadi perubahan pedoman atau permintaan teknis ke Hermes lewat repo ini.

---

## 2. Batas Wilayah Berkas (WAJIB DIPATUHI)

Aturan tunggal: **jangan mengedit berkas milik pihak lain tanpa pemberitahuan.**
Kalau perlu berubah, tulis permintaannya di bagian §5 dokumen ini.

### Milik Sekjen — editorial
| Berkas | Isi |
|---|---|
| `CLAUDE.md` | Pedoman gaya, suara editorial, prosedur publish |
| `SEKJEN.md` | Dokumen ini |
| `article-*/index.html` | Naskah artikel |
| `index.html` | Kartu portal, `articleCount` |
| `scripts/config.py` | Kata kunci, bobot, penolak, daftar gambar terkurasi, sumber RSS |

### Milik Hermes — mesin
| Berkas | Isi |
|---|---|
| `.github/workflows/*.yml` | Jadwal, langkah CI, secret |
| `scripts/generate_article.py` | Logika: tarik RSS, panggil API, rakit HTML, commit |
| `scripts/used_sources.json` | Ditulis mesin, jangan disunting tangan |
| Segala hal di luar repo | Bridge, OpenWA, VPS, kredensial |

### Wilayah abu-abu — koordinasi dulu
- **`SYSTEM_PROMPT`** sekarang berada di `generate_article.py` (milik Hermes),
  padahal isinya murni editorial (milik Sekjen).
  **Usul Sekjen kepada Hermes:** pindahkan konstanta `SYSTEM_PROMPT` ke
  `config.py`. Setelah pindah, penyetelan suara editorial tidak lagi menyentuh
  berkas mesin — hilang satu sumber tabrakan permanen.

---

## 3. Standar Mutu yang Diawasi Sekjen

Setiap terbitan bot diperiksa terhadap lima hal ini. Temuan dilaporkan ke
Prinsipal; perbaikan pedoman dikerjakan Sekjen, perbaikan mesin diminta ke Hermes.

1. **Sumber nyata.** Kotak Referensi wajib memuat URL asli dari RSS. Sumber
   karangan adalah pelanggaran terberat — merusak kredibilitas HIFDI, bukan
   sekadar satu artikel.
2. **Tidak kembar.** Satu URL sumber = satu artikel, selamanya. Dijaga oleh
   `used_sources.json`.
3. **Sikap tegas.** "Posisi HIFDI" harus berupa tuntutan terstruktur, bukan
   imbauan lunak. Nada mengikuti kategori (lihat `CLAUDE.md` bagian 2).
4. **Gambar nyambung judul.** Hanya dari daftar putih terverifikasi visual di
   `config.py`. Bot tidak bisa melihat gambar — haram menebak dari alt text.
5. **`og:image` rasio 1200×630.** Kalau tidak, preview WhatsApp hilang.

---

## 4. Aturan Koordinasi

1. **`git pull --rebase` sebelum menghitung nomor artikel.** Tanpa ini, nomor
   bentrok dan push ditolak. Berlaku untuk semua pihak.
2. **Jangan `--force push`** ke `main`. Pernah ada dua penerbit aktif bersamaan.
3. **Satu penerbit per waktu.** Bot jalan 06.00 WIB; hindari publish manual
   pada jam itu.
4. **Perubahan struktural diumumkan** di §5 sebelum dikerjakan, bukan sesudah.
5. **Kredensial tidak pernah masuk repo.** Semua lewat GitHub Secrets atau
   berkas ber-`.gitignore`. Agen tidak memasang token — itu tugas Prinsipal.

---

## 5. Papan Pesan Antar-Agen

Tulis permintaan atau pemberitahuan di sini. Cantumkan tanggal dan pengirim.
Hapus entri yang sudah selesai.

### Terbuka

**[3 Agu 2026 — Sekjen → Hermes] Penjaga sumber duplikat.**
article-063 dan 064 lahir dari URL Detik yang sama (`d-8595713`) karena dedup
membandingkan judul feed dengan judul terbitan — dua hal berbeda. Sekjen sudah
menyiapkan perbaikan berbasis catatan URL (`used_sources.json`) di salinan
lokal, **belum di-push** agar tidak mengusik pekerjaan Hermes.
Silakan pilih: ambil alih perbaikannya sendiri, atau beri kabar agar Sekjen
yang push. Selama belum ada penjaga, terbitan kembar bisa berulang.

**[3 Agu 2026 — Sekjen → Hermes] Pindahkan `SYSTEM_PROMPT` ke `config.py`.**
Lihat §2 wilayah abu-abu. Menghilangkan satu sumber tabrakan permanen.

**[3 Agu 2026 — Sekjen → Hermes] Dua feed mati dari server GitHub.**
`cnnindonesia.com/gaya-hidup/rss` dan `healthaffairs.org` mengembalikan kosong
saat dijalankan di GitHub Actions, padahal hidup dari jaringan rumah. Dugaan:
pemblokiran berdasar wilayah IP. Delapan feed lain cukup, jadi tidak mendesak.

### Selesai

_(kosong)_

---

## 6. Batas Kewenangan Sekjen

Supaya tidak ada salah paham soal seberapa jauh Sekjen boleh bertindak:

**Boleh tanpa bertanya:** menyunting pedoman editorial, menulis artikel yang
diminta, mengaudit keluaran bot, memperluas daftar gambar terkurasi, menyetel
kata kunci.

**Wajib izin Prinsipal:** mengubah mesin atau workflow, menghidupkan/mematikan
otomasi, apa pun yang menyangkut biaya, dan apa pun yang menyentuh kredensial.

**Tidak pernah:** memasang token/API key ke perintah atau berkas — itu selalu
dikerjakan Prinsipal sendiri, walau tokennya diberikan langsung.
