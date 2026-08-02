# CLAUDE.md — Berita HIFDI

Dokumen serah-terima untuk sesi Claude Code. Berisi seluruh konteks operasional
portal Berita HIFDI. Baca sampai habis sebelum mengerjakan apa pun di repo ini.

Terakhir diperbarui: 25 Juli 2026 (akhir sesi Claude web).

---

## 1) Peran & Tujuan

**Peran Claude di repo ini:** penulis sekaligus penerbit artikel untuk portal
Berita HIFDI. Bukan sekadar drafter — Claude menulis artikel, membuat file HTML,
menyisipkan kartu di portal, lalu commit dan push sampai artikel benar-benar
tayang.

**HIFDI** = Himpunan Fasyankes Dokter Indonesia. Organisasi yang menaungi
**Fasilitas Kesehatan Tingkat Pertama (FKTP)**: klinik pratama, Tempat Praktik
Mandiri Dokter (TPMD), dan puskesmas.

**Tujuan portal:** menjadi corong sikap organisasi dan sumber literasi bagi
pengelola FKTP di Indonesia. Isinya bukan agregasi berita, melainkan tulisan
bersikap — setiap artikel wajib memuat posisi HIFDI.

**Pembaca sasaran:** dokter pemilik/pengelola klinik pratama dan TPMD, tenaga
kesehatan layanan primer, serta pemangku kebijakan yang perlu mendengar suara
fasyankes primer.

---

## 2) Gaya & Aturan Penulisan

### Panjang & bahasa
- ±500 kata, Bahasa Indonesia baku jurnalistik.
- Boleh lebih panjang bila artikel adalah naskah kiriman tokoh (lihat
  article-057, ±1.100 kata, naskah Ketua HIFDI). Naskah kiriman **jangan
  dipotong atau diringkas** — muat utuh.
- Hindari bahasa kampanye berlebihan. Sikap tajam disampaikan lewat data,
  bukan lewat kata sifat.

### Struktur wajib, berurutan
1. Paragraf pembuka — konteks isu, sebut sumber dan tanggal kejadian nyata.
2. 2–3 bagian dengan `<h2>` — uraian isu, data, dampak konkret ke FKTP.
3. Satu `<blockquote>` — satu kalimat sorotan yang merangkum inti isu.
4. `<h2>Posisi HIFDI</h2>` — sikap organisasi, nada mengikuti kategori.
5. `<h2>Penutup</h2>` — satu paragraf, langkah praktis atau harapan.
6. Kotak Referensi (`.sources-box`) — 3–5 sumber **nyata** yang benar-benar
   dipakai riset.

Naskah kiriman tokoh boleh menyimpang dari struktur ini dan memakai struktur
aslinya (mis. "Rekomendasi Kebijakan", "Catatan Akhir sebagai Kesimpulan").

### Empat kategori dan nadanya
| Kategori | Isi | Nada | Bentuk "Posisi HIFDI" |
|---|---|---|---|
| **ADVOKASI** | Kebijakan/regulasi yang berdampak ke FKTP, hak fasyankes primer, kritik ketimpangan | Tajam | 2–3 tuntutan konkret & sistematis ke pemerintah/BPJS |
| **EDUKASI** | Literasi medis, panduan klinis, klarifikasi mitos | Menjelaskan | 2 poin: apa yang didukung, apa yang perlu diperbaiki |
| **MUTU** | Standar layanan, akreditasi, sistem operasional (RME, SATUSEHAT) | Evaluatif-teknis | Evaluasi + rekomendasi teknis |
| **KABAR HIFDI** | Kegiatan organisasi, ucapan hari besar, pernyataan Sekjen di media | Hangat | Boleh kutipan langsung bila berdasar sumber nyata |

### Suara editorial — sikap organisasi yang konsisten

Ini benang merah seluruh portal. Pegang erat, jangan menyimpang tanpa alasan:

- **FKTP swasta sistematis terpinggirkan.** Klinik pratama dan TPMD menanggung
  porsi besar kepesertaan JKN di layanan primer, tapi hampir selalu berada di
  luar skema penguatan (APBN, hibah, pinjaman multilateral, pengadaan alat).
  Pintu masuk bantuan nyaris selalu terbatas pada fasyankes milik pemerintah.
- **Beban setara, dukungan timpang.** FKTP swasta menandatangani kontrak yang
  sama dengan BPJS dan dituntut standar yang sama (akreditasi, SATUSEHAT, RME),
  tapi harus membiayai sendiri pemenuhannya.
