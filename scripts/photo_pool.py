#!/usr/bin/env python3
"""Kolam foto HIFDI — modul gilir untuk dipakai generate_article.py (dan CLI).

pools = {"KategoriEditorial": ["cat-XX", ...]} -> definisi di config.py.
Semua state (pemakaian) di scripts/photo_registry.json.
"""
import json, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(REPO, 'scripts', 'photo_registry.json')
IMGDIR = os.path.join(REPO, 'images', 'foto')
SITE = 'https://berita.hifdi.id/images/'


def load_registry():
    if os.path.exists(REG):
        with open(REG, encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_registry(reg):
    with open(REG, 'w', encoding='utf-8') as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)


def pick(category, article_no=None, pools=None):
    """Pilih foto paling jarang dipakai dari kolam kategori editorial.

    Mengembalikan dict gambar (local=True) atau None bila kolam kosong.
    Pemakaian foto langsung dicatat ke registry (rotasi merata).
    """
    if not pools or not pools.get(category):
        return None
    reg = load_registry()
    for cat in pools[category]:
        d = os.path.join(IMGDIR, cat)
        files = sorted(
            f for f in os.listdir(d)
            if f.endswith('.jpg') and not f.endswith('-og.jpg')
        ) if os.path.isdir(d) else []
        if not files:
            continue
        # Registry: hanya entri yang file-nya BENAR-BENAR ADA di disk dan
        # tidak berstatus excluded (foto dibuang) — bug nyata 6 Agu 2026:
        # cat-12-001 (excluded, file dipindah ke _ditolak/) tetap ikut
        # kompetisi rotasi karena known diisi dari registry, menang (used=0),
        # lalu dipakai article-069 -> gambar 404.
        known = {}
        for i in reg.get(cat, []):
            if i.get('status') == 'excluded':
                continue
            if i['file'] in files:
                known[i['file']] = i
        for fn in files:
            if fn not in known:
                known[fn] = {'file': fn, 'used': 0, 'last_article': None}
        # paling jarang dipakai -> rotasi merata
        chosen = sorted(known.values(), key=lambda i: (i['used'], i['file']))[0]
        chosen['used'] += 1
        if article_no:
            chosen['last_article'] = article_no
        reg[cat] = list(known.values())
        save_registry(reg)
        base = chosen['file'][:-4]
        return {
            'local': True,
            'id': f'foto/{cat}/{chosen["file"]}',
            'og': f'foto/{cat}/{base}-og.jpg',
            'alt': 'Ilustrasi',
        }
    return None


def url(image, variant='display'):
    """URL absolut di situs untuk gambar lokal; None bila bukan lokal."""
    if not image or not image.get('local'):
        return None
    key = 'og' if variant == 'og' else 'id'
    return SITE + image[key]


if __name__ == '__main__':
    import sys
    cat = sys.argv[1] if len(sys.argv) > 1 else 'Advokasi'
    pools = {'Advokasi': ['cat-10', 'cat-12']}
    r = pick(cat, pools=pools)
    print(r if r else 'kolam kosong')
