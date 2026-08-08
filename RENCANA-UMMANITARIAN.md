# RENCANA UMMANITARIAN — Menuju Otonom (pola HIFDI)

Dibuat: 5 Agu 2026 oleh Admin HIFDI (Staf Mesin), atas permintaan Sekjen.
Dipecah dari `RENCANA-FMI-UMMANITARIAN.md` atas arahan Prinsipal (8 Agu 2026):
**satu kantor berita = satu dokumen rencana.** Ummanitarian fokus sekarang;
FMI dipindah ke `RENCANA-FMI.md` (dikerjakan menyusul, satu-satu).
Status: **DRAFT** — menunggu review Sekjen + keputusan Prinsipal (U1–U3 di bagian akhir).
Sumber data: verifikasi langsung via GitHub API + cek situs live, 5 Agu 2026 ±01.00 WIB.
Referensi pola: `pp-hifdi/berita-hifdi` (HIFDI = contoh sudah otonom) & `putrosm/otomasi-website-berita` (blueprint 12 dokumen, 3 Agu 2026).

## Ringkasan eksekutif

- **Ummanitarian:** ±30% siap (konten & register ada). Hampir semua infra belum ada — termasuk deploy otomatis. Tahap 1 = fondasi, Tahap 2 = mesin bot.

---

## Ummanitarian — `putrosm/ummanitarian-insight` → insight.ummanitarian.org

### (a) Yang sudah ada sekarang

1. Repo publik `putrosm/ummanitarian-insight`, branch `main`. Situs **live** (HTTP 200, terverifikasi 5 Agu).
2. **31 artikel**, format folder `NNN-slug/index.html` (002–032). Konten **berbahasa Inggris**.
3. `KONTEN-REGISTER.md` — sumber kebenaran penomoran (002–032 + kurasi eksternal `wadem-congress-2027` → wadem.org). Menandai produsen: **Claude** (internal) / **guest** (Kamal Putra Pratama) / kurasi eksternal.
4. `og-image.jpg` (1 file di root — kemungkinan dipakai semua artikel).
5. `index.html` master (kartu artikel).
6. `.gitignore` berisi `*.md` — register terlanjur ter-track (tetap ke-commit), tapi file `.md` baru tidak ikut commit otomatis.

### (b) Penghalang menuju otonom

1. **TIDAK ADA deploy otomatis** — belum ada workflow apa pun; artikel di-upload manual. Ini penghalang PALING DASAR.
2. **TIDAK ADA mesin produsen** — belum ada generate workflow, RSS, script, LLM.
3. **TIDAK ADA penjaga duplikat & suara editorial mesin** — belum ada `used_sources.json`, `config.py`, SYSTEM_PROMPT.
4. **Feed niche kemanusiaan belum diuji** — kandidat: ReliefWeb, OCHA/UN, IFRC, WHO emergencies, Google News RSS (humanitarian, disaster response, famine, refugee, flood, earthquake response). Belum diverifikasi hidup dari IP GitHub.
5. **og-image tunggal** untuk semua artikel = preview share seragam; per artikel lebih baik (U1).
6. **Struktur folder `NNN-slug/`** berbeda dari HIFDI/FMI (file di root) — script harus adaptasi path & link relatif.
7. **Bahasa EN** — SYSTEM_PROMPT bot harus EN (bukan ID seperti HIFDI).
8. **Alur guest writer harus dipertahankan** — register menandai produsen; bot jangan menimpa/menduplikasi naskah guest.
9. **Kredensial belum ada** di repo ini: CF token/account, DeepSeek key. Nama project = **`ummanitarian-insight`** (terverifikasi via DNS 8 Agu 2026 — tidak perlu cek dashboard); yang belum jelas = **akun/email Cloudflare pemilik project** & ketersediaan token untuk akun itu.
10. **`.gitignore *.md`** menghambat pedoman & register baru.

### (c) Rencana bertahap

