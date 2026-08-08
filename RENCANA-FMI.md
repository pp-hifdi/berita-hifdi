# RENCANA FMI — Menuju Otonom (pola HIFDI)

Dibuat: 5 Agu 2026 oleh Admin HIFDI (Staf Mesin), atas permintaan Sekjen.
Dipecah dari `RENCANA-FMI-UMMANITARIAN.md` atas arahan Prinsipal (8 Agu 2026):
**satu kantor berita = satu dokumen rencana.** Status: **DITUNDA** — fokus
sekarang Ummanitarian (`RENCANA-UMMANITARIAN.md`); FMI dikerjakan menyusul.
Sumber data: verifikasi langsung via GitHub API + cek situs live, 5 Agu 2026 ±01.00 WIB.
Referensi pola: `pp-hifdi/berita-hifdi` (HIFDI = contoh sudah otonom) & `putrosm/otomasi-website-berita` (blueprint 12 dokumen, 3 Agu 2026).

## Ringkasan eksekutif

- **FMI:** ±80% infrastruktur sudah ada (repo, deploy otomatis, register, desain sistem, 54 artikel). Yang kurang: mesin produsen (bot harian). Tahap 1 = adaptasi mesin HIFDI.

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

## Keputusan yang dibutuhkan

| Kode | Keputusan | Pemutus | Dibutuhkan |
|------|-----------|---------|------------|
| K1 | Pasang `DEEPSEEK_API_KEY` di secrets `BeritaFMI/berita-fmi` (1 key bisa dipakai 3 portal) | Prinsipal | Tahap 1 |
| K2 | PAT scope `workflow` untuk push workflow FMI | Prinsipal | Tahap 1 |
| K3 | Sumber gambar bot FMI: daftar putih baru / lisensi bebas / tetap manual Sekjen | Sekjen | Tahap 1 |
| K4 | Format register FMI: tetap MD (bot parse) atau tambah JSON paralel | Sekjen | Tahap 2 |
| K5 | STATUS-SEKJEN.md: per portal atau 1 file lintas-portal | Sekjen | Segera |
| K6 | Lubang penomoran FMI (2–10, 44): dibiarkan atau dinormalisasi | Sekjen | Nanti |

## Catatan koordinasi

- **KEPUTUSAN INFRASTRUKTUR (Sekjen, 5 Agu 2026): TIDAK pakai VPS.** Laptop rumah nyala 24/7 khusus untuk host Hermes. Bot berita TETAP jalan di GitHub Actions, bukan di laptop.
- **Blueprint sudah ada:** `putrosm/otomasi-website-berita` (12 dokumen). Semua pola mengikuti blueprint. Repo itu publik — jangan taruh kredensial di sana.
- **HIFDI tetap piloting:** mesin HIFDI jangan dirombak — duplikasi script per portal lebih aman.
- Bot DeepSeek di GitHub Actions = otak Pekerja; biaya token API ditanggung Prinsipal.
- Standar mutu & klausul suksesi HIFDI (SEKJEN.md §3, §6) diadopsi sebagai standar bersama.
- **DITUNDA (8 Agu 2026, arahan Prinsipal):** dikerjakan satu-satu — Ummanitarian dulu, FMI menyusul.
- File ini sengaja ditaruh di repo HIFDI (tempat Staf Mesin berkantor); bisa dipindah ke repo FMI atas arahan Sekjen.
