#!/usr/bin/env python3
"""Rakit article-111 (Esai, kesejahteraan tenaga medis) dari naskah kiriman.

Sumber naskah: ~/workspace/artikel-kesejahteraan-tenaga-medis/naskah-final.md
CSS diambil dari article-110/index.html supaya identitas visual tidak berubah.
Jalankan: python3 scripts/build-article-111.py
Lalu:     python3 scripts/seo_refresh.py && python3 scripts/validate_seo.py
"""
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "article-110" / "index.html"
OUT = ROOT / "article-111" / "index.html"
NASKAH = pathlib.Path.home() / "workspace" / "artikel-kesejahteraan-tenaga-medis" / "naskah-final.md"

TITLE = "Butuh Berapa Banyak Contoh Lagi: Potret Kesejahteraan Tenaga Medis Indonesia"
DEK = ("Hampir setiap orang bersentuhan dengan tenaga medis, tetapi kesejahteraan mereka jarang "
       "masuk agenda publik. Kesejahteraan itu lebih luas dari angka di slip gaji: keselamatan kerja, "
       "kesehatan mental, perlindungan hukum, dan cara negara menempatkan mereka.")
DESC = ("Esai Gigih Pratama, dokter lulusan Universitas Palangka Raya: kesejahteraan tenaga medis "
        "bukan hanya soal gaji, melainkan keselamatan kerja, kesehatan mental, perlindungan hukum, "
        "dan pemerataan yang belum selesai.")
HERO = "article-111-nakes-sejahtera-hero.jpg"
OG = "article-111-og.jpg"
FOTO = "article-111-gigih-pratama.jpg"
DATE_ID = "18 November 2026"
BYLINE = "Gigih Pratama"
BYLINE_ROLES = "Dokter lulusan Universitas Palangka Raya, Kalimantan Tengah"
KATEGORI = "Advokasi"
KATEGORI_SLUG = "advokasi"

BIO = ("Gigih Pratama merupakan dokter lulusan Universitas Palangka Raya, Kalimantan Tengah. Ia pernah "
       "menjabat sebagai Ketua Nasional Perhimpunan Tim Bantuan Medis Mahasiswa Kedokteran Indonesia "
       "(PTBMMKI), serta terlibat dalam komunitas literasi Swarapena dan kegiatan pengabdian masyarakat "
       "SINESIA (Sisi Indonesia). Saat ini, ia mengemban amanah sebagai Wakil Chief Nasional Program "
       "Internsip Dokter Indonesia (PIDI). Ia menaruh perhatian pada kesehatan masyarakat, kebijakan "
       "kesehatan, isu sosial, pendidikan, literasi, dan pemberdayaan masyarakat.")

BLOCKQUOTE = ("Kita begitu cepat menuntut pelayanan yang sempurna, tetapi sering lupa bahwa orang yang "
              "kita tuntut juga manusia. Kita berharap mereka selalu kuat. Selalu sabar. Selalu tersedia.")
FIG_HTML = ""

SOURCES = [
    ("Katadata Databoks, &ldquo;Rasio Dokter di Tingkat Provinsi Indonesia Akhir 2025&rdquo; "
     "(mengutip data Kementerian Kesehatan, 0,76 dokter per 1.000 penduduk)",
     "https://databoks.katadata.co.id/layanan-konsumen-kesehatan/statistik/693a7b72e9bd8/rasio-dokter-di-tingkat-provinsi-indonesia-akhir-2025"),
    ("Kementerian Kesehatan RI, Indikator SDM Kesehatan: rasio dokter terhadap populasi "
     "(termasuk dokter spesialis 0,19 per 1.000 penduduk)",
     "https://eplanning-ditjennakes.kemkes.go.id/indikator/user/rasio_sdgs/?nakes=Dokter"),
    ("ANTARA, &ldquo;Kemenkes pegang bukti 733 pengaduan perundungan yang terkonfirmasi&rdquo; "
     "(dari 2.920 aduan PPDS Juli 2023 sampai Agustus 2025)",
     "https://www.antaranews.com/berita/5056981/kemenkes-pegang-bukti-733-pengaduan-perundungan-yang-terkonfirmasi"),
    ("Pan American Health Organization (kantor regional WHO untuk Amerika), &ldquo;Violence against health "
     "workers remains a challenge for health systems in the Americas&rdquo;, 24 September 2026 "
     "(sekitar 62 persen tenaga kesehatan dunia pernah mengalami kekerasan di tempat kerja)",
     "https://paho.org/en/news/24-9-2026-violence-against-health-workers-remains-challenge-health-systems-americas-paho-warns"),
    ("World Health Organization, &ldquo;Health workforce&rdquo;",
     "https://www.who.int/health-topics/health-workforce"),
    ("Undang-Undang Nomor 17 Tahun 2023 tentang Kesehatan, Pasal 273 ayat (1) tentang hak tenaga medis "
     "dan tenaga kesehatan atas perlindungan hukum",
     "https://pasal.id/peraturan/uu/uu-no-17-tahun-2023/pasal-273"),
    ("detikBali, &ldquo;PN Kupang Tolak Praperadilan 3 Anggota DPRD TTU di Kasus Intimidasi dr Icha&rdquo;, "
     "6 Oktober 2026",
     "https://www.detik.com/bali/hukum-dan-kriminal/d-8694855/pn-kupang-tolak-praperadilan-3-anggota-dprd-ttu-di-kasus-intimidasi-dr-icha"),
]

