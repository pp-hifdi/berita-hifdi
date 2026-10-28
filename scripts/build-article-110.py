#!/usr/bin/env python3
"""Rakit article-110 (Kabar HIFDI, Hari Sumpah Pemuda ke-98).

CSS diambil dari article-109/index.html supaya identitas visual tidak berubah.
Jalankan: python3 scripts/build-article-110.py
Lalu:     python3 scripts/seo_refresh.py && python3 scripts/validate_seo.py
"""
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "article-109" / "index.html"
OUT = ROOT / "article-110" / "index.html"

TITLE = "Sumpah Pemuda ke-98: Pemuda Paling Rentan Depresi, Paling Jarang Berobat"
DEK = ("Depresi paling tinggi pada kelompok usia 15 sampai 24 tahun, tetapi hanya 10,4 persen "
       "yang berobat. Di Hari Sumpah Pemuda ke-98, HIFDI menilai ikrar satu bangsa belum "
       "menjadi satu akses layanan.")
DESC = ("HIFDI memperingati Hari Sumpah Pemuda ke-98 28 Oktober 2026 dan menyoroti kesenjangan "
        "akses layanan kesehatan jiwa bagi pemuda usia 15 sampai 24 tahun, kelompok dengan "
        "prevalensi depresi tertinggi tetapi paling sedikit mendapat pengobatan.")
HERO = "article-110-jiwa-pemuda-hero.jpg"
OG = "article-110-og.jpg"
IMG_TUNGGU = "article-110-jiwa-pemuda-tunggu.jpg"
DATE_ID = "28 Oktober 2026"
BYLINE = "Redaksi Berita HIFDI"
BYLINE_ROLES = "Peringatan Hari Sumpah Pemuda ke-98, 28 Oktober 2026"

