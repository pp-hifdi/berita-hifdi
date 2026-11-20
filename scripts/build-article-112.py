#!/usr/bin/env python3
"""Rakit article-112 (Kabar HIFDI: Prof. Muhammad Akbar nakhodai PERDOSNI).

Sumber naskah: ~/workspace/artikel-perdosni-akbar/naskah-final.md
CSS diambil dari article-111/index.html supaya identitas visual tidak berubah.
Jalankan: python3 scripts/build-article-112.py
Lalu:     python3 scripts/seo_refresh.py && python3 scripts/validate_seo.py
"""
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "article-111" / "index.html"
OUT = ROOT / "article-112" / "index.html"
NASKAH = pathlib.Path.home() / "workspace" / "artikel-perdosni-akbar" / "naskah-final.md"

TITLE = "Prof. Muhammad Akbar Nakhodai PERDOSNI, HIFDI Soroti Deteksi Dini Stroke di Layanan Primer"
DEK = ("Akbar menang 135 suara berbanding 101 dalam Kongres XI PERDOSNI di Medan. Bagi HIFDI, "
       "pekerjaan terbesar neurologi Indonesia justru dimulai di klinik pratama: menemukan "
       "hipertensi dan diabetes sebelum berubah menjadi stroke.")
DESC = ("Prof. dr. Muhammad Akbar terpilih sebagai Ketua Umum PERDOSNI 2026 sampai 2029 dengan "
        "135 suara, unggul 34 suara atas Dr. dr. Fritz. HIFDI menyoroti deteksi dini stroke dan "
        "pengendalian faktor risiko di layanan primer.")
HERO = "article-112-akbar-perdosni-hero.jpg"
OG = "article-112-og.jpg"
DATE_ID = "20 November 2026"
BYLINE = "Redaksi Berita HIFDI"
BYLINE_ROLES = "Kabar HIFDI, Kongres XI PERDOSNI, Medan, 19 November 2026"
KATEGORI = "Kabar HIFDI"
KATEGORI_SLUG = "kabar-hifdi"

DATELINE = "MEDAN, 20 NOVEMBER 2026."

BLOCKQUOTE = ("Waktu sebesar itu tidak bisa dibeli di ruang gawat darurat. Ia diselamatkan "
              "bertahun-tahun sebelumnya, di tensimeter dan catatan gula darah di layanan primer.")

SOURCES = [
    ("Buka Mata News, &ldquo;Unggul 34 Suara, Prof Muhammad Akbar Terpilih Pimpin PERDOSNI "
     "2026-2029&rdquo;, 20 November 2026",
     "https://bukamatanews.id/read/2026/11/20/unggul-34-suara-prof-muhammad-akbar-terpilih-pimpin-perdosni-20262029"),
    ("ANTARA, &ldquo;Perdosni siap isi kebutuhan dokter saraf RS di daerah&rdquo;, "
     "2 Mei 2026 (pernyataan Muhammad Akbar soal syarat CT-scan)",
     "https://www.antaranews.com/berita/5551344/perdosni-siap-isi-kebutuhan-dokter-sarafrs-di-daerah"),
    ("Kementerian Kesehatan RI, &ldquo;Cegah Stroke dengan Aktivitas Fisik&rdquo;, "
     "25 Oktober 2024 (beban stroke, prevalensi SKI 2023, pembiayaan, deteksi dini)",
     "https://kemkes.go.id/eng/cegah-stroke-dengan-aktivitas-fisik"),
    ("PERDOSNI, &ldquo;Konas XI PERDOSNI dan AOCN XX&rdquo;, Medan, 18 sampai 22 November 2026",
     "https://perdosni.org/events/konas-xi-perdosni-dan-aocn-xx--1775728212769"),
]

