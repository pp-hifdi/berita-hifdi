# STATUS-SEKJEN.md — ringkasan pagi (dirawat Admin HIFDI; update tiap selesai kerjaan penting)

**Update terakhir:** 9 Agu 2026 (Ummanitarian: search + pagination LIVE)

## UMMANITARIAN — search box + pagination arsip (9 Agu 2026, perintah Prinsipal)
- **Masalah pembaca:** tidak ada kolom cari, dan semua artikel menggantung di satu halaman (scroll tak berujung).
- **Eksekusi (commit `bf771d4`, repo `putrosm/ummanitarian-insight`):**
  1. **Search client-side** — kotak di header (desktop & mobile), `search-index.json` (41 entri: 32 artikel lokal + 9 kartu kurasi eksternal) di-generate `scripts/gen_site_pages.py` + `search.js`. Tes live: ketik "sudan" → 4 hasil. Tanpa backend, tanpa dependency.
  2. **Pagination** — 10 kartu/halaman: `page-2/` s.d. `page-5/` (hero tetap hanya di halaman 1; halaman arsip tanpa hero, h1 sr-only, canonical sendiri, script filter versi aman). `index.html` halaman 1 tetap manual (alur hero-swap Sekjen tidak diganggu).
- **Idempoten:** generator membaca kartu dari index.html + page-N yang ada (dedupe per href, urutan editorial dipertahankan). **Setiap publish artikel baru → jalankan `scripts/gen_site_pages.py`** sebelum commit (atau minta Admin HIFDI).
- **Wilayah tak tersentuh:** hero, ticker, sidebar, about, footer, CSS, artikel, register. File baru di root: `search.js`, `search-index.json`, `scripts/gen_site_pages.py`, `page-2..5/`.
- **Verifikasi live:** homepage 200 + search box tampil, `/search-index.json` 41 entri, `/page-2/` & `/page-5/` 200, pages.dev 200.


## SOP PAGI — revisi 8 Agu 2026 (koreksi Prinsipal: cek pipeline dulu, baru produksi)
0. **05.55** — Hermes cek pipeline (cron): OpenWA session ready? cron caption aktif? clone sehat? situs 200? Merah → perbaiki dulu (auto-fix OpenWA), baru produksi.
1. **06.00** — bot GH Actions tersulut: `stok/` → RSS → DeepSeek tulis → foto gilir → article-0XX → commit → deploy LIVE.
2. **±06.25** — caption hangat → WAG Bangkit + info ke chat Prinsipal (deliver telegram).
3. **07.00** — watchdog: sudah terbit? belum → trigger ulang + lapor.
Aturan: pipeline macet = berhenti & perbaiki; Admin tidak trigger manual tanpa konfirmasi Prinsipal.

## Keputusan Prinsipal (8 Agu 2026)
- **KETERANGAN ILUSTRASI WAJIB:** foto stok/CC yang bukan objek berita tidak boleh tampil tanpa penjelasan (bisa diasosiasikan sebagai klinik/instansi bersangkutan). Featured image wajib caption tampak "Ilustrasi: … — bukan <objek> pada berita" + alt deskriptif + atribusi lisensi; berlaku manual & bot. Preseden: article-069 → cat-20 (Puskesmas Tamblong, CC BY-SA 4.0, ≤150KB).
- **ATURAN GEOGRAFI FOTO:** berita Indonesia → gambar dari Indonesia; berita luar negeri → gambar boleh dari luar negeri. Jangan ketukar (foto landmark asing untuk berita Indonesia = pelanggaran). Foto generik netral (tanpa lokasi terlihat) aman untuk keduanya.

## Kerjaan selesai (7 Agu 2026, Admin HIFDI)
- **article-072 terbit MANUAL (perintah Prinsipal, acc langsung):** "Gula Berlebih pada Anak: Banyak Anak SD Sudah Berisiko Diabetes" (Edukasi, 7 Agu). Sumber 4 feed (ANTARA, BBC Indonesia, Kemenko PMK, MetroTV) via Google News; gambar sistem gilir `cat-03-003` (by-sa). LIVE terverifikasi (artikel/foto/og 200, kartu tampil, count 68). Caption WAG otomatis menyusul (cron `*/5`).
- **Run bot 7 Agu SKIP oleh cron GitHub** (bukan batal — TERTUNDA ~12 mnt). Admin trigger manual 08:27 (article-070) → cron telat jalan 08:39 (article-071) = **2 artikel 1 hari (dobel, kesalahan Admin: trigger tanpa konfirmasi)**. Prinsipal memutuskan biarkan keduanya. Watchdog Hermes dipasang `0 7 * * *` (07:00 WIB) — trigger otomatis hanya kalau sampai 07.00 belum ada run; aturan baru: Admin tidak trigger manual tanpa konfirmasi Prinsipal.
- **Foto konteks artikel (perintah Prinsipal):** article-070 (UNNES/mahasiswa) → `cat-18` mahasiswa Indonesia (CC BY-SA 4.0, Wikimedia); article-071 (Sierra Leone) → `cat-19` Connaught Hospital Freetown (CC BY 2.0, Wikimedia). QC vision lolos, og 1200×630 dibuat, registry di-update. LIVE terverifikasi.
- **Caption WAG otomatis dipercepat `*/15 → */5`** — artikel terbit ≤5 mnt → WAG + info ke Telegram Prinsipal.
- **SOP TAKE DOWN dibuat (7 Agu, acc Prinsipal):** keputusan level Admin HIFDI, taktis, TANPA ACC Sekjen (paralel publish). 3 tingkat: errata / tarik (`scripts/takedown.py --tarik` → `_ditarik/`) / hapus (`--hapus`). Info wajib via STATUS ini + pesan koreksi WAG bila caption tersebar. Dok: `docs/SOP-TAKE-DOWN.md`.

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
- **Ummanitarian (FOKUS SEKARANG, arahan Prinsipal 8 Agu — satu kantor berita per rencana):** scoping selesai (5 Agu) → `RENCANA-UMMANITARIAN.md` (DRAFT). Paling dasar: deploy otomatis belum ada (tahap 1). Butuh: U2–U3 (Prinsipal) + U1 (Sekjen).
- **FMI (DITUNDA):** scoping selesai (5 Agu) → `RENCANA-FMI.md`. Situs + deploy CF otomatis sudah jalan; kurang = bot produsen (tahap 1). Dikerjakan SETELAH Ummanitarian.

