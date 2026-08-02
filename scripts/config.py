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
]

KEYWORDS_MEDIUM = [   # bobot 3 — relevan, tapi perlu teman
    "tenaga kesehatan", "nakes", "apoteker", "bidan", "perawat",
    "rumah sakit", "faskes", "asuransi kesehatan", "telemedisin",
    "cukai", "stunting", "wasting", "gizi buruk", "imunisasi", "vaksin",
    "obat generik", "formularium", "bpom", "puskesos",
    "clinic", "clinical", "hospital", "physician", "nurse", "midwife",
    "public health", "quality of life", "health worker", "health data",
    "vaccination", "immunization", "health equity", "health outcomes",
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
# DeepSeek — OpenAI-compatible. Kunci dibaca dari env DEEPSEEK_API_KEY
# (GitHub Secrets), TIDAK PERNAH ditulis di repo.
# ---------------------------------------------------------------------------
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# Batas aman
MAX_SOURCE_CHARS = 6000   # potong isi berita sumber sebelum dikirim ke model
MIN_TITLE_WORDS = 4       # judul feed terlalu pendek biasanya bukan berita utuh
