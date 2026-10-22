#!/usr/bin/env python3
"""SEO maintenance Berita HIFDI.

Menambah (idempoten) di setiap halaman:
  - <link rel="canonical">
  - JSON-LD schema.org NewsArticle / WebSite + Organization
Lalu menulis ulang:
  - sitemap.xml
  - robots.txt (dengan baris Sitemap)

Dijalankan manual atau oleh .github/workflows/seo-maintenance.yml setiap push ke main.
Tidak mengubah isi artikel, judul, atau CSS. Tidak menambahkan em-dash (U+2014).
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
from datetime import datetime, timezone, timedelta

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://berita.hifdi.id"
WIB = timezone(timedelta(hours=7))
ORG = "Himpunan Fasyankes Dokter Indonesia (HIFDI)"
LOGO = BASE + "/images/logo-hifdi.png"

BULAN = {
    "januari": 1, "februari": 2, "maret": 3, "april": 4, "mei": 5, "juni": 6,
    "juli": 7, "agustus": 8, "september": 9, "oktober": 10, "november": 11,
    "desember": 12,
}


def no_emdash(s: str) -> str:
    return s.replace("\u2014", "-").replace("\u2013", "-")


def strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    s = (s.replace("&ldquo;", '"').replace("&rdquo;", '"').replace("&amp;", "&")
         .replace("&nbsp;", " ").replace("&middot;", "·").replace("&#8217;", "'"))
    return re.sub(r"\s+", " ", s).strip()


def parse_date(text: str) -> datetime | None:
    m = re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", text or "")
    if not m:
        return None
    bulan = BULAN.get(m.group(2).lower())
    if not bulan:
        return None
    return datetime(int(m.group(3)), bulan, int(m.group(1)), 9, 0, tzinfo=WIB)


def git_date(path: pathlib.Path) -> datetime | None:
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%aI", "--", str(path)],
                             cwd=ROOT, capture_output=True, text=True, timeout=20).stdout.strip()
        return datetime.fromisoformat(out) if out else None
    except Exception:
        return None


def first(pattern: str, html: str, flags=re.S) -> str:
    m = re.search(pattern, html, flags)
    return strip_html(m.group(1)) if m else ""


def head_end(html: str) -> int:
    i = html.lower().find("</head>")
    return i if i >= 0 else html.lower().find("<body")


def add_canonical(html: str, url: str) -> tuple[str, bool]:
    head = html[:head_end(html)]
    if re.search(r'<link[^>]+rel=["\']canonical["\']', head, re.I):
        return html, False
    tag = '<link rel="canonical" href="%s">\n' % url
    i = head_end(html)
    # taruh setelah </title> kalau ada, kalau tidak tepat sebelum </head>
    m = re.search(r"</title>", head, re.I)
    if m:
        pos = m.end()
        return html[:pos] + "\n" + tag.rstrip("\n") + html[pos:], True
    return html[:i] + tag + html[i:], True


def add_jsonld(html: str, data: dict) -> tuple[str, bool]:
    head = html[:head_end(html)]
    if "application/ld+json" in head:
        return html, False
    block = ('<script type="application/ld+json">\n'
             + json.dumps(data, ensure_ascii=False, indent=2) + "\n</script>\n")
    i = head_end(html)
    return html[:i] + block + html[i:], True


def article_meta(path: pathlib.Path, html: str) -> dict:
    slug = path.parent.name
    url = "%s/%s/" % (BASE, slug)
    title = first(r"<title>(.*?)</title>", html, re.S)
    title = re.sub(r"\s+[\-\u2013\u2014]\s+(HIFDI|Berita HIFDI)\s*$", "", title).strip()
    desc = first(r'<meta name="description" content="(.*?)">', html)
    image = first(r'<meta property="og:image" content="(.*?)">', html)
    cat = first(r'<span class="article-category">(.*?)</span>', html)
    author = first(r'<div class="byline-name">(.*?)</div>', html)
    date_raw = first(r'<div class="article-meta">(.*?)</div>', html)
    dt = parse_date(date_raw) or parse_date(desc) or git_date(path) or datetime(2026, 1, 1, tzinfo=WIB)
    mod = git_date(path) or dt
    if mod < dt:
        mod = dt
    return {
        "slug": slug, "url": url, "title": no_emdash(title), "desc": no_emdash(desc),
        "image": image, "cat": no_emdash(cat), "author": no_emdash(author),
        "dt": dt, "mod": mod,
    }


def newsarticle_jsonld(m: dict) -> dict:
    author = m["author"] or "Redaksi Berita HIFDI"
    if "redaksi" in author.lower():
        author_obj = {"@type": "Organization", "name": author}
    else:
        author_obj = {"@type": "Person", "name": author}
    data = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "mainEntityOfPage": {"@type": "WebPage", "@id": m["url"]},
        "url": m["url"],
        "headline": m["title"][:110],
        "description": m["desc"],
        "image": [m["image"]] if m["image"] else [LOGO],
        "datePublished": m["dt"].isoformat(),
        "dateModified": m["mod"].isoformat(),
        "inLanguage": "id-ID",
        "author": author_obj,
        "publisher": {
            "@type": "Organization",
            "name": ORG,
            "alternateName": "HIFDI",
            "url": "https://hifdi.id",
            "logo": {"@type": "ImageObject", "url": LOGO},
        },
    }
    if m["cat"]:
        data["articleSection"] = m["cat"]
    return data


def homepage_jsonld() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "url": BASE + "/",
        "name": "Berita HIFDI",
        "inLanguage": "id-ID",
        "publisher": {
            "@type": "Organization",
            "name": ORG,
            "alternateName": "HIFDI",
            "url": "https://hifdi.id",
            "logo": {"@type": "ImageObject", "url": LOGO},
        },
    }


def main() -> None:
    changed_files, entries, canon, ld = [], [], 0, 0

    home = ROOT / "index.html"
    html = home.read_text(encoding="utf-8")
    new, c1 = add_canonical(html, BASE + "/")
    new, c2 = add_jsonld(new, homepage_jsonld())
    if c1 or c2:
        home.write_text(new, encoding="utf-8")
        changed_files.append(home.name)
    canon += int(c1)
    ld += int(c2)
    entries.append((BASE + "/", git_date(home) or datetime(2026, 10, 22, tzinfo=WIB), "1.0"))

    for d in sorted(ROOT.glob("article-*")):
        f = d / "index.html"
        if not f.is_file():
            continue
        html = f.read_text(encoding="utf-8")
        m = article_meta(f, html)
        new, c1 = add_canonical(html, m["url"])
        new, c2 = add_jsonld(new, newsarticle_jsonld(m))
        if c1 or c2:
            f.write_text(new, encoding="utf-8")
            changed_files.append(str(f.relative_to(ROOT)))
        canon += int(c1)
        ld += int(c2)
        entries.append((m["url"], m["mod"], "0.8"))

    # sitemap
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, mod, prio in entries:
        lines.append("  <url><loc>%s</loc><lastmod>%s</lastmod>"
                     "<changefreq>weekly</changefreq><priority>%s</priority></url>"
                     % (url, mod.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"), prio))
    lines.append("</urlset>")
    sitemap = "\n".join(lines) + "\n"
    sm = ROOT / "sitemap.xml"
    if not sm.exists() or sm.read_text(encoding="utf-8") != sitemap:
        sm.write_text(sitemap, encoding="utf-8")
        changed_files.append("sitemap.xml")

    robots = ("# robots.txt Berita HIFDI\n"
              "User-agent: *\n"
              "Allow: /\n"
              "Disallow: /scripts/\n"
              "Disallow: /*.json$\n"
              "\n"
              "Sitemap: %s/sitemap.xml\n" % BASE)
    rb = ROOT / "robots.txt"
    if not rb.exists() or rb.read_text(encoding="utf-8") != robots:
        rb.write_text(robots, encoding="utf-8")
        changed_files.append("robots.txt")

    print("canonical ditambah: %d | JSON-LD ditambah: %d | URL sitemap: %d"
          % (canon, ld, len(entries)))
    print("berkas berubah:", ", ".join(changed_files[:8]) + (" ..." if len(changed_files) > 8 else ""))


if __name__ == "__main__":
    main()