**TAHAP 1 — Fondasi** (prasyarat: U2, U3)
1. Workflow `.github/workflows/deploy.yml` (wrangler-action, project Cloudflare Pages — nama dikonfirmasi Prinsipal dari dashboard) + secrets CF. Setelah ini tiap push langsung tayang.
2. Pedoman koordinasi: `SEKJEN.md` Ummanitarian (papan pesan, wilayah, aturan) + `CLAUDE.md` (suara editorial, standar mutu, prosedur publish). Draft disiapkan Hermes, **disahkan Sekjen**.
3. Perbaiki `.gitignore` (kecualikan register & pedoman dari aturan `*.md`).
4. Uji feed kemanusiaan (ReliefWeb/OCHA/IFRC + Google News RSS) dari rumah → IP GitHub, bertahap.

**TAHAP 2 — Mesin produsen**
1. Adaptasi `generate_article.py` (template Ummanitarian, path `NNN-slug/index.html`, EN, update register), `config.py` (feed, kata kunci, blocklist, SYSTEM_PROMPT EN, daftar gambar), `used_sources.json` (backfill 31 + wadem).
2. Workflow `daily-generate.yml` (cron 06.00 WIB, DeepSeek) + secret `DEEPSEEK_API_KEY`.
3. Uji lokal skenario wajib (stok bersih, URL kembar ditolak, RSS normal).
4. Pilot + audit Sekjen.

**TAHAP 3 — Otonom penuh & pengawasan**
1. Alur guest writer: `stok/guest` atau folder khusus + flag register; naskah kiriman muat utuh (pola HIFDI article-057).
2. `stok/` amunisi Sekjen + pembaca stok.
3. Pantau 2–4 minggu; tuning feed/kata kunci; tambah feed bertahap.
4. Notifikasi Telegram; klausul suksesi; sinkronisasi register.

---

## Keputusan yang dibutuhkan

| Kode | Keputusan | Pemutus | Dibutuhkan |
|------|-----------|---------|------------|
| U1 | og-image: tetap 1 global atau per artikel | Sekjen | Tahap 2 |
| U2 | Project CF Pages = `ummanitarian-insight` (**TERVERIFIKASI via DNS 8 Agu**); sisa: konfirmasi akun/email pemilik | Prinsipal | Tahap 1 |
| U3 | Secrets CF (token/account — tergantung akun pemilik project) + DeepSeek di repo Ummanitarian | Prinsipal | Tahap 1–2 |

## Catatan koordinasi

- **KEPUTUSAN INFRASTRUKTUR (Sekjen, 5 Agu 2026): TIDAK pakai VPS.** Laptop rumah nyala 24/7 khusus untuk host Hermes. Bot berita (HIFDI dan nanti Ummanitarian/FMI) **TETAP jalan di GitHub Actions**, bukan di laptop. Deploy & bot tetap di GitHub Actions + Cloudflare Pages.
- **Blueprint sudah ada:** `putrosm/otomasi-website-berita` (12 dokumen). Semua pola di rencana ini mengikuti blueprint. Repo itu publik berisi materi belajar — jangan taruh kredensial di sana.
- **HIFDI tetap piloting:** mesin HIFDI jangan dirombak untuk keperluan portal lain — duplikasi script per portal lebih aman daripada berbagi file.
- Bot DeepSeek di GitHub Actions = otak Pekerja; biaya token API ditanggung Prinsipal (keputusan biaya).
- Standar mutu & klausul suksesi HIFDI (SEKJEN.md §3, §6) diadopsi sebagai standar bersama.
- Perintah eksekusi ke Staf Mesin (Hermes) lewat papan pesan `SEKJEN.md` repo HIFDI — Prinsipal cukup memerintah Sekjen, Sekjen yang menugaskan Hermes.
- FMI tidak dibahas di sini — lihat `RENCANA-FMI.md` (ditunda; dikerjakan setelah Ummanitarian).
- File ini sengaja ditaruh di repo HIFDI (tempat Staf Mesin berkantor & dibaca Sekjen tiap pagi); bisa dipindah ke repo Ummanitarian atas arahan Sekjen.