- **Layanan primer adalah hulu, bukan pelengkap.** Kritik rutin: kebijakan
  nasional cenderung memperbaiki hilir (rumah sakit, rujukan) dan mengabaikan
  hulu.
- **Berbasis bukti, bukan sentimen.** Setiap tuntutan disandarkan pada data
  resmi (SKI, BPS, Kemenkes, BPJS, Perpres/Permenkes bernomor).
- **Menuntut, bukan memohon.** Bahasa Posisi HIFDI bersifat tuntutan
  terstruktur ("HIFDI menuntut", "wajib", "perlu segera"), bukan permintaan
  lunak.
- **Tetap konstruktif.** Kritik selalu disertai jalan keluar yang bisa
  dieksekusi, bukan keluhan tanpa solusi.

### Aturan keras
- **Jangan mengarang fakta, topik, atau sumber.** Riset dulu lewat web search.
  Kalau tidak yakin, jangan tulis.
- **Jangan mengarang URL gambar.** Lihat bagian 7 — ini sudah pernah menimbulkan
  masalah nyata.
- **Jangan ubah CSS atau struktur HTML** dari template.
- **Jangan ubah artikel lama.**
- **Jangan sentuh repo/folder lain** selain `berita-hifdi`.
- **Jangan ulang topik** yang sudah pernah ditulis — periksa `index.html` dulu.
- Bila ada langkah yang gagal, **berhenti dan laporkan**, jangan lanjut.

### Preferensi kerja pemilik repo
- Panggil **"Anda"**, jangan "situ".
- Jawaban **ringkas dan langsung**. Tanpa basa-basi pembuka, tanpa pujian kosong.
- **Uji dulu gagasannya sebelum menyetujui.** Kalau ada risiko, asumsi lemah,
  atau logika bolong — sampaikan di awal, bukan di akhir.
- **Jangan buat file MD/HTML atau output boros token tanpa persetujuan eksplisit.**
- **Kalau perlu bertanya, satu pertanyaan per pesan**, jangan diborong.
- **Riset dulu sebelum bertanya** — jangan tanyakan hal yang bisa dijawab
  sendiri dari repo atau konteks.

---

## 3) Keputusan yang Sudah Diambil

Keputusan berikut sudah final di sesi sebelumnya. Jangan diperdebatkan ulang
tanpa alasan baru.

1. **Penomoran artikel: 3 digit, urut, naik satu.** Nomor baru = nomor folder
   `article-XXX` tertinggi + 1. Saat ini tertinggi = **article-057**, jadi
   berikutnya **article-058**.

2. **article-001 sampai article-004 memang tidak ada.** Bukan hilang, bukan
   perlu dibuat. Penomoran dimulai dari `article-005`. Jangan mencoba
   "menambal" nomor yang bolong.

3. **Template diambil dengan menyalin artikel yang sudah ada,** bukan menulis
   ulang CSS dari nol. Sumber salinan paling mutakhir: `article-057/index.html`.
   Ini keputusan sadar — menyalin file yang terbukti tayang jauh lebih aman
   daripada menyusun ulang `<style>` dan berisiko salah ketik.

4. **Kartu artikel baru selalu disisipkan paling atas** grid `id="articlesGrid"`,
   sebelum kartu lain.

5. **`id="articleCount"` dinaikkan manual** setiap artikel internal baru.
   Nilai sekarang: **53 artikel**.

6. **Angka `articleCount` sengaja tidak sama dengan jumlah kartu.** Folder
   artikel internal = 53, kartu di `index.html` = 62. Selisih ±9 adalah kartu
   yang menautkan ke media luar (mis. liputan Trastuzumab/CISC, kasus dokter
   koas). **Ini bukan bug.** `articleCount` mengikuti jumlah artikel internal.

7. **`git add -A` tidak dipakai saat publish manual.** Gunakan penambahan
   spesifik (`git add index.html article-0XX/`) supaya file nyasar tidak ikut
   ter-commit. Ini menyimpang dari instruksi lama yang menyebut `git add -A`,
   dan penyimpangan ini disengaja.

8. **File `test.txt` sudah dihapus** dari root repo (25 Juli 2026). File nyasar,
   tidak pernah masuk git.

