# DESAIN-KANTOR-BERITA-GENERIK.md — Blueprint Kantor Berita Otomatis

> Template desain sistem kantor berita statis yang bisa dipakai untuk SEMUA
> proyek portal berita serupa (kampus, organisasi, komunitas). Salin file ini
> ke repo proyek baru, isi bagian "KONFIGURASI PROYEK".
> Ditulis 3 lapis: **awam** (analogi), **IT** (teknis), **AI** (aturan agent).
> Desain ini TANPA peran editor khusus (efisiensi token & workflow, 11 Agu 2026).

---

## 1. KONFIGURASI PROYEK (isi per proyek)

| Parameter | Nilai |
|---|---|
| Nama portal | `...` |
| Domain | `...` |
| Repo | `...` |
| Sumber berita (RSS) | `...` |
| Model AI penulis | `...` |
| Jadwal generate | `...` |
| Channel ACC (chat pemilik) | `...` |
| Channel distribusi (WA/Telegram) | `...` |
| Hosting | `...` |

---

## 2. GAMBARAN (awam)

Kantor berita otomatis = **toko roti otomatis**:

| Bagian | Analogi | Komponen nyata |
|---|---|---|
| Bahan baku | Berita mentah | RSS feed |
| Koki | AI penulis artikel | LLM (mis. DeepSeek) |
| Mesin oven | Penjadwal | GitHub Actions / cron |
| Rak | Artikel jadi, belum tayang | Branch `draft` |
| Kasir | Pemberi izin tayang | Gate ACC (chat pemilik) |
| Etalase | Website | Hosting statis (CF Pages/Netlify/WebDAV) |
| Kurir | Penyebar ke pembaca | WA group / Telegram channel |

Tiap jadwal: mesin mengolah berita → artikel jadi di rak (draft) → minta izin
ke pemilik (ACC) → pajang di etalase (tayang) → kirim ke pelanggan.

---

## 3. PERAN (hanya 3 — tanpa editor khusus)

| Peran | Pemegang | Tugas |
|---|---|---|
| **Pemilik** | Manusia | Keputusan akhir (ACC/TOLAK), kredensial, biaya |
| **Bot Penulis** | LLM di scheduler | Menulis artikel dari sumber, merakit HTML, push draft |
| **Operator Otomasi** | Agent infrastruktur (Hermes/sejenisnya) | Jadwal, gate ACC, verifikasi, recovery, alert |

Prinsip: **mesin menulis, mesin mengelola, manusia memutuskan.** Tidak ada
peran editor perantara → hemat token, hemat koordinasi.

---

## 4. DIAGRAM ARSITEKTUR

```
   RSS feeds ──► SCHEDULER (cron) ──► BOT PENULIS (LLM)
                     │                    │ tulis artikel + pilih foto
                     │                    ▼
                     │              branch DRAFT
                     │                    │
                     ▼                    ▼
              GATE ACC (chat pemilik)
               - kirim judul + narasi + link foto
               - ACC = tayang / TOLAK = buang
               - tenggat (mis. 30 menit) → AUTO-TAYANG
                     │
                     ▼
              push MAIN ──► HOSTING STATIS (auto-deploy)
                     │
                     ▼
              DISTRIBUSI (WA group / Telegram)
```

---

## 5. ALUR RILIS HARIAN (generik)

```
JAM X       Scheduler jalankan Bot Penulis → push branch draft
JAM X+20    Operator kirim ke chat Pemilik:
            judul + narasi LENGKAP + link foto yang akan ditayangkan
            ── balasan Pemilik ──
               ACC   → rebase draft ke main → push → tayang → kirim link
               TOLAK → buang branch draft
            ── tidak dibalas sampai tenggat (mis. 30 menit) ──
               AUTO-TAYANG (fail-open dengan tenggat)
```

Desain gate: **kontrol manusia + otonomi mesin** — manusia memegang keputusan,
produksi tidak pernah macet menunggu selamanya.

---

## 6. KOMPONEN & ATURAN (IT)

| Komponen | Ketentuan |
|---|---|
| Repo | Statis murni (HTML/CSS), satu-satunya sumber kebenaran |
| Scheduler | Cron di GitHub Actions (UTC), jadwal pagi |
| Bot penulis | LLM + feedparser; pedoman editorial di file `PEDOMAN.md` (bukan peran, hanya dokumen) |
| Anti-duplikat | Registry sumber ter-commit (`used_sources.json`) — satu sumber tidak dipakai 2× |
| Gambar | Kolam foto lokal + whitelist stok; rotasi merata; alt JUJUR; og:image rasio standar (1200×630) |
| Penomoran artikel | Tertinggi di `main` + 1 (hitung dari main, bukan draft) |
| Commit | Spesifik (jangan `git add -A`); tidak pernah force-push |
| Gate | Chat pemilik (bukan bot terpisah — hindari konflik polling) |
| Hosting | Auto-deploy dari `main`; `404.html` disediakan |
| Distribusi | Caption otomatis ke channel (WA via OpenWA / Telegram) |

---

## 7. ATURAN UNTUK AI (lapisan agent)

1. Baca `AGENTS.md` proyek sebelum menyentuh apa pun.
2. `git fetch` dulu; bandingkan `draft` vs `main` sebelum generate/publish.
3. Nomor artikel dari main terbaru; resolve draft yang diverged SEBELUM generate.
4. Commit spesifik; tidak pernah force-push; verifikasi hash setelah push
   (`git rev-parse HEAD origin/main` sama).
5. Kredensial tidak pernah di repo; token 401 → laporkan (butuh regenerate),
   jangan retry buta.
6. Satu bot = satu polling; kalau butuh dua konsumen, pisahkan fungsi/bot.
7. Gate yang menunggu manusia WAJIB punya tenggat + default action.
8. Jalur non-kritis (notifikasi) toleran error; jalur kritis (publish) tegas.
9. Kegagalan workflow → alert ke pemilik, jangan diam.

---

## 8. CHECKLIST SETUP PROYEK BARU

- [ ] Repo statis + hosting auto-deploy dari `main`
- [ ] Scheduler cron harian (generate artikel)
- [ ] Bot penulis LLM + pedoman editorial (`PEDOMAN.md`)
- [ ] Branch `draft` + gate ACC via chat pemilik + tenggat auto-tayang
- [ ] Registry anti-duplikat sumber
- [ ] Kolam foto + whitelist stok + aturan alt jujur
- [ ] Distribusi otomatis ke channel pembaca
- [ ] `AGENTS.md` (konteks AI) + `STATUS.md` (ringkasan harian)
- [ ] Alert kegagalan workflow
- [ ] Inventaris kredensial + tes token berkala

---

## 9. CATATAN DESAIN (keputusan 11 Agu 2026)

- **Tanpa peran editor perantara (Sekjen)** — efisiensi token & workflow.
  Pedoman editorial tetap ada sebagai DOKUMEN, bukan sebagai peran.
- **Gate pakai chat pemilik yang sudah ada** — tidak perlu bot baru.
- **Fail-open dengan tenggat** (30 menit tanpa ACC → auto-tayang).
- Pelajaran dari insiden nyata: lihat `PEMBELAJARAN-INFRA.md` (versi generik
  bisa disalin ke repo mana pun).
