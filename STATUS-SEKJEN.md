# STATUS-SEKJEN.md — ringkasan pagi (dirawat Admin HIFDI; update tiap selesai kerjaan penting)

**Update terakhir:** 5 Agu 2026, 02:05 WIB

## Keputusan Sekjen (5 Agu 2026)
- **13 feed Google News:** DISETUJUI ditambah bertahap sambil dipantau — tapi **EKSEKUSI DITUNDA** sampai aba-aba tahap berikutnya dari Sekjen. Jangan dieksekusi dulu.
- **CNN Gaya Hidup & Health Affairs:** TIDAK dihapus — biarkan di `config.py` (cuma keblokir IP GitHub, bukan mati; terverifikasi hidup dari jaringan rumah, 5 Agu).
- **INFRASTRUKTUR: TIDAK pakai VPS.** Laptop rumah nyala 24/7 hanya untuk host Hermes. Bot HIFDI (dan nanti FMI/Ummanitarian) TETAP di GitHub Actions — laptop bukan host bot.
- **SISTEM FOTO GILIR (restu Prinsipal/Sekjen):** bot harian BOLEH memakai koleksi foto. Pemetaan kategori editorial → kategori foto (`PHOTO_BY_CATEGORY`) sudah di `config.py`. **Syarat 1 TERPENUHI** (audit lisensi → 3 foto dikeluarkan). **Syarat 2 TERPENUHI** (audit netralitas 54 foto → 12 foto memuat orang bisa dikenali/konten sensitif dikeluarkan). **Aktif: 42 foto generik & netral**; dokumentasi lengkap `docs/HAK-PAKAI-FOTO.md`. Integrasi `generate_article.py` belum dikerjakan (tunggu arahan).

## Status proyek
- **Berita HIFDI (piloting):** mesin sehat. Bot harian terbit article-065 (4 Agu, run sukses).
- **stok/:** kosong — bot 5 Agu pagi pakai jalur RSS normal.
- **FMI:** scoping selesai (5 Agu) → `RENCANA-FMI-UMMANITARIAN.md`. Situs + deploy CF otomatis sudah jalan; kurang = bot produsen (tahap 1).
- **Ummanitarian:** scoping selesai (5 Agu) → `RENCANA-FMI-UMMANITARIAN.md`. Paling dasar: deploy otomatis belum ada (tahap 1).

## Butuh keputusan Sekjen
1. **Review RENCANA-FMI-UMMANITARIAN.md** — 9 keputusan K1–K9; urgent: K1–K3 (FMI tahap 1) & K8–K9 (Ummanitarian tahap 1).
