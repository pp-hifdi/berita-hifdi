# -*- coding: utf-8 -*-
"""
Konfigurasi bot harian Berita HIFDI.
Dipisah dari generate_article.py supaya gampang disetel tanpa menyentuh logika.

SEMUA URL FEED DI SINI SUDAH DIUJI HIDUP (3 Agustus 2026).
Jangan menambah feed tanpa mengujinya dulu:
    curl -s -o /tmp/f.xml -w "%{http_code}" -A "Mozilla/5.0" "<URL>" && grep -c "<item" /tmp/f.xml
Feed yang 403/404/kosong akan diam-diam mengurangi kolam kandidat.
"""

# ---------------------------------------------------------------------------
# SUMBER RSS — grounding fakta. Bot TIDAK pernah menulis dari ingatan model;
# ia selalu berangkat dari berita nyata di salah satu feed ini, dan URL asli
# feed itulah yang masuk ke kotak Referensi.
# ---------------------------------------------------------------------------
FEEDS = [
    # --- Indonesia ---
    ("Detik Health",      "https://health.detik.com/rss"),
    ("CNN Indonesia",     "https://www.cnnindonesia.com/gaya-hidup/rss"),
    ("ANTARA News",       "https://www.antaranews.com/rss/terkini.xml"),
    ("Republika",         "https://www.republika.co.id/rss"),
    # --- Internasional ---
    ("WHO",               "https://www.who.int/rss-feeds/news-english.xml"),
    ("Medical Xpress",    "https://medicalxpress.com/rss-feed/"),
    ("Fierce Healthcare", "https://www.fiercehealthcare.com/rss/xml"),
    ("STAT News",         "https://www.statnews.com/feed/"),
    ("Health Affairs",    "https://www.healthaffairs.org/action/showFeed?type=etoc&feed=rss&jc=hlthaff"),
    ("KFF Health News",   "https://kffhealthnews.org/feed/"),
    # --- Google News RSS (restu Sekjen 3 Agu 2026) ---
    # TAHAP 1 (3 feed inti, dipantau 2 hari sebelum 13 sisanya menyusul).
    # Catatan Sekjen: query pencarian pakai frasa penuh, bukan singkatan.
    ("GN: AI kesehatan",  "https://news.google.com/rss/search?q=AI+kesehatan&hl=id&gl=ID&ceid=ID:id"),
    ("GN: health financing", "https://news.google.com/rss/search?q=health+financing&hl=en-US&gl=US&ceid=US:en"),
    ("GN: telemedicine",  "https://news.google.com/rss/search?q=telemedicine&hl=id&gl=ID&ceid=ID:id"),
]

# ---------------------------------------------------------------------------
# KATA KUNCI RELEVANSI — saringan pertama. Judul feed harus memuat minimal satu
# kata kunci ini, kalau tidak dibuang. Tujuannya: bot tidak menulis soal tips
# diet atau gosip selebriti hanya karena muncul di feed gaya hidup.
# Dicocokkan huruf kecil, substring sederhana.
# ---------------------------------------------------------------------------
#
# BERBOBOT, BUKAN BINER. Pelajaran dari uji coba 3 Agustus 2026: saringan
# "lolos kalau ada satu kata kunci" meloloskan sampah — "Lagi Diet, Masih
# Boleh Makan Mie Instan? Saran Dokter Gizi" lolos hanya karena kata "dokter".
# Kata umum seperti "dokter"/"kesehatan" ada di hampir semua artikel kesehatan
# konsumen, jadi bobotnya harus kecil dan tidak boleh cukup untuk lolos sendiri.
#
KEYWORDS_STRONG = [   # bobot 10 — inti urusan HIFDI, satu saja sudah cukup
    "bpjs", "jkn", "kapitasi", "iuran bpjs", "jaminan kesehatan",
    "fktp", "fasyankes", "klinik pratama", "puskesmas", "posyandu",
    "kemenkes", "kementerian kesehatan", "permenkes", "menteri kesehatan",
    "akreditasi", "satusehat", "rekam medis", "rujukan", "kredensial",
    "layanan primer", "kesehatan primer", "pelayanan kesehatan primer",
    "primary care", "primary health", "primary healthcare",
    "health policy", "health system", "health financing", "health coverage",
    "universal health coverage", "uhc", "accreditation", "patient safety",
    "quality assurance", "quality improvement", "quality of care",
    "health tech", "health technology", "digital health", "telemedicine",
    "telehealth", "electronic health record", "ehr", "health workforce",
    # Restu Sekjen 3 Agu 2026 — arah baru portal (AI kesehatan, telehealth,
    # health financing, GGL, MBG). Catatan Sekjen: "ggl" aman dipakai untuk
    # PENYARINGAN judul (dicek bersama konteks judul), bukan untuk query RSS.
    "ai kesehatan", "kecerdasan buatan", "artificial intelligence",
    "teleradiologi", "telesurgery", "pembiayaan kesehatan",
    "asuransi kesehatan", "ggl", "gula garam lemak", "mbg",
    "makan bergizi gratis",
]

