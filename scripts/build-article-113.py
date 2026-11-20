#!/usr/bin/env python3
"""Rakit article-113 (Opini: Menyelamatkan Otak Sebelum Terlambat, Muhammad Akbar).

Naskah: ~/workspace/artikel-opini-stroke-hulu/naskah-final.md
Dimuat sebelumnya di Harian Waspada, halaman A6 (Opini), 18 November 2026.
Jalankan: python3 scripts/build-article-113.py
Lalu:     python3 scripts/seo_refresh.py && python3 scripts/validate_seo.py
"""
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "article-112" / "index.html"
OUT = ROOT / "article-113" / "index.html"
NASKAH = pathlib.Path.home() / "workspace" / "artikel-opini-stroke-hulu" / "naskah-final.md"

TITLE = "Negara Membayar Rp7,2 Triliun untuk Strok, tapi Skriningnya Baru Menyentuh Puskesmas"
DEK = ("BPJS Kesehatan menanggung 9,5 juta kasus strok senilai Rp7,2 triliun pada 2025, naik "
       "hampir tiga kali lipat dalam enam tahun. HIFDI menilai pencegahan masih dikerjakan "
       "setengah hati, karena fasyankes primer swasta yang melayani peserta JKN belum masuk "
       "skema skrining.")
DESC = ("BPJS menanggung 9,5 juta kasus strok senilai Rp7,2 triliun pada 2025. HIFDI menilai "
        "skrining strok tidak boleh berhenti di Puskesmas dan harus mencakup klinik pratama "
        "serta TPMD mitra JKN, dengan target yang terukur.")
HERO = "article-113-stroke-hero.jpg"
OG = "article-113-og.jpg"
DATE_ID = "20 November 2026"
BYLINE = "Redaksi Berita HIFDI"
BYLINE_ROLES = ("Diolah dari opini Prof. dr. Muhammad Akbar di Harian Waspada, 18 November 2026, "
                "dikembangkan dengan data Kemenkes dan IHME")
KATEGORI = "Advokasi"
KATEGORI_SLUG = "advokasi"

EDITOR_NOTE = ("Artikel ini diolah dari opini Prof. dr. Muhammad Akbar, Sp.S., Subsp. NIOO(K), Ph.D., DFM. "
               "yang dimuat Harian Waspada, halaman A6 (Opini), Rabu 18 November 2026, dalam rangka "
               "menyongsong Kongres Nasional XI PERDOSNI di Medan. Data dan gagasan pokok berasal dari tulisan "
               "tersebut, sedangkan sudut pembahasan dan butir tuntutan merupakan pengembangan redaksi Berita HIFDI. "
               "Pada 19 November 2026, Prof. Akbar terpilih sebagai Ketua Umum PERDOSNI periode 2026 sampai 2029.")

GALLERY = """
<div class="gal-title">Galeri</div>
<figure class="fig-gallery" data-gallery>
  <div class="fg-stage">
    <div class="fg-main">
      <div class="fg-slide">
        <div class="fg-frame fit"><img src="../images/article-113-kartu.jpg" alt="Kartu ringkasan Berita HIFDI: biaya strok yang ditanggung BPJS 2025, capaian deteksi dini, dan porsi strok yang dapat dicegah." loading="lazy"></div>
        <div class="fg-cap">Ringkasan angka yang dipakai artikel ini. Desain: Berita HIFDI.</div>
      </div>
      <div class="fg-slide">
        <div class="fg-frame fit"><img src="../images/article-113-waspada.jpg" alt="Halaman A6 Harian Waspada edisi Rabu 18 November 2026 yang memuat opini Menyelamatkan Otak Sebelum Terlambat." loading="lazy"></div>
        <div class="fg-cap">Halaman A6 (Opini) Harian Waspada, Rabu 18 November 2026, tempat tulisan ini pertama dimuat. Foto: dokumen.</div>
      </div>
    </div>
    <button class="fg-nav fg-prev" type="button" aria-label="Slide sebelumnya">&lsaquo;</button>
    <button class="fg-nav fg-next" type="button" aria-label="Slide berikutnya">&rsaquo;</button>
    <span class="fg-count">1 / 2</span>
  </div>
</figure>
"""

