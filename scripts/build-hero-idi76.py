#!/usr/bin/env python3
"""Hero artikel HUT IDI ke-76 (1200x675).

Tata letak sesuai arahan Prinsipal (24 Okt 2026):
  - logo IDI BESAR, mengambil sekitar separuh kanvas,
  - kutipan Ketua Umum HIFDI di sisi kanan,
  - logo HIFDI kecil di bawah, menyatu dengan strip seperti running text.
"""
import pathlib
import subprocess

INV = pathlib.Path("/home/hermes/workspace/berita-hifdi")
OUT = INV / "images"
IDI = "file:///home/hermes/workspace/berita-hifdi/images/logo-idi-hd.png"
HIFDI = "file:///home/hermes/workspace/berita-hifdi/images/logo-hifdi.png"

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'PlayfairDisplay'; src:url('file:///home/hermes/.fonts/PlayfairDisplay.ttf'); }}
@font-face {{ font-family:'DMSans'; src:url('file:///home/hermes/.fonts/DMSans.ttf'); font-weight:300 700; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1200px; height:675px; overflow:hidden; }}
.canvas {{ position:relative; width:1200px; height:675px; background:#FFFFFF;
          display:flex; font-family:'DMSans',sans-serif; }}

.kiri {{ width:600px; display:flex; align-items:center; justify-content:center;
         padding-bottom:66px; }}
.kiri img {{ width:452px; height:452px; }}

.garis {{ width:1px; background:#E4E8E4; margin:54px 0 120px; }}

.kanan {{ flex:1; padding:66px 72px 92px 60px; }}
.label {{ font-size:17px; letter-spacing:0.22em; text-transform:uppercase;
          color:#8A9490; font-weight:500; }}
.angka {{ font-family:'PlayfairDisplay',serif; font-size:64px; font-weight:700;
          color:#1B4028; line-height:1; margin-top:18px; }}
.angka span {{ color:#E8AB28; }}
.kutip {{ font-family:'PlayfairDisplay',serif; font-style:italic; font-size:26px;
          line-height:1.42; color:#1B4028; margin-top:22px; }}
.sumber {{ font-size:15px; letter-spacing:0.12em; text-transform:uppercase;
           color:#5F6B63; margin-top:20px; line-height:1.5; }}

.strip {{ position:absolute; left:0; right:0; bottom:0; height:66px;
          background:#1B4028; display:flex; align-items:center;
          justify-content:space-between; padding:0 40px; }}
.strip .kiri2 {{ display:flex; align-items:center; gap:12px; }}
.strip img {{ width:40px; height:40px; border-radius:50%; }}
.strip .nm {{ color:#FFFFFF; font-size:17px; letter-spacing:0.16em;
              text-transform:uppercase; font-weight:500; }}
.strip .rt {{ color:#BFD3C5; font-size:14px; letter-spacing:0.14em;
              text-transform:uppercase; }}
.strip .rt b {{ color:#E8AB28; font-weight:500; }}
</style></head><body>
<div class="canvas">
  <div class="kiri"><img src="{IDI}"></div>
  <div class="garis"></div>
  <div class="kanan">
    <div class="label">HUT IDI ke-76 &middot; 24 Oktober 2026</div>
    <div class="angka">76 <span>tahun</span></div>
    <div class="kutip">&ldquo;Bagi IDI, ini berarti berani keluar dari menara gading klinis dan menerjemahkan temuan ilmu kedokteran yang teknis ke dalam bahasa anggaran serta kebijakan publik, tanpa kehilangan independensi ilmiah yang menjadi sumber kredibilitasnya.&rdquo;</div>
    <div class="sumber">dr. Zaenal Abidin, M.H.<br>Ketua Umum HIFDI</div>
  </div>
  <div class="strip">
    <div class="kiri2"><img src="{HIFDI}"><div class="nm">HIFDI</div></div>
    <div class="rt">Himpunan Fasyankes Dokter Indonesia &nbsp;&middot;&nbsp; hifdi.id &nbsp;&middot;&nbsp; <b>Selamat Hari Dokter Nasional</b></div>
  </div>
</div></body></html>"""

(INV / "raw").mkdir(exist_ok=True)
html = INV / "raw" / "hero-idi76.html"
html.write_text(HTML, encoding="utf-8")
png = INV / "raw" / "article-109-idi76-hero.png"
subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
                "--hide-scrollbars", "--force-device-scale-factor=1",
                "--window-size=1200,675", "--virtual-time-budget=3000",
                "--screenshot=%s" % png, "file://%s" % html],
               check=True, capture_output=True)

from PIL import Image
im = Image.open(png)
print("png", im.size)
dst = OUT / "article-109-idi76-hero.jpg"
im.convert("RGB").save(dst, quality=90, optimize=True)
print("ok", dst)