BODY = """
<p><strong>JAKARTA, 28 OKTOBER 2026.</strong> Hari Sumpah Pemuda tahun ini memasuki usia ke-98. Kementerian Pemuda dan Olahraga menerbitkan Surat Edaran Nomor 10.14.19 Tahun 2026 dengan tema &ldquo;Patriotik, Gigih, Berempati: Pemuda untuk Indonesia&rdquo;, dan mengimbau pemerintah pusat serta pemerintah daerah menyelenggarakan upacara bersama pada Rabu, 28 Oktober 2026, pukul 08.00 waktu setempat. Himpunan Fasyankes Dokter Indonesia (HIFDI) mengucapkan selamat dan menyoroti satu kata dalam tema itu: berempati.</p>

<p>Ikrar 1928 menyatukan pemuda dari berbagai daerah dalam satu tanah air, satu bangsa, dan satu bahasa. Sembilan puluh delapan tahun kemudian, persoalannya bergeser ke hal yang lebih sehari-hari: apakah pemuda di semua daerah punya akses yang sama ketika sakit, termasuk ketika yang sakit adalah jiwanya.</p>

<h2>Depresi tertinggi, pengobatan paling sedikit</h2>

<p>Survei Kesehatan Indonesia (SKI) 2023 mencatat prevalensi depresi nasional 1,4 persen. Angka itu tidak rata menurut umur. Kelompok 15 sampai 24 tahun mencatat prevalensi tertinggi, yaitu 2 persen, dan lebih tinggi pada perempuan (2,8 persen) dibanding laki-laki (1,1 persen).</p>

<p>Yang lebih penting bagi layanan kesehatan: kelompok ini justru paling sedikit mengakses pengobatan. Hanya 10,4 persen anak muda dengan depresi yang mendapat penanganan. Dari anak muda yang depresi, 61 persen mengaku punya pikiran mengakhiri hidup dalam sebulan terakhir, sekitar 36 kali lebih besar dibanding anak muda yang tidak depresi (1,7 persen). Badan Kebijakan Pembangunan Kesehatan Kementerian Kesehatan menyimpulkan kelompok ini membutuhkan intervensi agar kondisinya tidak berlanjut menjadi masalah yang lebih berat.</p>

<blockquote><p>&ldquo;Ikrar 1928 menyatukan bangsa. Pekerjaan hari ini menyatukan akses: pemuda di kota dan di desa harus bisa menjangkau layanan jiwa tanpa bergantung pada kemampuannya membayar.&rdquo;</p></blockquote>

<h2>Pintu pertama ada di fasyankes primer</h2>

<p>Pemuda jarang datang ke layanan kesehatan dengan kalimat &ldquo;saya depresi&rdquo;. Mereka datang dengan sakit kepala berulang, nyeri lambung, sulit tidur, atau keluhan yang sebabnya tidak jelas. Tempat pertama mereka datang biasanya bukan rumah sakit, melainkan klinik pratama, tempat praktik mandiri dokter (TPMD), atau puskesmas.</p>

<p>Di puskesmas, layanan kesehatan remaja punya jalur resmi. Petunjuk Teknis Integrasi Layanan Primer dalam Keputusan Menteri Kesehatan Nomor 2015 Tahun 2023 menempatkan Pelayanan Kesehatan Peduli Remaja (PKPR) sebagai paket layanan di dalam dan di luar gedung puskesmas, mencakup penjaringan kesehatan, skrining, dan pemeriksaan berkala.</p>

<figure class="inline-fig">
  <img src="../images/article-110-jiwa-pemuda-tunggu.jpg" alt="Ilustrasi digital HIFDI: seorang pemuda duduk sendiri di ruang tunggu klinik pratama sambil menunduk memegang ponsel." loading="lazy">
  <figcaption>Ilustrasi digital HIFDI: keluhan jiwa pada pemuda sering muncul sebagai keluhan fisik yang dibawa ke layanan primer.</figcaption>
</figure>

<p>Persoalannya, paket layanan remaja itu tidak otomatis sampai ke klinik pratama dan TPMD, padahal keduanya menjadi pintu pertama bagi banyak pemuda di kota dan kawasan industri. Menurut HIFDI, fasilitas ini menandatangani kontrak yang sama dengan BPJS Kesehatan dan dituntut standar akreditasi yang sama, tetapi biaya layanan tambahan di luar paket tidak otomatis ikut terbayar.</p>

<h2>Posisi HIFDI</h2>

<p>HIFDI menilai kesehatan jiwa pemuda tidak akan membaik selama layanan hanya tersedia di satu jenis fasilitas. HIFDI menuntut tiga hal. Pertama, paket layanan kesehatan remaja, termasuk skrining kesehatan jiwa, dibuka untuk fasyankes primer swasta dengan standar dan pembiayaan yang setara. Kedua, skrining kesehatan jiwa masuk paket pemeriksaan rutin di klinik pratama dan TPMD, dengan tarif yang menutup biaya pelaksanaannya. Ketiga, HIFDI dilibatkan dalam penyusunan pedoman pelayanan kesehatan remaja, karena kebijakan yang tidak melibatkan pelaksana di lapangan berhenti sebagai dokumen.</p>

<h2>Penutup</h2>

<p>Sumpah Pemuda mengajarkan bahwa persatuan tidak lahir dari kesamaan keadaan, melainkan dari kesediaan menanggung beban bersama. Bagi HIFDI, bentuk paling nyata dari sikap itu adalah memastikan pemuda yang datang meminta tolong benar-benar mendapat pertolongan, di fasilitas mana pun mereka datang.</p>

<p>HIFDI adalah organisasi yang mewadahi ekosistem fasilitas pelayanan kesehatan di Indonesia, meliputi klinik pratama, tempat praktik mandiri dokter, puskesmas, dan laboratorium kesehatan. HIFDI berbadan hukum berdasarkan Keputusan Menteri Hukum dan Hak Asasi Manusia RI Nomor AHU-0005242.AH.01.07.TAHUN 2023.</p>
"""