## Butuh keputusan Sekjen
1. **Review RENCANA-UMMANITARIAN.md** — 3 keputusan: U1 (og-image, Sekjen), U2–U3 (Cloudflare, Prinsipal). Urgent U2–U3 (prasyarat Tahap 1).
2. **FMI menyusul** — `RENCANA-FMI.md` (K1–K6) dibuka lagi setelah Ummanitarian jalan.

## Uji akses Ummanitarian (8 Agu 2026, perintah Prinsipal — Admin coba sejauh mana bisa terbitkan artikel)
- **HASIL: FULL SUCCESS — tidak mentok sama sekali.** Admin (Hermes) buat artikel **033-afghanistan-hunger-funding-gap** ("Twenty-Six Per Cent: Afghanistan's Hunger Is Outrunning Its Funding", 8 Agu, sumber REACH/UN via Kabul Tribune + KabulNow), push ke `putrosm/ummanitarian-insight` SUKSES → **auto-deploy Cloudflare Pages jalan** → LIVE terverifikasi (artikel 200, hero index berganti, kartu 032 tetap di grid).
- **TEMUAN PENTING:** deploy Ummanitarian memakai **GitHub integration** Cloudflare (push → auto-deploy), jadi **tidak perlu secret CF token/account di repo** — U3 tinggal `DEEPSEEK_API_KEY` saja (dipakai nanti untuk bot, Tahap 2). U2 tuntas: project = `ummanitarian-insight`.
- **Register:** 033 dicatat produsen **"Hermes (Staf Mesin)"** (jujur, bukan Claude).
- **BUTUH SEKJEN:** (1) review editorial artikel 033 — mutu & kesesuaian suara situs; (2) putuskan kewenangan Hermes publish di Ummanitarian (dengan aturan apa; usulan: tetap lewat arahan Sekjen/Prinsipal, dicatat di register). Struktur/template artikel TIDAK diubah (CSS identik dengan 032).
- **REHEARSAL "human-in-the-loop" (8 Agu, acc Prinsipal):** artikel **034-iom-2025-reach-funding-gap** terbit lewat alur draft → review → ACC → terbit (bukan langsung push). SOP Sekjen (struktur artikel + proses cari gambar: tematik, lisensi jelas, caption 3 unsur, kredit) **sudah dipetakan & disimpan permanen** (skill Hermes: `references/ummanitarian-sop-sekjen.md`) supaya bisa ditiru persis oleh agen/bot. Artikel 034 live & terverifikasi. Tahap berikut: uji Buzz (workspace agen+manusia) menyusul.

## Klarifikasi Cloudflare Ummanitarian (8 Agu 2026, hasil cek Admin — minta konfirmasi Prinsipal)
- **U2 TERJAWAB dari DNS (tanpa dashboard):** project Cloudflare Pages insight.ummanitarian.org = **`ummanitarian-insight`** (CNAME → ummanitarian-insight.pages.dev, HTTP 200 terverifikasi 8 Agu). Ketiga situs di Cloudflare: ummanitarian-insight / berita-hifdi / berita-fmi.
- **PERTANYAAN KE PRINSIPAL (via Sekjen):** project `ummanitarian-insight` ada di akun Cloudflare (email) yang **SAMA** dengan berita-hifdi/berita-fmi, atau **akun terpisah**?
  - Sama → token CF yang sudah dipakai HIFDI/FMI bisa langsung dipakai → U3 = tinggal salin secrets ke repo Ummanitarian, tidak perlu token baru.
  - Beda → perlu API token Pages-edit dari akun pemilik project; token lama TIDAK bisa dipakai lintas akun.
- Yang diminta: konfirmasi akun/email pemilik project + ketersediaan token untuk akun itu.
