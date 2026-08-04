# RENCANA FMI & UMMANITARIAN — Menuju Otonom (pola HIFDI)

Dibuat: 5 Agu 2026, oleh Admin HIFDI (Staf Mesin), atas permintaan Sekjen.
Status: **DRAFT** — menunggu review Sekjen + keputusan Prinsipal (daftar keputusan di bagian akhir).
Sumber data: verifikasi langsung via GitHub API + cek situs live, 5 Agu 2026 ±01.00 WIB.
Referensi pola: `pp-hifdi/berita-hifdi` (HIFDI = contoh sudah otonom) & `putrosm/otomasi-website-berita` (blueprint 12 dokumen, 3 Agu 2026).

## Ringkasan eksekutif

- **FMI:** ±80% infrastruktur sudah ada (repo, deploy otomatis, register, desain sistem, 54 artikel). Yang kurang: mesin produsen (bot harian). Tahap 1 = adaptasi mesin HIFDI.
- **Ummanitarian:** ±30% (konten & register ada). Hampir semua infra belum ada — termasuk deploy otomatis. Tahap 1 = fondasi, Tahap 2 = bot.

---

## FMI — `BeritaFMI/berita-fmi` → berita.mountaineering-indonesia.org

### (a) Yang sudah ada sekarang

1. Repo publik `BeritaFMI/berita-fmi`, branch `main`. Situs **live** (HTTP 200, terverifikasi 5 Agu).
2. **Deploy OTOMATIS:** `.github/workflows/deploy.yml` (wrangler-action → Cloudflare Pages, project `berita-fmi`, folder `berita/`). Run sukses terus; terakhir 4 Agu 10:11 UTC. Secrets `CLOUDFLARE_API_TOKEN` & `CLOUDFLARE_ACCOUNT_ID` sudah terpasang.
3. **54 artikel** HTML di `berita/` (nomor 1–64; bolong 2–10 & 44 — penomoran lama tidak rapat; register tetap sumber kebenaran). 35 gambar `img/NNN-slug.jpg`.
4. `BERITA-REGISTER.md` (salinan di `_meta/`) — sumber kebenaran penomoran, **Next Available Number: 065**.
5. `_operasional/DESAIN-SISTEM.md` — spesifikasi lengkap: bilingual `data-id`/`data-en`, 9 kategori + emoji, tag warna merah (artikel FMI) vs hitam (eksternal), card thumb vs icon, token warna & tipografi. Kualitas tinggi — bot bisa mengikuti spesifikasi ini.
6. `SEKJEN.md` FMI — papan keputusan. **Keputusan 4 Agu 2026: FMI TIDAK punya peran "Admin FMI"; urusan FMI dipegang Sekjen langsung.**
7. Produksi saat ini: **manual oleh Sekjen (Claude)**. Artikel terbaru: 064 (4 Agu 2026).
8. Format artikel: HTML lengkap, **bilingual ID/EN**, `og:image` 1200×630 → `img/NNN-slug.jpg`.

### (b) Penghalang menuju otonom

1. **TIDAK ADA mesin produsen** — belum ada workflow generate harian, script penarik RSS, pemanggil LLM. 1 artikel = 1 sesi manual Claude.
2. **TIDAK ADA sourcing RSS** — belum ada daftar feed pendakian, kata kunci, filter bobot, blocklist. Feed niche belum diuji dari IP GitHub (pembelajaran HIFDI: CNN & Health Affairs mati dari IP GitHub).
3. **TIDAK ADA penjaga duplikat** — belum ada `used_sources.json`; risiko kembar/ulang topik (HIFDI pernah kena bug kembar article-063/064 — jangan diulangi).
4. **TIDAK ADA suara editorial machine-readable** — SYSTEM_PROMPT & `config.py` FMI belum ada.
5. **Format bilingual menambah kompleksitas** — bot harus menulis ID + EN untuk tiap elemen (`data-id`/`data-en`); prompt & validasi pasangan elemen wajib.
6. **Sumber gambar** — HIFDI pakai daftar putih Unsplash terverifikasi; FMI pakai gambar nyata per artikel. Asal gambar untuk bot belum diputuskan.
7. **Register manual** — bot harus bisa membaca nomor berikut & meng-update `BERITA-REGISTER.md`.
8. **Kredensial** — `DEEPSEEK_API_KEY` belum ada di secrets repo FMI; PAT butuh scope `workflow` untuk menyentuh `.github/workflows/`.
9. **Koordinasi** — tanpa peran "Admin FMI", jalur kerja Hermes di repo FMI harus eksplisit (usulan: Hermes tetap Staf Mesin, bekerja atas permintaan Sekjen, dicatat di SEKJEN.md FMI).

### (c) Rencana bertahap

**TAHAP 1 — Mesin produsen** (prasyarat: K1, K2, K3)
1. Adaptasi mesin HIFDI → FMI: `scripts/generate_article.py` (template bilingual, penomoran dari register, path `berita/NNN-slug.html` + `img/`), `scripts/config.py` (feed, kata kunci, blocklist, SYSTEM_PROMPT bilingual, daftar gambar), `scripts/used_sources.json` (backfill 54 artikel).
2. Uji feed pendakian: Google News RSS (pendakian gunung, ekspedisi, alpinisme, himalaya, gunung merapi, fmi, panjat tebing) + feed terbitan mountaineering bila ada. Uji jaringan rumah DULU, lalu IP GitHub; tambah **bertahap 3 feed inti** (pola HIFDI).
3. Workflow `.github/workflows/daily-generate.yml` (cron 06.00 WIB, DeepSeek API).
4. Uji lokal di venv (feedparser + openai): draf stok bersih terbit, URL kembar ditolak → `stok/_ditolak/`, stok kosong → RSS. Bersihkan artefak uji sebelum push.
5. Pilot: bot terbit beberapa artikel; Sekjen audit (bilingual benar, sumber nyata, tidak kembar, gambar sah).

