#!/usr/bin/env python3
"""Ambil logo IDI bersih dari poster HUT IDI ke-76 kiriman Prinsipal.

Latar poster krem (#f7f4ee). Langkah:
  1. deteksi bounding box logo (piksel yang jauh dari warna latar) di area atas,
  2. crop dengan padding,
  3. hapus latar dengan flood fill dari tepi (bukan threshold global) supaya
     putih di dalam lambang IDI tetap utuh.
"""
from PIL import Image, ImageDraw

SRC = "/home/hermes/.hermes/profiles/hifdi/cache/images/img_ec26fd28dd15.jpg"
DST = "/home/hermes/workspace/berita-hifdi/images/logo-idi.png"

im = Image.open(SRC).convert("RGB")
REGION = (500, 10, 800, 225)
reg = im.crop(REGION)
px = reg.load()
w, h = reg.size
xs, ys = [], []
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        # latar krem: semua kanal > 225 dan selisih antar kanal kecil
        if r > 225 and g > 220 and b > 210 and (r - b) < 25:
            continue
        xs.append(x)
        ys.append(y)
print("bbox di region:", min(xs), min(ys), max(xs), max(ys))

pad = 6
box = (REGION[0] + min(xs) - pad, REGION[1] + min(ys) - pad,
       REGION[0] + max(xs) + pad, REGION[1] + max(ys) + pad)
lg = im.crop(box)
lw, lh = lg.size
for pt in [(0, 0), (lw - 1, 0), (0, lh - 1), (lw - 1, lh - 1)]:
    ImageDraw.floodfill(lg, pt, (255, 0, 255), thresh=30)

rgba = lg.convert("RGBA")
p2 = rgba.load()
for y in range(lh):
    for x in range(lw):
        r, g, b, a = p2[x, y]
        if abs(r - 255) < 12 and g < 14 and abs(b - 255) < 12:
            p2[x, y] = (0, 0, 0, 0)
rgba = rgba.crop(rgba.getbbox())
rgba.save(DST)
print("ok", DST, rgba.size, "dari crop", (lw, lh))
