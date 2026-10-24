#!/usr/bin/env python3
"""Bangun article-109: ucapan HUT IDI ke-76 / Hari Dokter Nasional 2026.

Menyalin kerangka article-108 (template tayang, sudah memuat komponen galeri
fig-gallery), lalu mengganti meta, JSON-LD, dan isi badan artikel.
"""
import json
import pathlib
import re

REPO = pathlib.Path("/home/hermes/workspace/berita-hifdi")
SRC = REPO / "article-108/index.html"
DEST = REPO / "article-109/index.html"

TITLE = "76 Tahun IDI, HIFDI Soroti Tiga Pekerjaan Rumah di Layanan Primer"
DESC = ("HIFDI mengucapkan selamat HUT ke-76 IDI dan Hari Dokter Nasional 24 Oktober 2026, "
        "sekaligus menyoroti tiga pekerjaan rumah organisasi profesi di layanan primer.")
IMAGE = "https://berita.hifdi.id/images/article-109-idi76-hero.jpg"
URL = "https://berita.hifdi.id/article-109/"
CAT = "Kabar HIFDI"
DATE_HUMAN = "24 Oktober 2026"

BODY = """<span class="article-category">Kabar HIFDI</span>
<h1 class="article-title">76 Tahun IDI, HIFDI Soroti Tiga Pekerjaan Rumah di Layanan Primer</h1>
<div class="article-subtitle">&ldquo;Bagi IDI, ini berarti berani keluar dari menara gading klinis dan menerjemahkan temuan ilmu kedokteran yang teknis ke dalam bahasa anggaran serta kebijakan publik, tanpa kehilangan independensi ilmiah.&rdquo;</div>
<div class="article-meta">
<span>24 Oktober 2026</span>
<span>Kabar HIFDI</span>
</div>
<img class="featured-image" src="../images/article-109-idi76-hero.jpg" alt="Kartu ucapan HUT IDI ke-76 dan Hari Dokter Nasional dari HIFDI, dengan logo IDI dan kutipan Ketua Umum HIFDI.">
<p class="featured-caption">Ucapan HUT IDI ke-76 dan Hari Dokter Nasional dari Himpunan Fasyankes Dokter Indonesia (HIFDI), 24 Oktober 2026. Desain: Berita HIFDI.</p>
<div class="byline">
<div class="byline-name">Redaksi Berita HIFDI</div>
<div class="byline-roles">Ucapan HUT ke-76 IDI dan Hari Dokter Nasional, 24 Oktober 2026</div>
</div>
<div class="article-body">
<p><strong>JAKARTA, 24 OKTOBER 2026.</strong> Ikatan Dokter Indonesia (IDI) genap berusia 76 tahun pada 24 Oktober 2026. Tanggal yang sama diperingati sebagai Hari Dokter Nasional, karena pada 24 Oktober 1950 IDI disahkan di hadapan notaris setelah muktamar pertamanya. Himpunan Fasyankes Dokter Indonesia (HIFDI) menyampaikan ucapan selamat dan mengangkat tema peringatan tahun ini, &ldquo;IDI Berkemajuan Berbakti untuk Bangsa&rdquo;.</p>

<p>Bagi HIFDI, usia 76 tahun bukan hanya soal bertambahnya umur lembaga profesi dokter di Indonesia. Ini soal apakah organisasi profesi masih bisa menjangkau tempat pasien pertama kali berobat, yaitu klinik pratama, tempat praktik mandiri dokter, dan puskesmas.</p>

<blockquote><p>&ldquo;Bagi IDI, ini berarti berani keluar dari menara gading klinis dan menerjemahkan temuan ilmu kedokteran yang teknis ke dalam bahasa anggaran serta kebijakan publik, tanpa kehilangan independensi ilmiah yang menjadi sumber kredibilitasnya.&rdquo;</p><p><strong>dr. Zaenal Abidin, M.H.</strong><br>Ketua Umum HIFDI</p></blockquote>

<h2>Tiga pekerjaan rumah yang disebut sendiri oleh IDI</h2>

<p>Dalam kolomnya di Pinisi.co.id, &ldquo;IDI Tetaplah Menyala dan Menjadi Suluh Bangsa&rdquo;, Zaenal Abidin yang juga Ketua Umum PB IDI 2012-2015 menyebut tiga hal yang harus dikerjakan organisasi profesi.</p>

<p>Pertama, menjaga etik ketika layanan kesehatan makin diperlakukan sebagai komoditas. Penegakan Kode Etik Kedokteran Indonesia (KODEKI) dinilai perlu berubah dari sistem yang menunggu aduan menjadi sistem yang mencegah, salah satunya dengan memasukkan literasi hukum kesehatan dan bioetika ke program pengembangan pendidikan keprofesian berkelanjutan (P2KB).</p>

<p>Kedua, memimpin riset yang menjawab masalah dalam negeri. Stunting, tuberkulosis, dan ketimpangan fasilitas antardaerah disebut tidak selesai oleh teknologi kedokteran tercanggih sekalipun, sehingga dokter Indonesia perlu menjadi produsen ilmu, bukan hanya pengguna teknologi dari luar.</p>

<p>Ketiga, soal pemerataan tenaga medis. Dalam kolom itu, Kementerian Kesehatan diminta tidak memposisikan organisasi profesi sebagai lawan dalam urusan regulasi, dan IDI perlu dilibatkan setara dalam penyusunan rancangan perlindungan profesi serta insentif dokter di wilayah terdepan, terluar, dan tertinggal.</p>

<h2>Titik temu dengan fasyankes primer</h2>

<p>Ketiga pekerjaan rumah itu bertemu di satu tempat: fasilitas pelayanan kesehatan tingkat pertama. Dokter di klinik pratama dan puskesmas adalah yang pertama menemui pasien, yang memutuskan apakah kasus cukup ditangani di tempat atau harus dirujuk, dan yang menanggung konsekuensi bila standar etik serta mutu tidak terjaga.</p>

<figure class="fig-gallery" data-gallery>
  <div class="fg-stage">
    <div class="fg-main">
      <div class="fg-slide">
        <img src="../images/article-109-idi76-klinik.jpg" alt="Ilustrasi digital HIFDI: dokter mendengarkan keluhan pasien lansia di klinik pratama, sementara ibu muda menunggu dengan anaknya." loading="eager">
        <div class="fg-cap">Ilustrasi digital HIFDI: dokter mendengarkan keluhan pasien lansia di klinik pratama, sementara ibu muda menunggu bersama anaknya.</div>
      </div>
      <div class="fg-slide">
        <img src="../images/article-109-idi76-posyandu.jpg" alt="Ilustrasi digital HIFDI: dokter memeriksa balita di posyandu didampingi ibunya dan seorang bidan." loading="lazy">
        <div class="fg-cap">Ilustrasi digital HIFDI: pemeriksaan balita di posyandu, titik temu pertama layanan primer dengan warga.</div>
      </div>
    </div>
    <button class="fg-nav fg-prev" type="button" aria-label="Gambar sebelumnya">&lsaquo;</button>
    <button class="fg-nav fg-next" type="button" aria-label="Gambar berikutnya">&rsaquo;</button>
    <span class="fg-count">1 / 2</span>
  </div>
  <div class="fg-thumbs">
    <button type="button" class="is-active" aria-label="Gambar 1"><img src="../images/article-109-idi76-klinik.jpg" alt=""></button>
    <button type="button" aria-label="Gambar 2"><img src="../images/article-109-idi76-posyandu.jpg" alt=""></button>
  </div>
</figure>

<h2>Posisi HIFDI</h2>

<p>HIFDI memandang penguatan IDI sebagai wadah tunggal profesi dokter sejalan dengan penguatan fasyankes primer. HIFDI mengajak IDI menjaga mutu dan etik di fasilitas layanan primer, dan siap menjadi mitra dialog dalam setiap kebijakan yang menyentuh klinik pratama, tempat praktik mandiri dokter, dan puskesmas.</p>

<h2>Penutup</h2>

<p>HIFDI mengucapkan selamat ulang tahun ke-76 kepada IDI dan selamat Hari Dokter Nasional kepada seluruh dokter di Indonesia. Harapan HIFDI sederhana: dokter di layanan primer punya waktu yang cukup untuk pasiennya, dan organisasi profesi tetap menjadi suluh yang menerangi jalan menuju keadilan kesehatan.</p>

<p>HIFDI adalah organisasi yang mewadahi ekosistem fasilitas pelayanan kesehatan di Indonesia, meliputi klinik pratama, tempat praktik mandiri dokter, puskesmas, dan laboratorium kesehatan. HIFDI berbadan hukum berdasarkan Keputusan Menteri Hukum dan Hak Asasi Manusia RI Nomor AHU-0005242.AH.01.07.TAHUN 2023.</p>

<div class="sources-box">
<div class="sources-title">Referensi</div>
<ul>
<li>Ikatan Dokter Indonesia, &ldquo;IDI Berkemajuan, Berbakti Untuk Bangsa&rdquo; (situs resmi PB IDI): <a href="https://idionline.org/">https://idionline.org/</a></li>
<li>Zaenal Abidin, &ldquo;IDI Tetaplah Menyala dan Menjadi Suluh Bangsa&rdquo;, Pinisi.co.id: <a href="https://pinisi.co.id/idi-tetaplah-menyala-dan-menjadi-suluh-bangsa/">https://pinisi.co.id/idi-tetaplah-menyala-dan-menjadi-suluh-bangsa/</a></li>
<li>Liputan6, &ldquo;Sejarah dan Makna Hari Dokter Indonesia 24 Oktober, Berawal dari Lahirnya IDI pada 1950&rdquo;: <a href="https://www.liputan6.com/hot/read/8319724/sejarah-dan-makna-hari-dokter-indonesia">https://www.liputan6.com/hot/read/8319724/sejarah-dan-makna-hari-dokter-indonesia</a></li>
</ul>
</div>
</div>
"""

