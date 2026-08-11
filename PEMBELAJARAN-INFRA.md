# PEMBELAJARAN-INFRA.md — Insiden GH Actions HIFDI (11 Agustus 2026)

> Dokumen pelajaran dari insiden nyata: pipeline artikel harian HIFDI macet
> (workflow merah 20× berturut-turut) dan cara memperbaikinya.
> Ditulis 3 lapis agar bisa dipahami **awam**, dipakai **IT**, dan dibaca **AI**.
> Bisa disalin sebagai ceklis saat menyiapkan proyek portal/otomasi baru.

---

## RINGKASAN EKSEKUTIF (untuk awam)

Bayangkan **toko roti otomatis**:
- Mesin pemanggang (GitHub Actions) membuat roti setiap pagi jam 06:00 — bagian ini MANDIRI.
- Ada **karyawan yang harus memberi izin** sebelum roti ditaruh di etalase (gate ACC):
  ia menunggu jawaban "ya/ACC" atau "tidak/TOLAK" lewat sebuah aplikasi chat (Telegram).
- Yang rusak: **kunci aplikasi chat-nya dicabut** (token bot tidak berlaku) — karyawan
  tidak bisa bertanya, mesin mengeluh tiap 5 menit, dan roti pagi tidak pernah keluar.

**Tiga pelajaran paling penting:**
1. **Kunci (token/kredensial) = satu titik gagal.** Kalau kunci dipakai banyak pintu
   dan dicabut, semua pintu ikut terkunci. Simpan daftar kunci + tes berkala.
2. **Jangan biarkan antrean menumpuk tanpa batas.** Draft yang menunggu berhari-hari
   akhirnya bentrok dengan karya baru (nomor artikel tabrakan) dan macet total.
3. **Izin tanpa batas waktu = macet.** Solusi: beri tenggat — 30 menit tidak dijawab,
   artikel tayang otomatis. Kontrol tetap ada, tapi tidak menggantung.

---

## KRONOLOGI (untuk IT)

| Waktu (WIB) | Kejadian |
|---|---|
| 10 Agu 23:24 | Bot harian push draft article-076 (Kanker Prostat) ke branch `draft` |
| 10 Agu 23:42 | Workflow ACC terakhir kali sukses |
| 11 Agu ~03:00–03:36 | Config bridge (Windows) diubah; dryrun dijalankan |
| 11 Agu 07:33 | Workflow `Publish Draft on ACC` mulai gagal (getUpdates → 401) |
| 11 Agu 23:27 | `Generate HIFDI Article` gagal di step "Siapkan branch draft" (rebase konflik) |
| 11 Agu 23:30+ | Diagnosa: token 401 (semua 3 bot), draft/main diverged, nomor artikel 076 bentrok |
| 11 Agu malam | Fix: draft dibuang, workflow ACC di-pause, gate ACC dipindah ke Hermes (chat) + auto-tayang 30 menit |

---

## PELAJARAN 1 — Kredensial adalah satu titik gagal

**Awam:** Kunci toko dipakai untuk pintu belakang (laptop) dan pintu depan (server).
Begitu kunci diganti tapi pintu-pintunya belum, semuanya terkunci. Cek kunci berkala.

**IT:**
- Token bot Telegram tidak "kedaluwarsa" sendiri — 401 = token dicabut/di-regenerate
  (BotFather `/token`, `/revoke`, atau bot dihapus) TANPA memperbarui semua pemakainya.
- Kasus nyata: token HIFDI dipakai di **2 tempat** (config bridge laptop + GH secret)
  → dicabut sekali, dua-duanya mati. Token 3 bot lain (fmi, ummanitarian) juga 401.
- **Inventaris kredensial wajib:** catat di mana saja sebuah token dipakai.
- **Tes berkala:** `getMe` via curl — 5 detik, ketahuan mati.

