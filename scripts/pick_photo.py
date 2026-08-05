#!/usr/bin/env python3
"""Sistem gilir foto HIFDI (versi repo).

Pemakaian:
  python3 scripts/pick_photo.py cat-01            -> cetak path foto terpilih
  python3 scripts/pick_photo.py cat-01 --dry-run  -> lihat pilihan tanpa mencatat
  python3 scripts/pick_photo.py --status          -> ringkasan pemakaian
  python3 scripts/pick_photo.py cat-01 --article 065  -> catat nomor artikel

Foto disimpan di images/foto/<kategori>/. Registry di scripts/photo_registry.json.
Aturan: pilih foto yang PALING JARANG dipakai (used terkecil) -> rotasi merata.
"""
import json, os, sys, argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(BASE, 'scripts', 'photo_registry.json')
IMGDIR = os.path.join(BASE, 'images', 'foto')

def load():
    with open(REG) as f:
        return json.load(f)

def save(reg):
    with open(REG, 'w') as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('category', nargs='?', help='kode kategori, misal cat-01')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--status', action='store_true')
    ap.add_argument('--article', default=None, help='nomor artikel (misal 065)')
    a = ap.parse_args()

    reg = load()

    if a.status:
        for k in sorted(reg):
            items = reg[k]
            used = sum(1 for i in items if i.get('used', 0) > 0)
            print(f'{k}: {used}/{len(items)} terpakai')
        return

    if not a.category:
        print('Gunakan: pick_photo.py <kode-kategori> [--dry-run] [--article XXX] | --status')
        sys.exit(1)

    k = a.category
    d = os.path.join(IMGDIR, k)
    files = sorted(f for f in os.listdir(d) if f.endswith('.jpg') and not f.endswith('-og.jpg')) if os.path.isdir(d) else []
    if not files:
        print(f'Kategori {k} kosong — belum ada foto.')
        sys.exit(1)

    known = {i['file']: i for i in reg.get(k, [])}
    for fn in files:
        if fn not in known:
            known[fn] = {'file': fn, 'used': 0, 'last_article': None, 'source': None, 'license': None}

    items = sorted(known.values(), key=lambda i: (i['used'], i['file']))
    pick = items[0]

    if not a.dry_run:
        pick['used'] += 1
        if a.article:
            pick['last_article'] = a.article
        reg[k] = list(known.values())
        save(reg)
        print(os.path.join(d, pick['file']))
    else:
        print(f'[dry-run] pilih: {pick["file"]} (sudah {pick["used"]}x)')

if __name__ == '__main__':
    main()
