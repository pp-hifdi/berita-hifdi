# DESAIN-KANTOR-BERITA-HIFDI.md — Arsitektur Sistem Kantor Berita HIFDI

> Dokumen desain sistem kantor berita otomatis Berita HIFDI (berita.hifdi.id),
> ditulis 3 lapis agar dipahami **awam**, dikerjakan **IT**, dan dibaca **AI**.
> Berlaku per 11 Agustus 2026 (termasuk alur ACC baru).

---

## 1. GAMBARAN (untuk awam)

Kantor berita HIFDI = **toko roti otomatis** yang buka tiap pagi:

| Bagian | Analogi | Komponen nyata |
|---|---|---|
| Bahan baku | Berita mentah dari agen berita | RSS feed (feedparser) |
| Koki | AI yang menulis artikel | DeepSeek API |
| Mesin oven | Penjadwal otomatis | GitHub Actions (cron 06:00 WIB) |
| Rak penyimpanan | Artikel jadi tapi belum tayang | Branch `draft` di GitHub |
| Karyawan kasir | Pemberi izin tayang | Gate ACC (via chat Hermes) |
| Etalase | Website publik | berita.hifdi.id (Cloudflare Pages) |
| Kurir | Penyebar ke pembaca | WhatsApp group (OpenWA) |

Cara kerjanya: tiap pagi mesin mengolah berita mentah menjadi artikel jadi,
menaruhnya di rak (draft), minta izin ke pemilik toko (ACC), lalu memajangnya
di etalase (tayang) dan mengirimkannya ke pelanggan (WA).

---

## 2. DIAGRAM ARSITEKTUR

```
                        ┌──────────────────────────────────────────┐
   SUMBER BERITA        │              GITHUB ACTIONS              │
   RSS feeds ──────────►│  06:00 WIB  daily-generate.yml           │
                        │  generate_article.py (DeepSeek + RSS)    │
                        │  ─► tulis artikel HTML (pedoman SEKJEN)  │
                        │  ─► pilih foto (photo_pool/whitelist)    │
                        │  ─► update kartu + registry anti-duplikat│
                        │  ─► push ke branch ┌──────────┐          │
                        │                    │  DRAFT   │          │
                        │                    └──────────┘          │
                        └───────────────────────────┬──────────────┘
                                                    │
                       ┌────────────────────────────▼──────────────┐
                       │  GATE ACC — HERMES (chat Prinsipal)       │
                       │  06:20 WIB: kirim judul + NARASI + FOTO   │
                       │  ─► balas ACC = tayang / TOLAK = buang    │
                       │  ─► 06:50 tanpa balasan = AUTO-TAYANG     │
                       └───────────────┬───────────────┬───────────┘
                                       │ ACC/auto     │ TOLAK
                                       ▼              ▼
                        ┌────────────────────┐   buang draft
                        │  push ke main      │
                        └─────────┬──────────┘
                                  ▼
                  ┌─────────────────────────────────┐
                  │  CLOUDFLARE PAGES (berita.hifdi.id)│
                  │  auto-build dari branch main      │
                  └──────────────┬──────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │  DISTRIBUSI: WA group    │
                    │  Bangkit (OpenWA caption)│
                    └──────────────────────────┘
```

---

## 3. KOMPONEN & PERAN

| Komponen | Teknologi | Fungsi |
|---|---|---|
| Repo | GitHub `pp-hifdi/berita-hifdi` | Satu-satunya sumber kebenaran (kode + konten) |
| Generator | `scripts/generate_article.py` | Tarik RSS → DeepSeek tulis artikel → rakit HTML |
| Penjadwal | `.github/workflows/daily-generate.yml` (cron `0 23 * * *` UTC = 06:00 WIB) | Jalankan generator tiap pagi |
| Gate ACC | Hermes cron (06:20 WIB) + auto-tayang (06:50 WIB) | Izin tayang dengan tenggat |
| Portal | Cloudflare Pages (auto dari `main`, folder root, `404.html` ada) | Publikasi situs |
| Gambar | `images/foto/cat-01..20` (102 aktif) + whitelist Unsplash/Stocksnap | Ilustrasi artikel, rotasi merata, alt jujur, og:image 1200×630 |
| Anti-duplikat | `scripts/used_sources.json` (ter-commit) | Sumber berita tidak dipakai dua kali |
| Distribusi | OpenWA API (Docker, port 2785) → WA group Bangkit | Caption artikel otomatis ke WA |
| Koordinasi | `SEKJEN.md`, `AGENTS.md`, `STATUS-SEKJEN.md` | Aturan kerja antar-agen (manusia/AI) |

**Peran (multi-agent):**
- **Prinsipal** (pemilik) — keputusan akhir, biaya, kredensial.
- **Sekjen** — mutu editorial, pedoman, artikel manual, pengawasan.
- **Hermes (Staf Mesin)** — infrastruktur, otomasi, workflow, recovery.
- **Pekerja (bot DeepSeek)** — artikel rutin dari RSS tiap pagi.

---

## 4. ALUR RILIS HARIAN (desain baru per 11 Agu 2026)

```
06:00  GitHub Actions generate artikel → push branch draft
06:20  Hermes cek draft → kirim ke chat Prinsipal:
       judul + narasi LENGKAP + link foto yang akan ditayangkan
       ── Prinsipal balas dalam 30 menit ──
          ACC   → rebase draft ke main → push → tayang → link dikirim
          TOLAK → branch draft dihapus
       ── tidak ada balasan sampai 06:50 ──
          AUTO-TAYANG (fail-open dengan tenggat)
```