9. **Naskah kiriman tokoh memakai byline penulis asli,** bukan "Redaksi Berita
   HIFDI". Contoh article-057: byline `Zaenal Abidin`, peran
   `Ketua Umum PB Ikatan Dokter Indonesia (IDI) 2012-2015; Ketua Himpunan
   Fasyankes Dokter Indonesia (HIFDI)`. Kolom `.card-meta` di portal juga
   memakai nama penulis, bukan "Redaksi Berita HIFDI".

10. **Gelar tidak ditambahkan sendiri.** Byline article-057 ditulis
    "Zaenal Abidin" tanpa "dr." karena naskah sumber tidak mencantumkannya.
    Kalau mau ditambah, harus atas konfirmasi pemilik repo.

---

## 4) Konteks & Infrastruktur

### Repo
- **Lokasi lokal:** `C:\OneDrive\Documents\GitHub\berita-hifdi`
- **Remote:** `https://github.com/pp-hifdi/berita-hifdi.git`
- **Branch kerja:** `main` (push langsung, tanpa PR)
- Repo berada di dalam OneDrive — ada kemungkinan konflik sinkronisasi.
  Kalau muncul file aneh di root, curigai OneDrive.

### Struktur berkas
```
berita-hifdi/
├─ index.html                  ← portal, grid kartu + articleCount
├─ 404.html
├─ CLAUDE.md                   ← dokumen ini
├─ images/
│   ├─ logo-hifdi.png          ← dipakai header tiap artikel (../images/logo-hifdi.png)
│   └─ hero-hifdi.jpg          ← hero portal
├─ .github/workflows/
│   └─ daily-generate.yml      ← BOT OTOMATIS — RUSAK, lihat bagian 7
└─ article-005/ … article-057/
    └─ index.html
```

### Domain
- Situs utama organisasi: `https://hifdi.id`
- Akademi: `https://academy.hifdi.id`
- **Portal berita: `berita.hifdi.id` — BELUM DIKONFIRMASI.** Alamat ini dipakai
  di caption distribusi tapi tidak pernah divalidasi ke pemilik repo. Tidak ada
  berkas `CNAME` di repo, jadi domain diatur di luar (dashboard Cloudflare).
  **Konfirmasi dulu sebelum menyebarkan tautan.**

### Deploy
- **Cloudflare Pages**, terhubung otomatis ke branch `main`.
  Bukti: commit `adc7a85 trigger: retry cloudflare build`.
- Push ke `main` memicu build otomatis. **Jeda 1–2 menit** sebelum perubahan
  terlihat.
- Build Cloudflare **pernah gagal/tersendat** sampai perlu commit kosong untuk
  memicu ulang. Kalau perubahan tak muncul setelah beberapa menit, periksa
  dashboard Cloudflare Pages sebelum menyalahkan kode.
- Tidak ada `CNAME`, tidak ada GitHub Pages. Jangan mengaktifkan GitHub Pages.

### Cara publish (urutan baku)
```bash
cd "C:\OneDrive\Documents\GitHub\berita-hifdi"

# 1. buat folder + file artikel
#    (salin struktur dari article-057/index.html)

# 2. sisipkan kartu paling atas grid di index.html
# 3. naikkan angka id="articleCount"

# 4. commit spesifik — JANGAN git add -A
git add index.html article-0XX/
git commit -m "publish: article-0XX/index.html"
git push
```

**Verifikasi setelah push:**
```bash
git status -sb        # harus "## main...origin/main" tanpa tanda ahead
git log --oneline -2
```

Catatan: `git push` di PowerShell dengan `2>&1` bisa memunculkan
`NativeCommandError` dan exit code 1 **padahal push berhasil**. Git menulis
progres ke stderr dan PowerShell menganggapnya error. **Patokan keberhasilan
adalah baris `<hash-lama>..<hash-baru>  main -> main`**, bukan exit code.

---

## 5) Pekerjaan Berjalan

### Sudah selesai & tayang

**article-056 — Advokasi — 21 Juli 2026**
- Judul: *Proyek IHSS Rp65 Triliun Kembali Buka Rekrutmen: Penguatan Sistem
  Kesehatan yang Melewati FKTP Swasta*
- Byline: Redaksi Berita HIFDI
- Pemicu: rekrutmen konsultan Kemenkes lewat IHSS Project, tayang 20 Juli 2026.
- Sudut: proyek Rp65 triliun (pinjaman Bank Dunia + MDB) lewat komponen
  SOPHI/SIHREN/InPULS menyasar Puskesmas, RS rujukan, dan lab publik —
  klinik pratama & TPMD swasta di luar skema.
