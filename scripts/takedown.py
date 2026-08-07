#!/usr/bin/env python3
"""Take down artikel Berita HIFDI — level Admin HIFDI (taktis, tanpa ACC Sekjen).

Pemakaian:
  python3 scripts/takedown.py 072 --tarik    # pindah ke _ditarik/ (link 404, reversibel)
  python3 scripts/takedown.py 072 --hapus    # git rm permanen (kasus serius)
  python3 scripts/takedown.py 072 --dry-run  # lihat rencana tanpa mengubah apa pun

Keduanya: hapus kartu dari index.html + turunkan articleCount. Setelah eksekusi
WAJIB: (1) update STATUS-SEKJEN.md, (2) kalau caption sudah tersebar di WAG/
Telegram kirim pesan koreksi/pencabutan, (3) verifikasi live (kartu hilang,
count turun, halaman 404/terpindah). Detail: docs/SOP-TAKE-DOWN.md.
"""
import argparse
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(BASE, "index.html")


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, cwd=BASE, capture_output=True, text=True, **kw)


def find_card(index_html, num):
    """Cari blok kartu artikel num di index.html -> (start, end) atau None."""
    pat = re.compile(
        rf'\n\s*<!-- ARTIKEL {num:03d}[^\n]*-->\n\s*<a class="article-card" href="\./article-{num:03d}/".*?</a>\n',
        re.S,
    )
    m = pat.search(index_html)
    return (m.start(), m.end()) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("num", type=int, help="nomor artikel, mis. 72")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--tarik", action="store_true", help="pindah ke _ditarik/ (reversibel)")
    g.add_argument("--hapus", action="store_true", help="hapus permanen (git rm)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    num = a.num
    src = os.path.join(BASE, f"article-{num:03d}")
    if not os.path.isdir(src):
        print(f"ERROR: {src} tidak ada")
        sys.exit(1)

    index_html = open(INDEX, encoding="utf-8").read()
    card = find_card(index_html, num)
    if not card:
        print(f"ERROR: kartu article-{num:03d} tidak ditemukan di index.html")
        sys.exit(1)

    count_m = re.search(r">(\d+) artikel<", index_html)
    new_count = max(1, int(count_m.group(1)) - 1) if count_m else None

    print(f"RENCANA take down article-{num:03d}:")
    print(f"  1. {'git mv' if a.tarik else 'git rm -r'} article-{num:03d}" +
          (" -> _ditarik/" if a.tarik else ""))
    print(f"  2. hapus kartu dari index.html (baris {index_html[:card[0]].count(chr(10))+1}..{index_html[:card[1]].count(chr(10))+1})")
    if new_count:
        print(f"  3. articleCount {count_m.group(1)} -> {new_count}")
    print("  4. commit + push; lalu STATUS-SEKJEN + pesan koreksi WAG + verifikasi live")

    if a.dry_run:
        print("DRY-RUN — tidak ada yang diubah")
        sys.exit(0)

    # 1. pindah/hapus folder artikel
    if a.tarik:
        dst_dir = os.path.join(BASE, "_ditarik")
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, f"article-{num:03d}")
        if os.path.isdir(dst):
            print(f"ERROR: {dst} sudah ada")
            sys.exit(1)
        r = sh(f"git mv article-{num:03d} _ditarik/article-{num:03d}")
    else:
        r = sh(f"git rm -r -q article-{num:03d}")
    if r.returncode != 0:
        print("ERROR git:", r.stderr.strip()[:300])
        sys.exit(1)

    # 2. hapus kartu
    new_html = index_html[: card[0]] + index_html[card[1]:]
    # 3. turunkan count
    if new_count:
        new_html = new_html.replace(
            f">{count_m.group(1)} artikel<", f">{new_count} artikel<", 1
        )
    open(INDEX, "w", encoding="utf-8").write(new_html)
    sh("git add index.html")

    print("SELESAI — langkah lokal selesai. Sekarang:")
    print(f"  git commit -m 'takedown article-{num:03d} ({'tarik' if a.tarik else 'hapus'})'")
    print("  git push")
    print("  lalu: STATUS-SEKJEN.md + pesan koreksi WAG + verifikasi live")


if __name__ == "__main__":
    main()
