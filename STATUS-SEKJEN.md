# STATUS-SEKJEN.md — ringkasan pagi (dirawat Admin HIFDI; update tiap selesai kerjaan penting)

**Update terakhir:** 6 Agu 2026, 00:20 WIB

## Kerjaan selesai (6 Agu 2026 dini hari, Admin HIFDI)
- **FIX BUG FOTO article-069:** bot harian memilih `cat-12-001` (status **excluded**, file sudah dibuang 5 Agu → dipindah `_ditolak/`) → gambar ilustrasi 404. Root cause: `photo_pool.py` mengisi kandidat dari registry tanpa filter status excluded/keberadaan file. **Sudah dipatch** (`photo_pool.py` kini filter `status=excluded` + hanya file yang ada di disk) + `article-069/index.html` diganti ke `cat-12-002` (featured + og:image) + registry di-update. **LIVE & terverifikasi** (gambar HTTP 200, deploy sukses). Ini mencegah terulang.
- **Caption WAG OTOMATIS (acc Prinsipal):** cron Hermes `*/15` pantau artikel baru di repo → kirim caption hangat ke WAG HIFDI Bangkit via OpenWA (state `~/.hermes/scripts/wa_state.json`, mulai 069). Bot GH Actions tidak bisa kirim WA (OpenWA lokal), jadi dipegang Hermes. Artikel bot maupun manual tertangkap. **Papan pesan SEKJEN §5 di-update.**
- **Caption article-069** terkirim ke WAG HIFDI Bangkit (6 Agu, via OpenWA, messageId ACK) — sebelumnya hanya ke Telegram @hifdi_bot, tidak ke WAG (inkonsistensi dilaporkan Prinsipal).

## Keputusan Sekjen (5 Agu 2026)
- **13 feed Google News:** DISETUJUI ditambah bertahap sambil dipantau — tapi **EKSEKUSI DITUNDA** sampai aba-aba tahap berikutnya dari Sekjen. Jangan dieksekusi dulu.
- **CNN Gaya Hidup & Health Affairs:** TIDAK dihapus — biarkan di `config.py` (cuma keblokir IP GitHub, bukan mati; terverifikasi hidup dari jaringan rumah, 5 Agu).
- **INFRASTRUKTUR: TIDAK pakai VPS.** Laptop rumah nyala 24/7 hanya untuk host Hermes. Bot HIFDI (dan nanti FMI/Ummanitarian) TETAP di GitHub Actions — laptop bukan host bot.
- **SISTEM FOTO GILIR (restu Prinsipal/Sekjen):** bot harian BOLEH memakai koleksi foto. Pemetaan kategori editorial → kategori foto (`PHOTO_BY_CATEGORY`) sudah di `config.py`. **Syarat 1 & 2 TERPENUHI.** Koreksi aturan privasi Prinsipal: **wajah tanpa nama = BOLEH** — 5 foto dikembalikan (cat-04-001/002/004, cat-05-002/004); yang tetap keluar 7 (data pribadi terbaca, anak-anak, pasien terekspos) + 3 lisensi = 10. **Aktif: 47 foto**; dokumentasi `docs/HAK-PAKAI-FOTO.md`. **REVISI (syarat keras): sistem tidak pernah memasangkan foto berwajah + nama; caption "Ilustrasi" generik memenuhi** — wajib diterapkan saat integrasi `generate_article.py`. **REVISI (lisensi): foto lama dianggap aman Prinsipal; dokumentasi hak-pakai fokus penambahan foto baru** (wajib source+license+QC per SOP-FOTO). **HIMBAUAN: perluas sumber gambar eksternal; utamakan foto tanpa wajah (alkes/fasilitas/objek)**. Integrasi belum dikerjakan (tunggu arahan).

## Status proyek
- **Berita HIFDI (piloting):** mesin sehat. Bot harian terbit article-066 (5 Agu, run sukses). **article-067 terbit manual oleh Admin HIFDI (5 Agu, Mutu, AI Skrining TB) — LIVE & terverifikasi** (gambar sistem gilir cat-01-001, caption "Ilustrasi").
- **stok/:** kosong — bot pagi pakai jalur RSS normal.
- **FMI:** scoping selesai (5 Agu) → `RENCANA-FMI-UMMANITARIAN.md`. Situs + deploy CF otomatis sudah jalan; kurang = bot produsen (tahap 1).
- **Ummanitarian:** scoping selesai (5 Agu) → `RENCANA-FMI-UMMANITARIAN.md`. Paling dasar: deploy otomatis belum ada (tahap 1).

## Butuh keputusan Sekjen
1. **Review RENCANA-FMI-UMMANITARIAN.md** — 9 keputusan K1–K9; urgent: K1–K3 (FMI tahap 1) & K8–K9 (Ummanitarian tahap 1).