Prinsip desain gate: **kontrol manusia + otonomi mesin**. Manusia memegang
keputusan; mesin tidak pernah macet menunggu selamanya.

---

## 5. STRUKTUR REPO & FILE KUNCI

```
berita-hifdi/
├── index.html                  # portal: grid kartu artikel + articleCount
├── 404.html                    # fallback Cloudflare Pages
├── article-XXX/index.html      # 1 folder = 1 artikel (statis penuh)
├── images/
│   ├── foto/cat-01..20/        # kolam foto lokal (102 aktif, _ditolak = QC gagal)
│   └── article-*-og.jpg        # og:image artikel
├── scripts/
│   ├── generate_article.py     # generator harian (DeepSeek + RSS)
│   ├── config.py               # kata kunci, bobot, daftar gambar (wilayah Sekjen)
│   ├── photo_pool.py           # rotasi foto merata
│   ├── used_sources.json       # penjaga duplikat sumber
│   ├── photo_registry.json     # status foto (aktif/excluded)
│   └── telegram_state.json     # offset pesan (alur ACC lama, kini nonaktif)
├── .github/workflows/
│   ├── daily-generate.yml      # AKTIF — generate pagi
│   └── publish-on-acc.yml      # DI-PAUSE — alur ACC pindah ke Hermes
├── SEKJEN.md                   # aturan editorial + papan pesan antar-agen
├── AGENTS.md                   # konteks operasional untuk AI
├── STATUS-SEKJEN.md            # ringkasan status harian
└── PEMBELAJARAN-INFRA.md       # pelajaran insiden (11 Agu 2026)
```

**Aturan penting:** commit spesifik (bukan `git add -A`), nomor artikel = tertinggi
di main + 1, kartu baru di paling atas grid, `articleCount` naik manual, sumber
nyata di kotak referensi, tidak ada force-push.

---

## 6. SISTEM GAMBAR (keadaan aktual per 10 Agu 2026)

- Kolam lokal: `images/foto/cat-01..20` = **102 jpg aktif** (20 ditolak QC di `_ditolak/`).
- Pemetaan kategori → kolam: `IMAGE_POOLS` di config.py
  (Advokasi: cat-10/12/13; Mutu: cat-12/02/09; Edukasi: cat-03/04/08/07; Kabar: cat-13/01/05).
- Rotasi: `photo_pool.py` — pilih foto paling jarang dipakai, skip excluded.
- Cadangan: whitelist `IMAGES` (Unsplash 4 + Stocksnap 6, CC0), dipilih `random.choice`.
- Aturan keras: **alt jujur** (AI tak bisa melihat gambar), og:image 1200×630,
  verifikasi visual sebelum masuk daftar putih.

---

## 7. DISTRIBUSI (WhatsApp)

- Artikel baru → caption otomatis ke **WA group Bangkit** via OpenWA API
  (`http://localhost:2785`, session `berita-wa`, state `wa_state.json`, cek tiap 15 menit).
- OpenWA = Docker container `openwa-api` di Docker Desktop Windows.
- Urutan pesan: LINK dulu (biar preview OG muncul), lalu CAPTION (jeda 3 detik).
- Pipeline dicek tiap pagi (`cek_pipeline_pagi.sh` 05:55) — semua hijau sebelum publish.

---

## 8. KOORDINASI MULTI-AGENT

- `SEKJEN.md` §2: tabel wilayah berkas (siapa boleh edit apa) — cegah tabrakan.
- `SEKJEN.md` §5: papan pesan antar-agen (tulis tanggal + pengirim, hapus yang selesai).
- `STATUS-SEKJEN.md`: ringkasan pagi ≤15 baris, dirawat Hermes, dibaca Sekjen.
- Prinsip: **baca dokumen dulu sebelum sentuh repo**; perubahan struktural
  diumumkan dulu di papan pesan.

---

## 9. LAPISAN AI (aturan ringkas untuk agent sesi baru)

1. Baca `SEKJEN.md` → `AGENTS.md` sebelum menyentuh repo.
2. `git fetch` dulu; bandingkan `origin/draft` vs `origin/main` sebelum generate.
3. Nomor artikel dari main terbaru (tertinggi + 1), bukan dari draft.
4. Commit spesifik, jangan `git add -A`; tidak pernah force-push.
5. Verifikasi setelah push: `git rev-parse HEAD origin/main` harus sama.
6. Kredensial tidak pernah di repo; token 401 → laporkan, jangan retry buta.
7. Gate yang menunggu manusia WAJIB punya tenggat (30 menit → auto).
8. Jalur non-kritis (notifikasi) toleran error; jalur kritis (publish) tegas.
9. Kegagalan workflow → alert ke pemilik, jangan diam.

---

## 10. BLUEPRINT REPLIKASI (ke proyek portal lain)

Untuk membangun kantor berita serupa dari nol:
1. Repo statis + Cloudflare Pages (auto-build dari `main`).
2. Generator harian: RSS → LLM (DeepSeek) → artikel HTML + kartu + registry anti-duplikat.
3. Branch `draft` sebagai staging + gate ACC dengan tenggat (30 menit auto-tayang).
4. Kolam foto lokal + whitelist gambar, alt jujur, og:image sesuai rasio.
5. Distribusi: caption ke WA group (OpenWA) + link preview.
6. Dokumentasi: `AGENTS.md` + `SEKJEN.md` (peran, wilayah, papan pesan) + `STATUS-*.md`.
7. Checklist reuse lengkap ada di `PEMBELAJARAN-INFRA.md`.