SOURCES = [
    ("Kementerian Pemuda dan Olahraga, Surat Edaran Menteri Pemuda dan Olahraga Nomor 10.14.19 Tahun 2026 "
     "tentang Penyelenggaraan Peringatan Hari Sumpah Pemuda ke-98 Tahun 2026 (14 Oktober 2026), "
     "diberitakan Kompas TV",
     "https://www.kompas.tv/info-publik/698017/ini-pedoman-peringatan-sumpah-pemuda-2026-resmi-dari-kemenpora?page=all"),
    ("Badan Kebijakan Pembangunan Kesehatan Kementerian Kesehatan RI, &ldquo;Depresi pada Anak Muda di Indonesia&rdquo;, "
     "Lembar Fakta Survei Kesehatan Indonesia 2023",
     "https://www.badankebijakan.kemkes.go.id/repositori/id/eprint/5532/1/03%20factsheet%20Keswa_bahasa.pdf"),
    ("Kementerian Kesehatan RI, Keputusan Menteri Kesehatan Nomor 2015 Tahun 2023 tentang Petunjuk Teknis "
     "Integrasi Layanan Primer (pelayanan kesehatan anak usia sekolah dan remaja melalui PKPR di puskesmas)",
     "https://renbut.kemkes.go.id/regulasi/Buku%20KMK%20No%202015%20tahun%202023%20tentang%20Petunjuk%20Teknis%20ILP.pdf"),
]

EXTRA_CSS = """
.inline-fig { margin: 30px 0 34px; }
.inline-fig img { display: block; width: 100%; height: auto; border-radius: 10px; border: 1px solid var(--neutral-200); }
.inline-fig figcaption { font-family: var(--font-mono); font-size: 11px; color: var(--neutral-500); margin-top: 10px; line-height: 1.6; }
"""


def base_css() -> str:
    raw = SRC.read_text(encoding="utf-8")
    start = raw.index("<style>")
    end = raw.rindex("</style>")
    css = raw[start:end]
    return css.replace("<style>", "").replace("</style>", "").strip()


def main() -> None:
    sources_html = "\n".join(
        f'<li>{text}: <a href="{url}">{url}</a></li>' for text, url in SOURCES
    )
    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{DESC}">
<meta property="og:title" content="{TITLE} - HIFDI">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://berita.hifdi.id/images/{OG}">
<meta property="og:type" content="article">
<title>{TITLE} - HIFDI</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400&display=swap" rel="stylesheet">
<style>
{base_css()}
{EXTRA_CSS}
</style>
</head>
<body>
<header>
<div class="header-inner">
<a class="header-left" href="https://hifdi.id">
<img class="header-logo" src="../images/logo-hifdi.png" alt="Logo HIFDI">
<span class="header-brand-name">Berita HIFDI</span>
</a>
<a class="back-link" href="../">&larr; Kembali ke Portal</a>
</div>
</header>
<div class="article-container">
<span class="article-category">Kabar HIFDI</span>
<h1 class="article-title">{TITLE}</h1>
<div class="article-subtitle">&ldquo;{DEK}&rdquo;</div>
<div class="article-meta">
<span>{DATE_ID}</span>
<span>Kabar HIFDI</span>
</div>
<img class="featured-image" src="../images/{HERO}" alt="Ilustrasi digital HIFDI: dokter di klinik pratama berbincang dengan pasien pemuda yang tampak lelah.">
<p class="featured-caption">Ilustrasi digital HIFDI: keluhan kesehatan jiwa pada pemuda kerap masuk lewat pintu layanan primer. Desain: Berita HIFDI.</p>
<div class="byline">
<div class="byline-name">{BYLINE}</div>
<div class="byline-roles">{BYLINE_ROLES}</div>
</div>
<div class="article-body">{BODY}
<div class="sources-box">
<div class="sources-title">Referensi</div>
<ul>
{sources_html}
</ul>
</div>
</div>
</div>
<div class="article-footer">
<a class="back-to-portal" href="../">&larr; Kembali ke Portal Berita</a>
</div>
</div>
<footer>
<p>&copy; 2026 Himpunan Fasyankes Dokter Indonesia (HIFDI) &nbsp;|&nbsp; <a href="https://hifdi.id">hifdi.id</a> &nbsp;|&nbsp; <a href="https://academy.hifdi.id">academy.hifdi.id</a></p>
</footer>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    words = len(re.sub(r"<[^>]+>", " ", BODY).split())
    print(f"wrote {OUT.relative_to(ROOT)} | {words} kata badan artikel")


if __name__ == "__main__":
    main()