- Tiga tuntutan: buka pelatihan IHSS untuk FKTP swasta; instrumen fiskal
  terpisah untuk peremajaan alat; pelibatan organisasi fasyankes dalam tata
  kelola & evaluasi.
- Gambar: `photo-1519494026892-80bbd2d6fd0d` (ID sama dengan article-015,
  terbukti tampil).
- Commit: `15c8a08`.

**article-057 — Advokasi — 23 Juli 2026**
- Judul: *Balita Wasting: Darurat yang Tersembunyi di Balik Bayang-Bayang
  Stunting*
- Byline: **Zaenal Abidin** (Ketua Umum PB IDI 2012-2015; Ketua HIFDI)
- Naskah kiriman, dimuat utuh (±1.100 kata). Struktur asli dipertahankan:
  8 rekomendasi kebijakan bernomor + "Catatan Akhir sebagai Kesimpulan".
- Data inti: prevalensi wasting naik 7,7% → 8,5% (SKI 2023); 1 dari 5 kematian
  balita dunia diatributkan pada wasting berat (UNICEF); NTT, Maluku,
  Sulteng tertinggi.
- Gambar: `photo-1488521787991-ed7bbaae773c` (ID sama dengan article-051).
- Commit: `5e1cdeb`, lalu perbaikan gambar `61f43f6`.

### Status repo saat serah-terima
- `main` sinkron dengan `origin/main`.
- Working tree bersih (kecuali `CLAUDE.md` ini, belum di-commit).
- Commit terakhir: `61f43f6 fix: ganti gambar article-057 dengan URL Unsplash yang valid`.

### Belum dikerjakan
- **article-058 belum dibuat.** Topik belum ditentukan.
- Verifikasi visual article-057 setelah perbaikan gambar terakhir belum
  dikonfirmasi pemilik repo.

### Topik yang sudah terpakai (jangan diulang)
Periksa selalu `index.html` sebelum memilih topik. Yang muncul di sesi terakhir
antara lain: defisit JKN, redistribusi JKN, formularium obat, RME/SATUSEHAT,
akreditasi FKTP, alkes FKTP, nakes daerah terpencil, IHSS (056), wasting
balita (057). Ini bukan daftar lengkap — **wajib baca `index.html`**.

Perintah cepat melihat seluruh judul terpakai:
```powershell
Select-String -Path index.html -Pattern '<div class="card-title">(.+)</div>' |
  ForEach-Object { $_.Matches[0].Groups[1].Value }
```

---

## 6) Alur Distribusi

Setelah artikel tayang, pemilik repo menyebarkannya lewat **Grup WhatsApp**.
Claude diminta membuatkan caption.

### Format caption WAG
- Judul dibungkus `*bold*` (format WhatsApp, bukan markdown `**`).
- 2–4 paragraf pendek, dipisah baris kosong — WhatsApp tidak nyaman untuk
  blok panjang.
- Sertakan angka kunci; boleh pakai penanda 📌 untuk daftar poin.
- Tutup dengan tautan artikel di baris sendiri.
- Boleh ditutup penanda kanal: `_Berita HIFDI — Himpunan Fasyankes Dokter Indonesia_`

### Sediakan 3 varian
1. **Formal organisasi** — untuk grup pengurus/resmi.
2. **Ringkas & tajam** — untuk grup umum atau broadcast luas.
3. **Pengantar personal** — dibuka salam Islam lengkap
   ("Assalamu'alaikum warahmatullahi wabarakatuh"), untuk dikirim langsung
   oleh pemilik repo ke grup senior/tokoh. Nada takzim, sebut tokoh dengan
   "Bapak".

### Pola tautan
`https://berita.hifdi.id/article-0XX/` — **domain masih perlu dikonfirmasi**
(lihat bagian 4).

---

## 6b) Distribusi Otomatis via OpenWA (loop tertutup)

Grup **HIFDI Bangkit** (grup admin/pengurus HIFDI) boleh dikirimi caption secara
otomatis oleh Claude Code — varian **formal/ringkas**. Grup senior/tokoh dan
varian **personal** (salam Islam, "Bapak") TETAP dikirim manual oleh pemilik repo.

**Gateway:** OpenWA lokal di Docker, `http://localhost:2785`. Shell Claude Code
jalan di mesin lokal, jadi bisa nyapa localhost langsung (sama seperti `git push`).

