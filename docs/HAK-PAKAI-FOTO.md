# HAK-PAKAI FOTO — Koleksi HIFDI (dokumentasi lisensi & sumber)

> Audit hak-pakai 57 foto koleksi portal. **Tanggal: 5 Agu 2026, oleh Admin HIFDI** atas syarat restu Prinsipal/Sekjen: *pastikan & dokumentasikan hak-pakai karena foto dipublikasikan; yang sumber/lisensinya tidak jelas dikeluarkan.*
> Sumber data per-file: `scripts/photo_registry.json` (field `file`, `source`, `license`, `status`).

## Ringkasan

| Status | Jumlah | Keterangan |
|---|---|---|
| ✅ Aktif (boleh dipakai) | **47** | Lisensi jelas; tanpa data pribadi terbaca / anak-anak / pasien terekspos |
| ⛔ Dikeluarkan — lisensi (syarat #1) | 3 | Detail di bawah |
| ⛔ Dikeluarkan — netralitas (syarat #2) | 7 | Detail di bawah |
| Total | 57 | |

> **Aturan privasi (keputusan Prinsipal, 5 Agu 2026) — satu garis:** JANGAN
> sandingkan wajah yang bisa dikenali DENGAN nama individu. **Foto tanpa nama =
> boleh. Nama tanpa foto = boleh.** Foto berwajah TIDAK dibuang hanya karena ada
> wajah — yang dilarang menempelkan nama orang pada wajahnya (di caption/artikel).
>
> **Revisi (5 Agu 2026) — SYARAT KERAS sistem:** sistem TIDAK PERNAH boleh
> memasangkan foto berwajah + nama individu. **Caption "Ilustrasi" generik
> sudah memenuhi syarat ini** — karena itu setiap foto di artikel memakai
> keterangan "Ilustrasi" (tanpa nama, tanpa narasi menebak isi foto). Alt text
> juga generik; tidak pernah memuat nama orang.
>
> **Revisi (5 Agu 2026) — lisensi:** foto lama yang sudah ada di koleksi
> **dianggap aman oleh Prinsipal** (tidak perlu diaudit ulang). Dokumentasi
> hak-pakai **difokuskan untuk penambahan foto baru**: setiap foto baru WAJIB
> tercatat `source` + `license` di `photo_registry.json` dan lolos QC (SOP-FOTO
> §2–4) sebelum masuk koleksi — tanpa itu, foto tidak boleh dipakai.
>
> **Himbauan (5 Agu 2026, Prinsipal) — arah penambahan ke depan** (anjuran,
> bukan pemblokir): perluas sumber dokumentasi/gambar eksternal lebih luas, dan
> sebisa mungkin pilih gambar **tanpa wajah individu** — utamakan **alkes
> (alat kesehatan), fasilitas/faskes, objek/ilustrasi**.

## Rincian lisensi — 47 foto aktif

| Lisensi | Jumlah | Arti hak-pakai | Atribusi |
|---|---|---|---|
| **CC BY** | 30 | Boleh dipakai komersial & dimodifikasi (crop/og-image) | WAJIB atribusi penulis + link lisensi |
| **CC BY-SA** | 14 | Sama seperti CC BY, plus turunan harus lisensi sama (share-alike) | WAJIB atribusi |
| **PDM** (Public Domain) | 3 | Bebas dipakai, tanpa atribusi | Tidak wajib |

Semua foto aktif berasal dari sumber yang jelas: **47 Flickr** (URL asli tercatat di registry).

## Foto yang DIKELUARKAN — syarat #2: netralitas (7, setelah koreksi aturan privasi)

Audit visual AI (mata Qwen, 5 Agu 2026) per foto aktif. Koreksi Prinsipal: **foto berwajah BOLEH selama tidak disandingkan nama** — 5 foto yang sempat dikeluarkan hanya karena wajah (cat-04-001/002/004, cat-05-002/004) **dikembalikan**. Yang TETAP keluar karena kontennya sendiri sensitif (bukan sekadar wajah):

| File | Alasan tetap keluar |
|---|---|
| `cat-01-002` | Pasien dengan kondisi tubuh terekspos (sensitivitas medis) |
| `cat-03-002` | Anak-anak di konteks klinis |
| `cat-05-001` | Memuat anak-anak |
| `cat-06-001` | Pasien dalam perawatan/terapi invasif |
| `cat-11-004` | Data pasien terbaca (nomor kamar/identitas) |
| `cat-12-001` | Nama pasien & data medis terbaca di foto |
| `cat-14-001` | Bayi dalam situasi darurat |

**Praktik saat memakai foto berwajah:** caption & isi artikel TIDAK boleh menyebut nama orang yang wajahnya tampak; bila artikel menyebut nama individu, pilih foto tanpa wajah orang itu.

## Foto yang DIKELUARKAN — syarat #1: lisensi (3)

| File | Lisensi | Alasan |
|---|---|---|
| `cat-07-001.jpg` (+`-og.jpg`) | by-nd (CC BY-ND) | NoDerivatives — TIDAK mengizinkan modifikasi; portal wajib membuat varian og-image 1200×630 (modifikasi) |
| `cat-08-001.jpg` (+`-og.jpg`) | by-nd (CC BY-ND) | Sama |
| `cat-15-001.jpg` (+`-og.jpg`) | tidak tercatat | Lisensi kosong di registry → tidak jelas → dikeluarkan (aturan: ragu → jangan dipakai) |

File dikeluarkan dipindah ke `images/foto/_ditolak/` dan ditandai `"status": "excluded"` di registry (jejak audit utuh, reversibel). Folder `_ditolak/` tidak di-scan sistem gilir `pick_photo.py`.

## Kewajiban saat foto dipakai di artikel

1. **CC BY / CC BY-SA** → cantumkan atribusi di halaman artikel: nama/kredit penulis + sumber URL (dari registry) + lisensi, mis. `Foto: <penulis>, via Flickr (URL), CC BY 2.0`. Atribusi minimal yang dapat diterima: tautan URL sumber + label lisensi.
2. **PDM** → bebas; tetap cantumkan sumber URL untuk jejak audit.
3. **Caption tampilan** → tulis **"Ilustrasi"** saja (SOP-FOTO §5b), jangan narasi menebak isi foto.
4. Jangan pernah memakai foto dari `_ditolak/`.

## Catatan lain

- `cat-04` (potret individu wajah jelas) **tidak dipetakan** di `PHOTO_BY_CATEGORY` — keputusan sementara menunggu persetujuan Prinsipal (risiko sensitivitas identitas), bukan masalah lisensi.
- Registri `photo_registry.json` diperbarui otomatis oleh `pick_photo.py` (field `used`, `last_article`) — dokumentasi ini hanya memakai data yang sama.
