# stok/ — Amunisi Tulisan Jadi (wilayah Sekjen)

Folder ini adalah **kotak amunisi** — tempat Sekjen menaruh **artikel jadi,
siap terbit** yang ditulis saat laptop terbuka (di luar RSS). Disepakati
3 Agustus 2026 (lihat papan pesan §5).

## Aturan pakai (untuk Sekjen)

1. **Satu draf = satu subfolder** berisi `index.html`:
   ```
   stok/<nama-bebas>/index.html
   ```
   Nama folder bebas (mis. `stok/ai-telemedicine-1/`). Yang dibaca bot hanya
   folder yang punya `index.html`.

2. **Format `index.html` = sama persis dengan artikel jadi** (`article-XXX/
   index.html`): satu file HTML lengkap dengan `<!DOCTYPE html>`, `<head>`
   (meta description, og:title, og:description, og:image), `<h1 class=
   "article-title">`, `<div class="article-subtitle">`, `<span class=
   "article-category">`, body artikel, dan **kotak Referensi** (`.sources-box`)
   berisi **URL sumber nyata**.

3. **URL sumber WAJIB nyata** (aturan mutu §3): kotak Referensi memuat
   `<a href="https://...">`. URL itu otomatis dicatat ke `used_sources.json`
   begitu draf terbit — sekali terbit, tidak boleh terbit lagi.

4. **Gambar**: kalau `og:image` memakai Unsplash (`images.unsplash.com/
   photo-...`), ID-nya dipakai untuk kartu portal. Kalau tidak ada, bot memakai
   gambar default sesuai kategori. Sebaiknya sertakan `og:image` dari daftar
   putih `config.py`.

5. **Prioritas terbit** (keputusan Prinsipal): tiap pagi 06.00 WIB, bot
   memeriksa folder ini DULU. **Ada draf → terbitkan yang paling awal
   (urut nama folder), RSS tidak disentuh.** **Kosong → RSS seperti biasa.**

6. Draf yang sudah terbit **dipindahkan otomatis** ke `article-XXX/` —
   Sekjen tidak perlu menghapusnya sendiri.

## Contoh struktur

```
stok/
└── telehealth-fkpt-1/
    └── index.html     # artikel lengkap siap terbit
```