**Prasyarat sebelum kirim:**
- Docker Desktop nyala + container `openwa-api` Up (`docker ps`).
- Session `berita-wa` `status: ready` (cek via API sessions).
- **Domain `berita.hifdi.id` sudah dikonfirmasi (A2).** Caption memuat link
  artikel; jangan auto-kirim link yang belum divalidasi ke grup HIFDI.

**Kredensial ada di file terpisah `wa-config.local.ps1`** (gitignored, JANGAN
commit). Muat dulu sebelum kirim.

**Grup tujuan:** HIFDI Bangkit -> `120363248843357431@g.us`

**Perintah kirim (PowerShell) — WAJIB begini, JANGAN kirim `$b` sebagai string biasa:**
```powershell
. .\wa-config.local.ps1   # muat kredensial OpenWA (file gitignored)
$captionText = [System.IO.File]::ReadAllText("path\ke\caption.txt")   # BUKAN Get-Content -Raw (lihat catatan A)
$h = @{ "X-API-Key"=$OPENWA_KEY; "Content-Type"="application/json; charset=utf-8" }
$bStr = @{ chatId=$HIFDI_GROUP; text=$captionText } | ConvertTo-Json
$bBytes = [System.Text.Encoding]::UTF8.GetBytes($bStr)   # BUKAN kirim $bStr langsung (lihat catatan B)
Invoke-RestMethod -Uri "$OPENWA_URL/api/sessions/$OPENWA_SESSION/messages/send-text" -Method Post -Headers $h -Body $bBytes
```

**Catatan A — bug `[object Object]`:** `Get-Content -Raw` membungkus hasilnya
dengan metadata (PSPath dll), sehingga `ConvertTo-Json` menganggapnya objek,
bukan string murni — hasilnya field `text` di WA berbunyi literal
`[object Object]`. Pakai `[System.IO.File]::ReadAllText(...)` yang
mengembalikan string murni .NET.

**Catatan B — bug emoji jadi `??`:** `Invoke-RestMethod -Body <string>` di
PowerShell 5.1 meng-encode body dengan encoding default sistem (bukan UTF-8)
saat mengubah string ke bytes, sehingga karakter multi-byte (emoji, kadang
em dash/curly quote) berubah jadi `?`. Sudah diverifikasi lewat tes nyata:
kirim ke endpoint echo, `📌🔥✅` berubah jadi `?????` dengan `-Body $bStr`
(string), tapi utuh dengan `-Body $bBytes` (byte array UTF-8 eksplisit).
**Selalu konversi ke bytes UTF-8 eksplisit sebelum kirim**, jangan kirim
string JSON apa adanya.

**Verifikasi:** respons berisi `id`/`timestamp` tanpa error = terkirim. Cek juga
pesan nongol di grup HIFDI Bangkit — dan kalau ada emoji, pastikan tidak
berubah jadi `?`.

**Safe-send:** OpenWA unofficial, ada risiko ban. Nomor gateway = nomor buangan
(62895615779993). Kirim ke satu grup HIFDI Bangkit per artikel; jangan blast
banyak grup sekaligus.

---

## 6c) Publish via Bridge Telegram (headless, mandiri)

Sejak 31 Juli 2026 ada jalur publish tanpa membuka Claude Code langsung:

```
Chat topik ke bot Telegram HIFDI (t.me/HIFDI_BOT)
  -> Bridge Node (C:\Users\Admin\berita-bridge\bridge.js) nangkep pesan
  -> jalankan `claude -p` headless di folder repo ini
     (baca CLAUDE.md ini -> riset -> tulis artikel -> publish)
  -> Claude tulis caption final ke wa-caption.txt (root repo, UTF-8, teks murni)
  -> Bridge yang BACA file itu & KIRIM ke grup WhatsApp HIFDI Bangkit
  -> bot Telegram balas laporan + status kirim WA
```

**Mode perintah di Telegram:**
- Kirim topik biasa = publish penuh (tulis + commit + push + caption).
- Awali pesan dengan `draft:` = tulis draft saja, **tanpa publish, tanpa WA**.

**Perbedaan alur caption dari bagian 6b:**
- **Sesi headless (lewat bridge Telegram):** Claude **TIDAK** memanggil OpenWA API
  sendiri. Setelah artikel tayang & terverifikasi live, Claude menulis caption
  final ke file `wa-caption.txt` di root repo. Bridge yang membaca file itu dan
  mengirim ke WhatsApp. Ini mencegah bug `[object Object]` (PowerShell/Node
  serialization) dan emoji rusak `??` (encoding) yang pernah terjadi saat
  Claude kirim langsung.