KEYWORDS_MEDIUM = [   # bobot 3 — relevan, tapi perlu teman
    "tenaga kesehatan", "nakes", "apoteker", "bidan", "perawat",
    "rumah sakit", "faskes", "asuransi kesehatan", "telemedisin",
    "cukai", "stunting", "wasting", "gizi buruk", "imunisasi", "vaksin",
    "obat generik", "formularium", "bpom", "puskesos",
    "clinic", "clinical", "hospital", "physician", "nurse", "midwife",
    "public health", "quality of life", "health worker", "health data",
    "vaccination", "immunization", "health equity", "health outcomes",
    # Restu Sekjen 3 Agu 2026 — arah baru portal
    "nutrition", "malnutrition", "health insurance", "ai diagnostics",
]

KEYWORDS_WEAK = [     # bobot 1 — terlalu umum untuk berdiri sendiri
    "dokter", "kesehatan", "health", "medical", "patient", "pasien",
]

# Skor minimum supaya sebuah judul dianggap layak. Diset 10 = harus ada
# minimal satu kata kunci KUAT, atau gabungan beberapa kata kunci sedang.
MIN_SCORE = 10

# Penolak mutlak — penanda artikel kesehatan konsumen / gosip. Kalau salah satu
# muncul di judul, buang berapa pun skornya. Portal ini bukan rubrik gaya hidup.
BLOCKLIST = [
    "diet", "resep", "tips", "trik", "mitos atau fakta", "khasiat",
    "manfaat", "cara mudah", "kata dokter", "saran dokter", "viral",
    "artis", "selebriti", "idol", "drakor", "zodiak", "ramalan",
    "ngidam", "kulit glowing", "awet muda", "diet ketat", "olahraga berat",
    "warganet", "netizen", "bikin kaget", "wajib tahu", "awas",
]

# ---------------------------------------------------------------------------
# GAMBAR TERKURASI — ID Unsplash yang SUDAH DIVERIFIKASI VISUAL (dibuka satu
# per satu di browser, bukan percaya alt text).
#
# KENAPA TIDAK MENCOCOKKAN ALT TEXT OTOMATIS: alt text lama di index.html
# terbukti berbohong. Contoh nyata (Agustus 2026): ID yang alt-nya berbunyi
# "penandatanganan perjanjian kerjasama" ternyata foto model jantung di atas
# buku EKG; ID lain yang alt-nya "dokter memeriksa dokumen perizinan" ternyata
# petugas lab memegang vial. Bot tidak bisa melihat gambar, jadi ia HANYA boleh
# memakai daftar putih ini.
#
# Menambah entri baru: buka https://images.unsplash.com/<ID>?auto=format&fit=crop&w=800&q=80
# di browser sungguhan, lihat fotonya, baru tulis alt yang jujur di sini.
# ---------------------------------------------------------------------------
IMAGES = {
    "rokok": {
        "id": "photo-1572113564617-7230ee196d9a",
        "alt": "Bungkus rokok yang robek tergeletak di aspal",
    },
    "kebijakan": {
        "id": "photo-1576091160550-2173dba999ef",
        "alt": "Tangan mengetik di laptop dengan stetoskop di atas meja",
    },
    "klinis": {
        "id": "photo-1530026186672-2cd00ffc50fe",
        "alt": "Model jantung anatomi di atas buku panduan EKG",
    },
    "laboratorium": {
        "id": "photo-1527613426441-4da17471b66d",
        "alt": "Petugas berjas lab memeriksa sampel dengan alat pelindung diri",
    },
}