EXTRA_CSS = """
.author-box { margin: 44px 0 10px; padding: 20px 22px; background: var(--neutral-50, #F7F7F5); border-left: 3px solid var(--green-800, #1B4028); border-radius: 6px; display: flex; gap: 18px; align-items: flex-start; }
.author-photo { flex: 0 0 96px; width: 96px; height: 96px; object-fit: cover; border-radius: 6px; border: 1px solid var(--neutral-200); }
.author-title { font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--neutral-500); margin-bottom: 6px; }
.author-box p { font-size: 14px; line-height: 1.68; color: var(--neutral-700); margin: 0; }
@media (max-width: 560px) { .author-box { flex-direction: column; gap: 12px; } }
"""


def parse_naskah() -> tuple[str, str, list[str]]:
    raw = NASKAH.read_text(encoding="utf-8").strip()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", raw) if b.strip()]
    title = blocks[0].lstrip("# ").strip()
    dek = blocks[1]
    body_blocks = blocks[2:]
    return title, dek, body_blocks


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def body_html(blocks: list[str]) -> str:
    out = []
    for b in blocks:
        if b.startswith("## "):
            out.append(f"<h2>{esc(b[3:].strip())}</h2>")
        elif b == BLOCKQUOTE:
            out.append(f"<blockquote><p>&ldquo;{esc(b)}&rdquo;</p></blockquote>")
        else:
            out.append(f"<p>{esc(b)}</p>")
    out.append(
        '<div class="author-box">'
        f'<img class="author-photo" src="../images/{FOTO}" alt="Gigih Pratama, dokter lulusan Universitas Palangka Raya." loading="lazy">'
        '<div class="author-text"><div class="author-title">Tentang penulis</div>'
        f'<p>{esc(BIO)}</p></div></div>'
    )
    return "\n\n".join(out)


def base_css() -> str:
    raw = SRC.read_text(encoding="utf-8")
    start = raw.index("<style>")
    end = raw.rindex("</style>")
    css = raw[start:end]
    return css.replace("<style>", "").replace("</style>", "").strip()


def main() -> None:
    title, dek, blocks = parse_naskah()
    assert title == TITLE, f"judul naskah berbeda: {title}"
    assert dek == DEK, "dek naskah berbeda dari konstanta"
    body = body_html(blocks)
    sources_html = "\n".join(f'<li>{text}: <a href="{url}">{url}</a></li>' for text, url in SOURCES)
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
<span class="article-category">{KATEGORI}</span>
<h1 class="article-title">{TITLE}</h1>
<div class="article-subtitle">&ldquo;{DEK}&rdquo;</div>
<div class="article-meta">
<span>{DATE_ID}</span>
<span>{KATEGORI}</span>
</div>
<img class="featured-image" src="../images/{HERO}" alt="Kartu esai Berita HIFDI: judul Butuh Berapa Banyak Contoh Lagi dengan tiga angka kunci, rasio dokter 0,76 per 1.000 penduduk, 733 aduan perundungan PPDS terbukti, dan 62 persen tenaga kesehatan pernah mengalami kekerasan kerja.">
<p class="featured-caption">Kartu esai Berita HIFDI: tiga angka yang jadi pijakan tulisan ini. Desain: Berita HIFDI.</p>
<div class="byline">
<div class="byline-name">{BYLINE}</div>
<div class="byline-roles">{BYLINE_ROLES}</div>
</div>
<div class="article-body">{body}
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
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    print(f"wrote {OUT.relative_to(ROOT)} | {words} kata badan artikel (termasuk kotak penulis)")


if __name__ == "__main__":
    main()