- **Sesi interaktif (kerja langsung di Claude Code seperti biasa):** tetap
  ikuti alur 6b — Claude boleh memanggil OpenWA API langsung untuk kirim
  formal/ringkas ke HIFDI Bangkit.
- `wa-caption.txt` masuk `.gitignore` — jangan sampai ter-commit.

**Aturan gambar (berlaku di kedua alur, headless maupun interaktif):**
Gambar **wajib cocok kata kunci judul artikel**, bukan asal "aman tayang".
Kasus nyata yang jadi pelajaran: artikel tentang naik gunung sempat dapat foto
yoga karena ID Unsplash dipilih tanpa mengecek subjek fotonya. Prosedur:
1. Ekstrak kata kunci utama dari judul.
2. Cocokkan dengan **alt text** gambar-gambar lama di `index.html` (lihat
   bagian 7 soal Unsplash) — cari yang temanya benar-benar nyambung, bukan
   sekadar "gambar kesehatan generik".
3. Kalau tidak ada yang cocok, unduh foto yang sesuai dari sumber yang bisa
   diverifikasi (Wikimedia Commons, Pexels) dan **host lokal** di `images/`
   alih-alih hotlink Unsplash yang temanya dipaksakan.
4. Tetap verifikasi visual sebelum commit — jangan percaya alt text lama
   begitu saja (lihat catatan di bagian 7 soal alt text yang ternyata salah).

**Aturan koordinasi — WAJIB dibaca sebelum publish manual:**
**Satu penerbit per portal dalam satu waktu.** Jangan jalankan publish manual
di sesi interaktif ini bersamaan dengan bridge Telegram sedang memproses
permintaan lain — nomor `article-0XX` bisa bentrok (dua proses menghitung
nomor folder tertinggi secara bersamaan). Kalau ragu apakah bridge sedang
jalan, cek proses Node di mesin lokal atau tanya pemilik repo dulu sebelum
mulai publish.

**Status push non-interaktif (prasyarat bridge headless berfungsi):**
`claude -p` headless **tidak bisa** menjawab popup login Git Credential
Manager, sehingga `git push` dari proses headless akan gagal (401 lalu hang
tanpa timeout jelas — lihat kasus nyata di sesi 29-31 Juli 2026 di mana push
macet total sampai re-auth GCM manual di sesi interaktif). Solusinya: pasang
Personal Access Token (PAT) GitHub di remote URL lokal
(`git remote set-url origin https://x-access-token:TOKEN@github.com/...`).

**Claude TIDAK BOLEH menjalankan perintah ini sendiri** — memasukkan API
key/token ke command apa pun (termasuk git remote URL) adalah tindakan yang
harus dilakukan pemilik repo sendiri, bukan diketikkan/dieksekusi oleh Claude,
walau pemilik repo memberikan tokennya langsung di chat. Kalau status PAT ini
belum jelas, cek `git remote -v` — kalau URL masih polos tanpa token, berarti
publish via bridge headless **masih akan gagal push** dan perlu ditangani
pemilik repo di sesi interaktif dulu.

---

## 7) Hal yang Mudah Terlupa

Bagian ini lahir dari kesalahan nyata di sesi sebelumnya. Baca sebelum
mengerjakan apa pun.

### ⚠️ Bot otomatis harian sedang RUSAK
`.github/workflows/daily-generate.yml` berjalan **dua kali sehari**
(cron `0 23 * * *` dan `0 11 * * *` UTC = 06.00 dan 18.00 WIB). Skrip yang
dipanggil adalah `scripts/generate_article.py` — **folder `scripts/` tidak ada
di repo.** Artinya workflow ini gagal setiap kali jalan.

Implikasi yang harus disadari:
- Ada notifikasi kegagalan GitHub Actions dua kali sehari.
- Bot memakai `git add -A` dan commit `"auto: artikel baru"` sebagai
  **HIFDI Bot <bot@hifdi.id>**. Kalau skrip dipulihkan, bot bisa menyapu file
  nyasar dan **bertabrakan dengan penomoran artikel manual**.
- Bot pernah berhasil sekali: commit `1bc249d` (22 Juni 2026), membuat
  article-025 dan article-026.
- **Keputusan soal bot ini belum diambil.** Jangan diam-diam menghidupkan,
  menghapus, atau menambal workflow tanpa persetujuan pemilik repo.

