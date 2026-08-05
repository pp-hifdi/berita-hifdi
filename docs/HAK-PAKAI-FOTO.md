# HAK-PAKAI FOTO — Koleksi HIFDI (dokumentasi lisensi & sumber)

> Audit hak-pakai 57 foto koleksi portal. **Tanggal: 5 Agu 2026, oleh Admin HIFDI** atas syarat restu Prinsipal/Sekjen: *pastikan & dokumentasikan hak-pakai karena foto dipublikasikan; yang sumber/lisensinya tidak jelas dikeluarkan.*
> Sumber data per-file: `scripts/photo_registry.json` (field `file`, `source`, `license`, `status`).

## Ringkasan

| Status | Jumlah | Keterangan |
|---|---|---|
| ✅ Aktif (boleh dipakai) | **42** | Generik & netral: lisensi jelas, tanpa orang bisa dikenali / konten sensitif |
| ⛔ Dikeluarkan — lisensi (syarat #1) | 3 | Detail di bawah |
| ⛔ Dikeluarkan — netralitas (syarat #2) | 12 | Detail di bawah |
| Total | 57 | |

## Rincian lisensi — 42 foto aktif

| Lisensi | Jumlah | Arti hak-pakai | Atribusi |
|---|---|---|---|
| **CC BY** | 28 | Boleh dipakai komersial & dimodifikasi (crop/og-image) | WAJIB atribusi penulis + link lisensi |
| **CC BY-SA** | 11 | Sama seperti CC BY, plus turunan harus lisensi sama (share-alike) | WAJIB atribusi |
| **PDM** (Public Domain) | 3 | Bebas dipakai, tanpa atribusi | Tidak wajib |

Semua foto aktif berasal dari sumber yang jelas: **42 Flickr** (URL asli tercatat di registry).

## Foto yang DIKELUARKAN — syarat #2: netralitas (12)

Audit visual AI (mata Qwen, 5 Agu 2026) per foto aktif: memuat **orang yang bisa dikenali / konten sensitif** (anak-anak, pasien + data pribadi, situasi darurat) — dikeluarkan dari rotasi supaya tidak nyasar ke berita duka/sensitif:

`cat-01-002` (pasien wajah jelas) · `cat-03-002` (anak di konteks klinis) · `cat-04-001/002/004` (potret wajah jelas) · `cat-05-001/002/004` (lansia & anak, wajah jelas) · `cat-06-001` (pasien + terapi ECT) · `cat-11-004` (pasien + nomor kamar terbaca) · `cat-12-001` (nama pasien & data medis terbaca) · `cat-14-001` (bayi + evakuasi darurat).

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