LD = {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
    "url": URL,
    "headline": TITLE,
    "description": DESC,
    "image": [IMAGE],
    "datePublished": "2026-10-24T12:00:00+07:00",
    "dateModified": "2026-10-24T12:00:00+07:00",
    "inLanguage": "id-ID",
    "author": {"@type": "Organization", "name": "Redaksi Berita HIFDI"},
    "publisher": {
        "@type": "Organization",
        "name": "Himpunan Fasyankes Dokter Indonesia (HIFDI)",
        "alternateName": "HIFDI",
        "url": "https://hifdi.id",
        "logo": {"@type": "ImageObject",
                 "url": "https://berita.hifdi.id/images/logo-hifdi.png"},
    },
    "articleSection": CAT,
}

html = SRC.read_text(encoding="utf-8")

html = re.sub(r"<title>.*?</title>", f"<title>{TITLE} - HIFDI</title>", html, count=1)
html = re.sub(r'<meta name="description" content="[^"]*">',
              f'<meta name="description" content="{DESC}">', html, count=1)
html = re.sub(r'<meta property="og:title" content="[^"]*">',
              f'<meta property="og:title" content="{TITLE} - HIFDI">', html, count=1)
html = re.sub(r'<meta property="og:description" content="[^"]*">',
              f'<meta property="og:description" content="{DESC}">', html, count=1)
html = re.sub(r'<meta property="og:image" content="[^"]*">',
              f'<meta property="og:image" content="{IMAGE}">', html, count=1)
html = re.sub(r'<link rel="canonical" href="[^"]*">',
              f'<link rel="canonical" href="{URL}">', html, count=1)
html = re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>',
              '<script type="application/ld+json">\n'
              + json.dumps(LD, ensure_ascii=False, indent=2)
              + "\n</script>", html, count=1)

start = html.index('<div class="article-container">') + len('<div class="article-container">')
end = html.index('<div class="article-footer">')
html = html[:start] + "\n" + BODY + "</div>\n" + html[end:]

DEST.parent.mkdir(parents=True, exist_ok=True)
DEST.write_text(html, encoding="utf-8")
print("tulis", DEST, len(html), "bytes")
words = len(re.findall(r"\S+", re.sub(r"<[^>]+>", " ", BODY)))
print("kata badan artikel (incl caption/ref):", words)
print("em-dash:", "\u2014" in BODY)