# Kategori artikel -> kunci gambar di atas. Dipakai kalau model tidak
# memberi petunjuk yang jelas. "kebijakan" jadi default paling aman karena
# mayoritas artikel portal ini bertema kebijakan/administrasi.
IMAGE_BY_CATEGORY = {
    "Advokasi": "kebijakan",
    "Mutu": "laboratorium",
    "Edukasi": "klinis",
    "Kabar HIFDI": "kebijakan",
}
DEFAULT_IMAGE = "kebijakan"

# ---------------------------------------------------------------------------
# FOTO GILIR (restu Sekjen/Prinsipal 5 Agu 2026) — koleksi 57 foto terkurasi
# di images/foto/cat-XX/ (16 kategori, nomenklatur unit Kemenkes 2026;
# cat-15 = Kemenhaj, cat-16 = Surkarkes). Pemilihan lewat sistem gilir:
#   python3 scripts/pick_photo.py cat-XX    # foto PALING JARANG dipakai
# Pemetaan kategori EDITORIAL -> kode kategori foto yang cocok (urut prioritas;
# daftar lebih dari satu supaya rotasi merata tidak cepat berulang).
#
# CATATAN AUDIT 5 Agu 2026 (lihat docs/HAK-PAKAI-FOTO.md & docs/SOP-FOTO.md):
# - Syarat restu #1 (lisensi): cat-07-001, cat-08-001 (by-nd) & cat-15-001
#   (lisensi tak tercatat) DIKELUARKAN.
# - Syarat restu #2 (netralitas): awalnya 12 foto dikeluarkan; setelah koreksi
#   aturan privasi Prinsipal (wajah tanpa nama = BOLEH), 5 dikembalikan.
#   Yang TETAP keluar (7): cat-01-002 (pasien terekspos), cat-03-002 (anak
#   klinis), cat-05-001 (anak), cat-06-001 (pasien terapi invasif),
#   cat-11-004 (data pasien terbaca), cat-12-001 (nama & data medis terbaca),
#   cat-14-001 (bayi darurat).
# - ATURAN PRIVASI (Prinsipal, 5 Agu 2026): jangan sandingkan wajah bisa
#   dikenali DENGAN nama individu; foto tanpa nama = boleh.
# - Aktif: 47 foto. Barang dikeluarkan ada di images/foto/_ditolak/
#   (ditandai "status": "excluded" di photo_registry.json).
# ---------------------------------------------------------------------------
PHOTO_BY_CATEGORY = {
    "Advokasi": ["cat-10", "cat-11", "cat-16", "cat-14"],
    "Mutu": ["cat-12", "cat-01", "cat-06", "cat-09"],
    "Edukasi": ["cat-13", "cat-01", "cat-05", "cat-08"],
    "Kabar HIFDI": ["cat-11", "cat-10", "cat-16", "cat-02"],
}