GALLERY_CSS = """
.gal-title { font-family: var(--font-display); font-size: 24px; margin: 44px 0 14px; }
.fig-gallery { margin: 0 0 38px; }
.fg-stage { position: relative; border-radius: 12px; overflow: hidden; border: 1px solid var(--neutral-200); background: var(--neutral-100); }
.fg-main { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scroll-behavior: smooth; scrollbar-width: none; }
.fg-main::-webkit-scrollbar { display: none; }
.fg-slide { flex: 0 0 100%; scroll-snap-align: start; display: flex; flex-direction: column; }
.fg-frame { height: 340px; display: flex; align-items: center; justify-content: center; background: #F4F1E7; }
.fg-frame img { display: block; width: 100%; height: 100%; object-fit: cover; }
.fg-frame.fit img { object-fit: contain; }
@media (max-width: 560px) { .fg-frame { height: 240px; } }
.fg-cap { font-family: var(--font-body); font-size: 12.5px; line-height: 1.6; color: var(--neutral-500); padding: 10px 14px 12px; background: #fff; }
.fg-nav { position: absolute; top: 42%; transform: translateY(-50%); width: 38px; height: 38px; border-radius: 50%; border: none; background: rgba(18,43,26,0.72); color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; line-height: 1; z-index: 2; }
.fg-nav:hover { background: rgba(18,43,26,0.92); }
.fg-nav:disabled { opacity: 0.3; cursor: default; }
.fg-prev { left: 12px; } .fg-next { right: 12px; }
.fg-count { position: absolute; right: 12px; top: 12px; background: rgba(18,43,26,0.72); color: #fff; font-family: var(--font-mono); font-size: 11px; padding: 3px 9px; border-radius: 999px; z-index: 2; }
.editor-note { margin: 34px 0 0; padding: 16px 20px; background: #F7F7F5; border-left: 3px solid #1B4028; border-radius: 6px; font-size: 13.5px; line-height: 1.65; color: #4A534C; }
.editor-note b { color: #1B4028; }
"""

GALLERY_JS = """<script>
document.querySelectorAll('[data-gallery]').forEach(function (g) {
  var main = g.querySelector('.fg-main');
  var count = g.querySelector('.fg-count');
  var prev = g.querySelector('.fg-prev');
  var next = g.querySelector('.fg-next');
  var total = g.querySelectorAll('.fg-slide').length;
  function go(i) {
    var n = Math.max(0, Math.min(i, total - 1));
    main.scrollTo({ left: n * main.clientWidth, behavior: 'smooth' });
  }
  prev.addEventListener('click', function () { go(Math.round(main.scrollLeft / main.clientWidth) - 1); });
  next.addEventListener('click', function () { go(Math.round(main.scrollLeft / main.clientWidth) + 1); });
  main.addEventListener('scroll', function () {
    var i = Math.round(main.scrollLeft / main.clientWidth);
    count.textContent = (i + 1) + ' / ' + total;
    prev.disabled = i === 0;
    next.disabled = i === total - 1;
  }, { passive: true });
  prev.disabled = true;
});
</script>"""

EXTRA_CSS = GALLERY_CSS

SOURCES = [
    ("Harian Waspada, halaman A6 (Opini), Rabu 18 November 2026, tempat tulisan ini pertama dimuat",
     None),
    ("ANTARA Lampung, &ldquo;Penyakit stroke penyebab kematian terbanyak di Indonesia&rdquo; "
     "(data IHME 2019: strok 19,42 persen dan jantung iskemik 14,38 persen)",
     "https://lampung.antaranews.com/berita/699501/penyakit-stroke-penyebab-kematian-terbanyak-di-indonesia"),
    ("Kementerian Kesehatan RI, &ldquo;Cegah Stroke dengan Aktivitas Fisik&rdquo; "
     "(sekitar 90 persen strok dapat dicegah, prevalensi 8,3 per 1.000 penduduk)",
     "https://kemkes.go.id/eng/cegah-stroke-dengan-aktivitas-fisik"),
    ("Katadata, &ldquo;Dirut BPJS Kesehatan Dorong Masyarakat Rajin Berolahraga demi "
     "Perpanjang Usia&rdquo; (konteks pembiayaan penyakit katastropik 2025)",
     "https://katadata.co.id/info/6a02c05781f16/dirut-bpjs-kesehatan-dorong-masyarakat-rajin-berolahraga-demi-perpanjang-usia"),
    ("Sumut Pos, &ldquo;PERDOSNI Harap Setiap Rumah Sakit Miliki Unit Stroke&rdquo;, 20 November 2026",
     "https://sumutpos.jawapos.com/kesehatan/2611200016/perdosni-harap-setiap-rumah-sakit-miliki-unit-stroke"),
    ("Berita HIFDI, &ldquo;Prof. Muhammad Akbar Nakhodai PERDOSNI, HIFDI Soroti Deteksi Dini "
     "Stroke di Layanan Primer&rdquo;, 20 November 2026",
     "https://berita.hifdi.id/article-112/"),
]