**TAHAP 2 — Amunisi & koordinasi**
1. Folder `stok/` FMI (draf lengkap Sekjen) + pembaca stok (prioritas sebelum RSS).
2. Update register otomatis oleh bot (atau register JSON paralel — keputusan K4).
3. Notifikasi hasil ke Telegram (pola HIFDI).
4. STATUS-SEKJEN.md per portal atau gabung lintas-portal (K5).

**TAHAP 3 — Otonom penuh & pengawasan**
1. Pantau 2–4 minggu: run sukses, mutu artikel, feed hidup.
2. Tuning: tambah feed bertahap (pola HIFDI: 13 sisanya), bobot kata kunci.
3. Klausul suksesi FMI (adopsi HIFDI §6): bot tetap jalan bila Sekjen hilang; ambang bahaya = sumber karangan → matikan cron, lapor Prinsipal.
4. Sinkronisasi register vs artikel terbit; putuskan nasib lubang nomor 2–10 & 44 (K6).

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

1. **TIDAK ADA deploy otomatis** — belum ada workflow apa pun; artikel di-upload manual. Ini penghalang PALING DASAR (FMI sudah punya deploy.yml, Ummanitarian belum).
2. **TIDAK ADA mesin produsen** — sama seperti FMI: belum ada generate workflow, RSS, script, LLM.
3. **TIDAK ADA penjaga duplikat & suara editorial mesin** — belum ada `used_sources.json`, `config.py`, SYSTEM_PROMPT.
4. **Feed niche kemanusiaan belum diuji** — kandidat: ReliefWeb, OCHA/UN, IFRC, WHO emergencies, Google News RSS (humanitarian, disaster response, famine, refugee, flood, earthquake response). Belum diverifikasi hidup dari IP GitHub.
5. **og-image tunggal** untuk semua artikel = preview share seragam; per artikel lebih baik (K7).
6. **Struktur folder `NNN-slug/`** berbeda dari HIFDI/FMI (file di root) — script harus adaptasi path & link relatif.
7. **Bahasa EN** — SYSTEM_PROMPT bot harus EN (bukan ID seperti HIFDI).
8. **Alur guest writer harus dipertahankan** — register menandai produsen; bot jangan menimpa/menduplikasi naskah guest.
9. **Kredensial belum ada** di repo ini: CF token/account, DeepSeek key; nama project Cloudflare Pages untuk insight.ummanitarian.org perlu dikonfirmasi (situs sudah live, kemungkinan project sudah ada di dashboard).
10. **`.gitignore *.md`** menghambat pedoman & register baru.

### (c) Rencana bertahap

**TAHAP 1 — Fondasi** (prasyarat: K8, K9)
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
| K1 | Pasang `DEEPSEEK_API_KEY` di secrets `BeritaFMI/berita-fmi` (1 key bisa dipakai 3 portal) | Prinsipal | Tahap 1 FMI |
| K2 | PAT scope `workflow` untuk push workflow FMI | Prinsipal | Tahap 1 FMI |
| K3 | Sumber gambar bot FMI: daftar putih baru / lisensi bebas / tetap manual Sekjen | Sekjen | Tahap 1 FMI |
| K4 | Format register FMI: tetap MD (bot parse) atau tambah JSON paralel | Sekjen | Tahap 2 FMI |
| K5 | STATUS-SEKJEN.md: per portal atau 1 file lintas-portal | Sekjen | Segera |
| K6 | Lubang penomoran FMI (2–10, 44): dibiarkan atau dinormalisasi | Sekjen | Nanti |
| K7 | og-image Ummanitarian: tetap 1 global atau per artikel | Sekjen | Tahap 2 Umm |
| K8 | Nama project Cloudflare Pages untuk insight.ummanitarian.org (cek dashboard) | Prinsipal | Tahap 1 Umm |
| K9 | Secrets CF (token/account) + DeepSeek di repo Ummanitarian | Prinsipal | Tahap 1–2 Umm |

## Catatan koordinasi

- **Blueprint sudah ada:** `putrosm/otomasi-website-berita` (12 dokumen: konsep, otomasi terjadwal, RSS, penjaga duplikat, kotak amunisi, hosting, tim agen AI, server 24 jam, backup, jebakan & solusi, glosarium + 3 script). Semua pola di rencana ini mengikuti blueprint. Repo itu publik berisi materi belajar — jangan taruh kredensial di sana.
- **HIFDI tetap piloting:** mesin HIFDI jangan dirombak untuk keperluan FMI/Ummanitarian — duplikasi script per portal lebih aman daripada berbagi file.
- Bot DeepSeek di GitHub Actions = otak Pekerja; biaya token API ditanggung Prinsipal (keputusan biaya).
- Standar mutu & klausul suksesi HIFDI (SEKJEN.md §3, §6) diadopsi sebagai standar bersama.
- File ini sengaja ditaruh di repo HIFDI (tempat Staf Mesin berkantor & dibaca Sekjen tiap pagi); bisa dipindah ke repo masing-masing atas arahan Sekjen.