**AI (aturan):** Jangan pernah berasumsi token valid. Sebelum menyalahkan logika
pipeline, tes endpoint auth dulu (`GET /bot<token>/getMe`). Jangan menyimpan token
di repo; satu sumber kebenaran (secret manager / config lokal ber-`.gitignore`).
Kalau token 401 muncul: laporkan "token tidak valid — perlu regenerate", jangan
retry tanpa henti.

---

## PELAJARAN 2 — Satu bot, satu polling

**Awam:** Satu nomor WA tidak bisa dipakai dua orang untuk menelepon bersamaan.
Bot chat juga begitu — satu proses yang mendengarkan pada satu waktu.

**IT:** Telegram mengizinkan SATU sesi `getUpdates` per bot. Dua proses (bridge di
laptop + workflow GitHub) memanggil `getUpdates` bot yang sama → HTTP **409 Conflict**
bagi yang kedua. Retry tidak menyelesaikan akar masalah; yang perlu dipisah adalah
pemakaiannya.

**AI (aturan):** Kalau satu bot butuh dua konsumen, jangan rebutan polling — pisahkan
fungsi ke bot berbeda, atau pindahkan salah satu konsumen ke jalur lain (webhook,
chat gateway yang sudah ada). 409 yang berulang = tanda arsitektur, bukan error transient.

---

## PELAJARAN 3 — Draft yang menumpuk = bom waktu

**Awam:** Kalau roti yang sudah jadi dibiarkan di rak belakang berhari-hari, roti baru
besok akan rebutan tempat dan labelnya jadi kacau. Selesaikan antrean setiap hari.

**IT:**
- Branch `draft` dibiarkan diverged dari `main` (2 commit manual masuk ke main,
  draft tidak pernah di-rebase) → step "Siapkan branch draft" (`git merge --ff-only`
  gagal → `git rebase origin/main`) konflik di `index.html` + `used_sources.json`.
- **Bentrok nomor artikel:** draft article-076 (Kanker Prostat) vs main article-076
  (HUT ke-81 RI) — jika ter-publish, draft akan MENIMPA artikel yang sudah tayang.
- Perbaikan: `git push origin --delete draft` (recoverable via commit hash), lalu
  generate berikutnya membuat draft segar dari main yang benar.

**AI (aturan):** Sebelum generate/publish: `git fetch`, bandingkan `origin/draft` vs
`origin/main`. Kalau diverged, resolve DULU (rebase/publish/buang) — jangan generate
di atas state kotor. Nomor artikel: selalu hitung dari `main` terbaru (nomor tertinggi
+ 1), jangan dari draft. Jangan pernah force-push.

---

## PELAJARAN 4 — Gate (izin) butuh tenggat waktu

**Awam:** "Minta izin" itu baik, tapi kalau yang dimintai izin tidak kunjung menjawab,
pekerjaan harus tetap jalan. Aturannya: tunggu 30 menit, kalau tidak dijawab, lanjutkan
otomatis. Yang penting tetap bisa membatalkan SELAMA jendela menunggu.

**IT:**
- Desain awal: draft menunggu ACC/TOLAK TANPA batas → tidak ada balasan = produksi
  berhenti diam-diam (workflow sukses tanpa output, draft menumpuk).
- Desain baru (fail-open dengan timeout): lapor draft jam 06:20 → ACC/TOLAK diterima
  sampai 06:50 → tanpa balasan, auto-publish 06:50.
- Pola ini "kontrol manusia + otonomi mesin": manusia memegang keputusan, mesin
  tidak pernah macet menunggu.

**AI (aturan):** Setiap gate yang menunggu input manusia WAJIB punya timeout dan
perilaku default (publish/buang/lewat). Dokumentasikan eksplisit di prompt:
"kalau 30 menit tidak di-ACC → otomatis tayang". Jangan membuat antrean yang bisa
menumpuk tanpa resolusi.

---

## PELAJARAN 5 — Bagian yang gagal jangan mematikan keseluruhan

**Awam:** Kalau lampu tanda di toko mati, roti tetap harus jadi. Kegagalan kecil
jangan menghentikan produksi utama.