# ---------------------------------------------------------------------------
# DeepSeek — OpenAI-compatible. Kunci dibaca dari env DEEPSEEK_API_KEY
# (GitHub Secrets), TIDAK PERNAH ditulis di repo.
# ---------------------------------------------------------------------------
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# ---------------------------------------------------------------------------
# SYSTEM_PROMPT — suara editorial (wilayah Sekjen).
# Dipindahkan dari generate_article.py pada 3 Agu 2026 atas usulan Sekjen:
# penyetelan suara editorial tidak boleh menyentuh berkas mesin. Skrip hanya
# mengimpor konstanta ini. Kalau Sekjen ingin mengubah nada/sikap portal,
# edit bagian ini — bukan generate_article.py.
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """Kamu penulis untuk portal Berita HIFDI (Himpunan Fasyankes Dokter Indonesia).
HIFDI menaungi Fasilitas Kesehatan Tingkat Pertama: klinik pratama, Tempat Praktik
Mandiri Dokter (TPMD), dan puskesmas. Portal ini bukan agregator berita — setiap
artikel WAJIB memuat sikap organisasi.

SUARA EDITORIAL (pegang erat):
- FKTP swasta sistematis terpinggirkan: menanggung porsi besar kepesertaan JKN,
  tapi hampir selalu di luar skema penguatan (APBN, hibah, pengadaan alat).
- Beban setara, dukungan timpang: kontrak dan standar sama dengan fasyankes
  pemerintah, tapi biaya pemenuhannya ditanggung sendiri.
- Layanan primer adalah hulu, bukan pelengkap.
- Berbasis bukti, bukan sentimen. Menuntut, bukan memohon. Tetap konstruktif.

ATURAN KERAS:
- DILARANG mengarang fakta, angka, nama, tanggal, nomor peraturan, atau sumber.
  Kamu HANYA boleh memakai fakta yang ada di berita sumber yang diberikan.
  Kalau sebuah detail tidak ada di sumber, jangan sebut.
- Kalau sumbernya berita luar negeri, tarik relevansinya ke layanan primer
  Indonesia — jangan sekadar menerjemahkan.
- Bahasa Indonesia baku jurnalistik, ±500 kata. Sikap tajam lewat data, bukan
  kata sifat berlebihan.

STRUKTUR BADAN ARTIKEL (HTML, berurutan):
1. <p> pembuka — konteks isu, sebut sumber dan tanggalnya.
2. 2-3 bagian <h2> — uraian isu, data, dampak konkret ke FKTP.
3. Satu <blockquote><p>...</p></blockquote> — satu kalimat sorotan.
4. <h2>Posisi HIFDI</h2> — sikap organisasi (nada mengikuti kategori).
5. <h2>Penutup</h2> — satu paragraf.
Hanya tag <p>, <h2>, <blockquote>, <em>, <strong>. Tanpa <html>/<body>/<div>.
JANGAN tulis kotak Referensi — skrip yang menambahkannya.

KATEGORI dan nada Posisi HIFDI:
- "Advokasi": kebijakan/regulasi berdampak ke FKTP. Tajam. 2-3 tuntutan konkret.
- "Edukasi": literasi medis/panduan klinis. Menjelaskan. 2 poin: yang didukung,
  yang perlu diperbaiki.
- "Mutu": standar layanan, akreditasi, RME/SATUSEHAT. Evaluatif-teknis.
- "Kabar HIFDI": kegiatan organisasi. Hangat.

Balas HANYA JSON valid. SEMUA enam kunci di bawah WAJIB ada dan terisi —
jangan ada yang dikosongkan atau dilewat:
  title            judul artikel (bukan terjemahan mentah judul sumber)
  subtitle         satu kalimat rangkuman
  category         salah satu: Advokasi | Edukasi | Mutu | Kabar HIFDI
  meta_description ringkasan <=200 karakter
  body_html        badan artikel sesuai struktur di atas
  caption          caption WhatsApp: judul dibungkus *bold*, 2-3 paragraf
                   pendek, tanpa menyertakan link (skrip yang menambahkan)

Tulis "caption" PALING AKHIR, setelah body_html selesai. Jangan berhenti
sebelum caption terisi.
"""

# Batas aman
MAX_SOURCE_CHARS = 6000   # potong isi berita sumber sebelum dikirim ke model
MIN_TITLE_WORDS = 4       # judul feed terlalu pendek biasanya bukan berita utuh
