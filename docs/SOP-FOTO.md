# SOP — Pencarian & Pengelolaan Foto (Koleksi HIFDI)

**Tujuan:** Menyediakan stok foto yang cocok, legal, dan terdistribusi merata untuk
artikel situs HIFDI, tanpa pengulangan gambar yang berlebihan.

---

## 1. Penentuan Kebutuhan
1. Tentukan topik artikel → pilih kategori dari **16 kategori** (lihat README.md).
2. Kalau topik tidak jelas kategorinya → tanyakan/tentukan dengan editor (Sekjen).
3. Tidak ada kategori yang pas → bicarakan dulu, jangan memaksakan.

## 2. Sumber Gambar (urutan prioritas)
1. **Koleksi sendiri** di `images/foto/cat-XX/` (foto kiriman user + hasil koleksi) — dipakai
   lewat sistem gilir, **paling diutamakan**.
2. **Openverse** (api.openverse.org) — agregator jutaan foto CC dari Flickr, Wikimedia,
   dll. Tanpa kunci API. **Wajib filter `license_type=commercial`** (lisensi boleh
   dipakai komersial: CC0, PDM, CC-BY, CC-BY-SA; hindari BY-NC).
3. **Wikimedia Commons** — cadangan, unduh pelan-pelan (jeda ≥1,5 dtk) karena aturan
   robot ketat (429).
4. Hindari: situs berita lain (hotlink), Google Images (kepemilikan tidak jelas).

## 3. Unduh & Simpan
1. Nama file: `cat-XX-###.jpg` (urutan angka, unik per kategori).
2. Simpan ke `images/<kode-kategori>/`.
3. Catat ke `scripts/photo_registry.json`:
   - `file`, `source` (URL asli), `license` (lisensi), `used` (berapa kali dipakai),
     `last_article` (artikel terakhir yang memakai).
4. Buang file yang < 10 KB (kemungkinan rusak/placeholder).

## 4. QC (Quality Control) — WAJIB
1. **Cek otomatis:** foto diperiksa dengan AI vision (mata Qwen) — cocok tidak dengan
   kategorinya.
2. **Cek manusia:** lembar periksa (contact sheet) dikirim ke user — user memberi
   keputusan akhir "cocok / ganti".
3. Foto yang tidak cocok → dihapus/diganti. **JANGAN dipakai sebelum lolos QC.**

## 5. Pemakaian (Sistem Gilir)
1. Artikel butuh foto kategori X → jalankan: `python3 pick_photo.py cat-XX`
2. Skrip memilih foto dengan **pemakaian paling sedikit** → otomatis merata.
3. Pengulangan baru terjadi setelah semua foto kategori itu terpakai.
4. Registry selalu diperbarui tiap pemilihan.

## 6. Larangan
- ❌ Memakai foto tanpa lisensi yang jelas (termasuk hotlink situs berita).
- ❌ Memakai foto kategori A untuk artikel kategori B (mismatch).
- ❌ Foto yang belum lolos QC.
- ❌ Mengunggah foto pribadi/orang lain tanpa izin.

## 7. Catatan Kepatuhan
- Semua foto wajib punya jejak: sumber URL + lisensi di registry (audit mudah).
- Bila ragu lisensi → jangan dipakai, cari lain.