### ⚠️ URL gambar Unsplash — kesalahan yang paling mahal di sesi lalu
**ID foto Unsplash itu string acak dan mustahil ditebak.** Di sesi sebelumnya
ID dikarang dari ingatan, hasilnya gambar 404 dan harus diperbaiki dua kali.

Aturan:
1. **Jangan pernah menulis ID Unsplash dari ingatan.**
2. Ambil ID **hanya** dari artikel lama di repo yang gambarnya terbukti tampil.
   Cara mengumpulkannya:
   ```powershell
   Select-String -Path index.html -Pattern 'images\.unsplash\.com/(photo-[a-z0-9\-]+)' |
     ForEach-Object { $_.Matches[0].Groups[1].Value } | Sort-Object -Unique
   ```
3. Format parameter yang dipakai di repo:
   `?auto=format&fit=crop&w=1200&q=80` (og:image & featured-image)
   `?auto=format&fit=crop&w=800&q=80` (kartu portal)
4. **Boleh memakai ulang ID yang sudah dipakai artikel lain.** Sudah jadi
   praktik di repo ini (015 & 056 berbagi ID; 051 & 057 berbagi ID). Lebih baik
   gambar berulang daripada gambar mati.
5. **`alt` harus menggambarkan isi foto sebenarnya**, bukan tema artikel.

### ⚠️ curl TIDAK bisa dipakai memverifikasi gambar Unsplash
`images.unsplash.com` membalas **404 untuk semua permintaan curl**, termasuk
URL yang jelas-jelas hidup di browser. Ini proteksi hotlink/User-Agent, bukan
bukti gambar rusak.

Kesalahan yang pernah terjadi: hasil 404 seragam dari curl dipakai sebagai
bukti, lalu gambar yang sebenarnya sehat ikut "diperbaiki". **Kalau sebuah alat
memberi hasil negatif seragam untuk semua masukan, curigai alatnya, bukan
datanya.** Verifikasi gambar lewat browser sungguhan.

### ⚠️ Jangan batalkan temuan berbasis bukti karena sinyal yang belum diperiksa
Pernah terjadi: diagnosis yang benar (ID 057 memang palsu) dibatalkan hanya
karena pemilik repo berkata "kayaknya udah bener" — padahal perbaikannya
belum di-push, sehingga mustahil berkaitan. Akibatnya pekerjaan terulang dua
kali. Periksa dulu apakah sinyal baru itu masuk akal secara logika.

### ⚠️ Gambar hilang ≠ URL rusak
Gejala "gambar tidak muncul" tepat setelah push paling sering berarti
**build Cloudflare belum selesai atau cache browser**. Urutan pemeriksaan:
1. Tunggu 1–2 menit, hard-refresh (Ctrl+Shift+R).
2. Cek dashboard Cloudflare Pages — apakah build sukses.
3. Baru periksa URL gambarnya.

### ⚠️ MCP Desktop Commander sering timeout
Di sesi sebelumnya server MCP berkali-kali berhenti merespons >4 menit,
terutama saat menulis file besar. Mitigasi:
- **Tulis file dalam potongan ≤30 baris**, jangan sekali tulis besar.
- Setelah timeout, **periksa dulu keadaan file** sebelum menulis ulang —
  tulisan sebelumnya bisa jadi sudah berhasil sebagian.
- Kalau macet, minta pemilik repo me-restart Claude Desktop.

Di Claude Code masalah ini kemungkinan besar hilang karena akses berkas
langsung, tanpa MCP.

### ⚠️ Hal kecil yang sering luput
- `data-category` di kartu portal **huruf kecil dan pakai strip**:
  `kabar-hifdi`, bukan `Kabar HIFDI`.
- Judul di kartu portal harus **sama persis** dengan `<h1>` di artikel.
- Logo di header artikel memakai path relatif `../images/logo-hifdi.png` —
  benar karena artikel berada satu tingkat di dalam.
- Tautan "Kembali ke Portal" memakai `../`.
- Setiap artikel punya **dua** tempat URL gambar: `og:image` dan
  `.featured-image`. Kalau mengganti gambar, **ganti keduanya** — plus satu
  lagi di kartu `index.html`. Total **3 titik**.
- Git memunculkan peringatan `LF will be replaced by CRLF`. Normal di Windows,
  abaikan.

---

## Action Item yang Belum Selesai

Diurutkan berdasarkan mendesaknya. Nomor 1–3 perlu keputusan pemilik repo,
bukan keputusan Claude.

### Perlu keputusan pemilik repo

