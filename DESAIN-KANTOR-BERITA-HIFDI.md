# DESAIN-KANTOR-BERITA-HIFDI.md — Instansi (Contoh Terpasang)

> Dokumen ini adalah INSTANSI dari blueprint generik
> **`DESAIN-KANTOR-BERITA-GENERIK.md`** (baca itu dulu untuk desain utuh).
> Hanya berisi isian konkret portal HIFDI. Berlaku per 11 Agu 2026.

---

## KONFIGURASI PROYEK

| Parameter | Nilai |
|---|---|
| Nama portal | Berita HIFDI |
| Domain | berita.hifdi.id |
| Repo | `pp-hifdi/berita-hifdi` (branch `main`) |
| Sumber berita | RSS feeds (feedparser) |
| Model AI penulis | DeepSeek (`deepseek-chat`) |
| Jadwal generate | 06:00 WIB (cron `0 23 * * *` UTC) |
| Channel ACC | Chat Hermes (Prinsipal) — 06:20 WIB |
| Tenggat auto-tayang | 06:50 WIB (30 menit tanpa ACC) |
| Channel distribusi | WA group Bangkit (OpenWA, port 2785) |
| Hosting | Cloudflare Pages (auto dari `main`, `404.html` ada) |

## PERAN (3)

- **Prinsipal** (manusia) — ACC/TOLAK, kredensial, biaya.
- **Bot Penulis** — DeepSeek di GitHub Actions (`daily-generate.yml`).
- **Operator Otomasi** — Hermes: jadwal ACC, verifikasi, recovery, alert.

## FILE KUNCI REPO

- `scripts/generate_article.py` — generator harian
- `scripts/config.py` — kata kunci, bobot, daftar gambar (wilayah editorial)
- `scripts/photo_pool.py`, `used_sources.json`, `photo_registry.json`
- `.github/workflows/daily-generate.yml` (AKTIF), `publish-on-acc.yml` (PAUSED)
- `SEKJEN.md` → kini berfungsi sebagai **PEDOMAN.md** (dokumen editorial, bukan peran)
- `AGENTS.md`, `STATUS-SEKJEN.md` → ringkasan harian
- `PEMBELAJARAN-INFRA.md`, `DESAIN-KANTOR-BERITA-GENERIK.md`

## SPESIFIK YANG BERBEDA DARI GENERIK

- Kolam foto lokal: `images/foto/cat-01..20` (102 jpg aktif) + whitelist Unsplash/Stocksnap.
- Gate ACC dijalankan Hermes via 2 jadwal: lapor draft 06:20, auto-tayang 06:50.
- Distribusi WA via Docker `openwa-api` (localhost:2785), session `berita-wa`.
- Nomor artikel 3 digit (article-XXX), `articleCount` di `index.html` naik manual.