**IT:** `notify_telegram()` di `generate_article.py` sudah dibungkus try/except —
laporan ke Telegram gagal (token 401) tidak membatalkan generate + push draft.
Ini yang membuat generate tetap hidup meski laporan mati.

**AI (aturan):** Bedakan jalur KRITIS (menghasilkan artefak, commit, push) vs jalur
NON-KRITIS (notifikasi, laporan). Yang non-kritis wajib try/except; kegagalannya
dicatat, bukan di-raise. Jangan biarkan langkah pelengkap menggagalkan langkah utama.

---

## PELAJARAN 6 — Verifikasi, jangan percaya output pipeline

**Awam:** "Sudah dikirim" dari mulut mesin belum tentu benar — cek barangnya sampai.

**IT:**
- `git push 2>&1 | tail -n` selalu exit 0 (exit code pipeline = tail) → "PUSH OK" bisa palsu.
- Verifikasi baku: `git fetch origin && git rev-parse HEAD origin/main` — sukses hanya
  kalau dua hash sama.
- Workflow "hijau" ≠ tidak ada masalah (kasus: git commit gagal diam-diam karena
  identitas git tidak diset di runner).

**AI (aturan):** Setelah push/publish, SELALU verifikasi dengan membandingkan hash
atau fetch URL live (HTTP 200 + konten ada). Laporan sukses dari tool = klaim,
bukan bukti. Di CI, set `git config user.name/email` sebelum commit.

---

## PELAJARAN 7 — Kegagalan harus teriak, bukan diam

**Awam:** Kalau lampu mesin merah terus 20 kali, harus ada yang membunyikan alarm —
bukan menunggu pemilik toko menyadarinya sendiri.

**IT:** Workflow ACC gagal ~20× (tiap 5 menit) sejak 07:33 tanpa ada yang tahu sampai
Prinsipal bertanya. Tidak ada alert kegagalan; yang ada hanya laporan hasil sukses.

**AI (aturan):** Sediakan mekanisme alert untuk run GAGAL (bukan hanya deliver hasil
sukses): notifikasi ke chat pemilik, atau job watchdog yang cek status Actions
harian. Kegagalan berulang = tanda sistem butuh perhatian, laporkan proaktif.

---

## CHECKLIST REUSE — set untuk proyek portal/otomasi baru

Salin bagian ini ke proyek baru sebagai ceklis:

- [ ] **1 bot per fungsi** — bot Telegram khusus ACC terpisah dari bot relay/chat.
- [ ] **Inventaris kredensial** — catat semua pemakai tiap token; tes `getMe` berkala.
- [ ] **Kredensial tidak di repo** — secret manager / file `.gitignore`; satu sumber kebenaran.
- [ ] **Branch draft punya siklus hidup** — resolve (publish/buang) maksimal H+1; jangan menumpuk.
- [ ] **Nomor urut dihitung dari main** — bukan dari draft/cache; cegah bentrok.
- [ ] **Gate ber-timeout** — default action kalau tidak dijawab (mis. auto-tayang 30 menit).
- [ ] **Jalur non-kritis toleran error** — notifikasi gagal ≠ generate gagal.
- [ ] **Verifikasi hash setelah push** — jangan percaya exit code pipeline.
- [ ] **Alert kegagalan** — workflow merah harus sampai ke pemilik, bukan diam.
- [ ] **AGENTS.md / STATUS** — aturan & status ditulis agar AI sesi baru langsung paham.

---

## CATATAN ARSITEKTUR BARU (HIFDI, per 11 Agu 2026)

- Generate pagi 06:00 WIB: GitHub Actions (DeepSeek) → push `origin/draft`.
- 06:20 WIB: Hermes (chat Prinsipal) cek draft → kirim **judul + narasi + link foto** → balas ACC/TOLAK.
- 06:50 WIB: tanpa balasan → auto-publish (Hermes).
- Workflow GH `publish-on-acc.yml` di-pause (cron lama mati).
- Tidak ada bot Telegram baru; tidak bergantung bridge/Claude.
