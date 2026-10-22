#!/usr/bin/env python3
"""Verifikasi live: sitemap valid, semua URL 200 (sampel), JSON-LD live terparse."""
import json, random, re, urllib.request, xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()


st, body = get("https://berita.hifdi.id/sitemap.xml")
root = ET.fromstring(body)
locs = [e.text for e in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
print("sitemap: HTTP", st, "| URL:", len(locs), "| unik:", len(set(locs)))

random.seed(7)
sampel = ["https://berita.hifdi.id/"] + random.sample(locs, 6)
hasil = []
for u in sampel:
    try:
        s, _ = get(u)
    except Exception as e:
        s = "ERR %s" % e
    hasil.append((s, u))
print("sampel status:", hasil)

# JSON-LD di halaman live
for page in ["https://berita.hifdi.id/article-013/", "https://berita.hifdi.id/article-108/",
             "https://berita.hifdi.id/"]:
    _, html = get(page)
    h = html.decode("utf-8", "ignore")
    m = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S)
    if not m:
        print("JSON-LD HILANG:", page)
        continue
    d = json.loads(m.group(1))
    print("%-45s %s | %s | %s" % (page, d.get("@type"),
                                  (d.get("headline") or d.get("name"))[:45],
                                  d.get("datePublished", "-")))