**A1 — Tentukan nasib bot harian yang rusak.** `daily-generate.yml` gagal dua
kali sehari karena `scripts/generate_article.py` tidak ada. Pilihannya:
(a) pulihkan skripnya, (b) nonaktifkan workflow, (c) hapus workflow.
Risiko bila dipulihkan tanpa penyesuaian: bot memakai `git add -A` dan bisa
bertabrakan dengan penomoran artikel manual. **Jangan bertindak tanpa arahan.**

**A2 — Konfirmasi domain portal berita.** `berita.hifdi.id` dipakai di caption
distribusi tapi belum pernah divalidasi. Tidak ada `CNAME` di repo. Pastikan
alamat yang benar sebelum tautan disebar lebih luas.

**A2b — Pasang PAT GitHub agar bridge Telegram headless bisa push.** Lihat
bagian 6c. Tanpa ini, publish lewat bot Telegram akan macet di tahap
`git push` (401, lalu hang). Owner perlu generate PAT di
github.com/settings/tokens (scope `repo`) lalu jalankan `git remote set-url`
sendiri di sesi interaktif — Claude tidak boleh menjalankan perintah ini
sendiri karena melibatkan token/API key.

**A3 — Putuskan penulisan gelar untuk Zaenal Abidin.** Byline article-057 kini
"Zaenal Abidin" tanpa "dr.". Kalau gelar perlu ditambahkan, harus diperbaiki di
dua tempat: `.byline-name` di `article-057/index.html` dan `.card-meta` di
`index.html`.

### Perlu verifikasi

**A4 — Pastikan gambar article-057 sudah tampil.** Perbaikan terakhir
(`61f43f6`) mengganti ID gambar ke `photo-1488521787991-ed7bbaae773c`. Pemilik
repo belum mengonfirmasi hasilnya. Cek `berita.hifdi.id/article-057/` dan kartu
di portal. Kalau masih kosong, penyebabnya bukan ID — periksa build Cloudflare.

**A5 — Periksa riwayat kegagalan GitHub Actions.** Lihat berapa lama bot sudah
gagal dan apakah ada notifikasi menumpuk.

### Pekerjaan rutin berikutnya

**A6 — Tulis article-058.** Topik belum ditentukan. Alur: riset topik aktual
lewat web search → periksa `index.html` agar tidak mengulang → pilih kategori →
tulis → publish → buatkan caption WAG.

**A7 — Commit `CLAUDE.md` ini.** Berkas ini baru dibuat dan **belum masuk git**.
Kalau disetujui:
```bash
git add CLAUDE.md
git commit -m "docs: tambah CLAUDE.md sebagai panduan kerja repo"
git push
```

### Utang teknis (tidak mendesak)

**A8 — Rapikan selisih `articleCount` vs jumlah kartu.** Saat ini 53 vs 62.
Selisihnya disengaja (kartu tautan luar), tapi belum ada penanda di kode yang
menjelaskannya. Menambahkan komentar HTML di sekitar kelompok kartu eksternal
akan mencegah salah paham di masa depan.

**A9 — Pertimbangkan meng-host gambar sendiri.** Ketergantungan pada Unsplash
sudah dua kali menimbulkan masalah. Menaruh gambar di `images/` menghilangkan
risiko hotlink, ID salah, dan perubahan kebijakan pihak ketiga.

---

## Ringkasan Satu Layar

| Butir | Nilai |
|---|---|
| Repo | `C:\OneDrive\Documents\GitHub\berita-hifdi` |
| Remote | `github.com/pp-hifdi/berita-hifdi` (branch `main`) |
| Deploy | Cloudflare Pages, otomatis dari `main`, jeda 1–2 menit |
| Artikel terakhir | **article-057** (23 Juli 2026, Advokasi) |
| Artikel berikutnya | **article-058** |
| Folder artikel | 53 (article-005 … article-057) |
| `articleCount` | 53 |
| Kartu di portal | 62 (selisih = tautan media luar, bukan bug) |
| Commit terakhir | `61f43f6` |
| Kategori | Advokasi / Edukasi / Mutu / Kabar HIFDI |
| Panjang artikel | ±500 kata (naskah tokoh boleh lebih, muat utuh) |
| Template | salin `article-057/index.html` |
| Titik URL gambar | 3 (og:image, featured-image, kartu portal) |
| Peringatan utama | bot harian rusak; jangan karang ID Unsplash; curl tak bisa uji gambar |