GALLERY = """
<div class="gal-title">Galeri</div>
<figure class="fig-gallery" data-gallery>
  <div class="fg-stage">
    <div class="fg-main">
      <div class="fg-slide">
        <div class="fg-frame"><img src="../images/article-112-akbar.jpg" alt="Prof. dr. Muhammad Akbar, Sp.S., Subsp. NIOO(K), Ph.D., DFM., tersenyum memakai toga akademik." loading="lazy"></div>
        <div class="fg-cap">Prof. dr. Muhammad Akbar, Sp.S., Subsp. NIOO(K), Ph.D., DFM., Ketua Umum PERDOSNI 2026 sampai 2029. Foto: dokumen, melalui pemberitaan Kongres XI PERDOSNI.</div>
      </div>
      <div class="fg-slide">
        <div class="fg-frame"><img src="../images/article-112-zaenal-abidin.jpg" alt="dr. Zaenal Abidin, M.H., Ketua Umum Himpunan Fasyankes Dokter Indonesia, tersenyum memakai kemeja batik sambil duduk di sofa." loading="lazy"></div>
        <div class="fg-cap">dr. Zaenal Abidin, M.H., Ketua Umum Himpunan Fasyankes Dokter Indonesia. Foto: dokumen HIFDI.</div>
      </div>
      <div class="fg-slide">
        <div class="fg-frame fit"><img src="../images/article-112-kutipan-ketum.jpg" alt="Kartu kutipan Ketua Umum HIFDI dr. Zaenal Abidin, M.H. tentang beban stroke di hulu layanan primer." loading="lazy"></div>
        <div class="fg-cap">Kutipan Ketua Umum HIFDI dr. Zaenal Abidin, M.H. soal beban stroke yang lahir di layanan primer. Desain: Berita HIFDI.</div>
      </div>
    </div>
    <button class="fg-nav fg-prev" type="button" aria-label="Slide sebelumnya">&lsaquo;</button>
    <button class="fg-nav fg-next" type="button" aria-label="Slide berikutnya">&rsaquo;</button>
    <span class="fg-count">1 / 3</span>
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
@media (max-width: 560px) { .fg-frame { height: 220px; } }
.fg-cap { font-family: var(--font-body); font-size: 12.5px; line-height: 1.6; color: var(--neutral-500); padding: 10px 14px 12px; background: #fff; }
.fg-nav { position: absolute; top: 42%; transform: translateY(-50%); width: 38px; height: 38px; border-radius: 50%; border: none; background: rgba(18,43,26,0.72); color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; line-height: 1; z-index: 2; }
.fg-nav:hover { background: rgba(18,43,26,0.92); }
.fg-nav:disabled { opacity: 0.3; cursor: default; }
.fg-prev { left: 12px; } .fg-next { right: 12px; }
.fg-count { position: absolute; right: 12px; top: 12px; background: rgba(18,43,26,0.72); color: #fff; font-family: var(--font-mono); font-size: 11px; padding: 3px 9px; border-radius: 999px; z-index: 2; }
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

GAL_ANCHOR = """        elif b.startswith(">"):
            out.append(quote_html(b))"""

EXTRA_CSS = GALLERY_CSS


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
    for b in blocks:
        if b.startswith("## "):
            out.append(f"<h2>{esc(b[3:].strip())}</h2>")
        elif b.startswith(">"):
            out.append(quote_html(b))
            out.append(GALLERY.strip())
        elif b.startswith(DATELINE):
            rest = b[len(DATELINE):].strip()
            out.append(f"<p><strong>{DATELINE}</strong> {esc(rest)}</p>")
        else:
            out.append(f"<p>{esc(b)}</p>")
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
<img class="featured-image" src="../images/{HERO}" alt="Kartu Berita HIFDI: Prof. Akbar Nakhodai PERDOSNI, dengan logo HIFDI dan PERDOSNI serta tiga angka kunci, perolehan suara 135 berbanding 101, prevalensi stroke 8,3 per 1.000, dan 90 persen stroke dapat dicegah.">
<p class="featured-caption">Kartu Berita HIFDI: Kongres XI PERDOSNI di Medan, 19 November 2026. Desain: Berita HIFDI.</p>
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
