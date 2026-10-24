#!/usr/bin/env python3
"""Tempel beberapa logo (baris kanan bawah) ke ilustrasi hasil generate.

Dipakai untuk artikel HUT IDI ke-76: hero membawa logo HIFDI (yang memberi
ucapan) dan logo IDI (yang berulang tahun), bersebelahan di kanan bawah.

Contoh:
  python3 tempel-logo-baris.py --src raw/hero.png --dst images/article-109-idi76.jpg \
      --logo images/logo-hifdi.png:0.085 --logo images/logo-idi.png:0.13 --out-size 1200x675
"""
import argparse

from PIL import Image, ImageDraw, ImageFilter


def logo_rgba(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    for pt in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        ImageDraw.floodfill(im, pt, (255, 0, 255), thresh=32)
    im = im.convert("RGBA")
    px = im.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if abs(r - 255) < 14 and g < 16 and abs(b - 255) < 14:
                px[x, y] = (0, 0, 0, 0)
    return im.crop(im.getbbox())


def plate(d, radius_frac=0.5):
    pd = d + max(10, d // 10)
    p = Image.new("RGBA", (pd, pd), (0, 0, 0, 0))
    ImageDraw.Draw(p).ellipse((0, 0, pd - 1, pd - 1), fill=(255, 255, 255, 228))
    sh = Image.new("RGBA", (pd + 26, pd + 26), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((13, 13, 13 + pd, 13 + pd), fill=(0, 0, 0, 85))
    return p, sh.filter(ImageFilter.GaussianBlur(7)), pd


def run(src, dst, logos, out_w, out_h, margin_frac=0.028, gap_frac=0.012):
    base = Image.open(src).convert("RGB")
    tr = out_w / out_h
    w, h = base.size
    if w / h > tr:
        nw = int(h * tr)
        base = base.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
    else:
        nh = int(w / tr)
        base = base.crop((0, (h - nh) // 2, w, (h + nh) // 2))
    base = base.resize((out_w, out_h), Image.LANCZOS).convert("RGBA")

    m = int(out_w * margin_frac)
    gap = int(out_w * gap_frac)
    items = []
    for path, frac in logos:
        d = int(out_w * frac)
        p, sh, pd = plate(d)
        lg = logo_rgba(path)
        # jaga rasio asli logo di dalam piringan
        lh = int(d * lg.height / lg.width)
        lg = lg.resize((d, lh), Image.LANCZOS)
        items.append((lg, p, sh, pd))

    right = out_w - m
    y_bottom = out_h - m
    for lg, p, sh, pd in reversed(items):
        x0 = right - pd
        y0 = y_bottom - pd
        base.alpha_composite(sh, (x0 - 13, y0 - 8))
        base.alpha_composite(p, (x0, y0))
        base.alpha_composite(lg, (x0 + (pd - lg.width) // 2,
                                  y0 + (pd - lg.height) // 2))
        right = x0 - gap

    base.convert("RGB").save(dst, quality=88, optimize=True)
    print("ok", dst, (out_w, out_h))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--logo", action="append", required=True,
                    help="path:frac, urut kiri ke kanan")
    ap.add_argument("--out-size", default="1200x675")
    a = ap.parse_args()
    logos = []
    for spec in a.logo:
        path, _, frac = spec.rpartition(":")
        logos.append((path, float(frac)))
    W, H = (int(x) for x in a.out_size.lower().split("x"))
    run(a.src, a.dst, logos, W, H)