def parse_naskah() -> tuple[str, str, list[str]]:
    raw = NASKAH.read_text(encoding="utf-8").strip()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", raw) if b.strip()]
    return blocks[0].lstrip("# ").strip(), blocks[1], blocks[2:]


def esc(s: str) -> str:
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out = []
    open_q = True
    for ch in s:
        if ch == '"':
            out.append("&ldquo;" if open_q else "&rdquo;")
            open_q = not open_q
        else:
            out.append(ch)
    return "".join(out)


def quote_html(b: str) -> str:
    parts = [ln.lstrip("> ").strip() for ln in b.split("\n")]
    parts = [p for p in parts if p]
    sep = parts.index("---") if "---" in parts else len(parts)
    text = " ".join(parts[:sep])
    attribution = parts[sep + 1] if sep < len(parts) - 1 else ""
    who, _, role = attribution.partition("|")
    html = f"<blockquote><p>&ldquo;{esc(text)}&rdquo;</p>"
    if who.strip():
        html += f"<p><strong>{esc(who.strip())}</strong><br>{esc(role.strip())}</p>"
    return html + "</blockquote>"


def body_html(blocks: list[str]) -> str:
    out = []
    for i, b in enumerate(blocks):
        if b.startswith("## "):
            out.append(f"<h2>{esc(b[3:].strip())}</h2>")
        elif b.startswith(">"):
            out.append(quote_html(b))
        else:
            out.append(f"<p>{esc(b)}</p>")
            if i == len(blocks) - 1:
                out.append(f'<div class="editor-note"><b>Catatan redaksi.</b> {esc(EDITOR_NOTE)}</div>')
                out.append(GALLERY.strip())
    return "\n\n".join(out)


def base_css() -> str:
    raw = SRC.read_text(encoding="utf-8")
    start = raw.index("<style>")
    end = raw.rindex("</style>")
    return raw[start:end].replace("<style>", "").replace("</style>", "").strip()


def main() -> None:
    title, dek, blocks = parse_naskah()
    assert title == TITLE, f"judul naskah berbeda: {title}"
    assert dek == DEK, "dek naskah berbeda dari konstanta"
    body = body_html(blocks)
    items = []
    for text, url in SOURCES:
        items.append(f'<li>{text}.' + (f' <a href="{url}">{url}</a>' if url else "") + "</li>")
    sources_html = "\n".join(items)
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
<img class="featured-image" src="../images/{HERO}" alt="Enam dokter spesialis neurologi berfoto di depan spanduk konferensi pers Kongres Nasional XI PERDOSNI dan AOCN XX di Medan.">
<p class="featured-caption">Konferensi pers Kongres Nasional XI PERDOSNI dan AOCN XX di Medan, November 2026. Foto: Sumut Pos.</p>
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
{GALLERY_JS}
<footer>
<p>&copy; 2026 Himpunan Fasyankes Dokter Indonesia (HIFDI) &nbsp;|&nbsp; <a href="https://hifdi.id">hifdi.id</a> &nbsp;|&nbsp; <a href="https://academy.hifdi.id">academy.hifdi.id</a></p>
</footer>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} | {len(re.sub(r'<[^>]+>', ' ', body).split())} kata badan")


if __name__ == "__main__":
    main()
