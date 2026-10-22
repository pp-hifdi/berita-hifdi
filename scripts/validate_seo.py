#!/usr/bin/env python3
"""Validasi hasil seo_refresh: JSON-LD terparse, canonical unik, tidak ada em-dash baru."""
import json, pathlib, re, sys

ROOT = pathlib.Path("/home/hermes/workspace/berita-hifdi")
bad, no_canon, seen = [], [], {}
files = [ROOT / "index.html"] + sorted(ROOT.glob("article-*/index.html"))

for f in files:
    h = f.read_text(encoding="utf-8")
    blocks = re.findall(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S)
    if len(blocks) != 1:
        bad.append((f.name, "jumlah ld+json=%d" % len(blocks)))
        continue
    try:
        d = json.loads(blocks[0])
    except Exception as e:
        bad.append((f.name, "json error %s" % e))
        continue
    if "\u2014" in blocks[0]:
        bad.append((f.name, "em-dash di JSON-LD"))
    can = re.findall(r'<link rel="canonical" href="([^"]+)"', h)
    if len(can) != 1:
        no_canon.append((f.name, len(can)))
    else:
        seen.setdefault(can[0], []).append(f.name)
    if f.parent.name != ROOT.name:
        if not d.get("datePublished") or not d.get("headline"):
            bad.append((f.name, "field wajib kosong"))

dupes = {k: v for k, v in seen.items() if len(v) > 1}
print("berkas diperiksa:", len(files))
print("JSON-LD bermasalah:", len(bad), bad[:5])
print("canonical bukan 1:", len(no_canon), no_canon[:5])
print("canonical duplikat:", len(dupes), list(dupes.items())[:3])
sys.exit(1 if (bad or no_canon or dupes) else 0)
