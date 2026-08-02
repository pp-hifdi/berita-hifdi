#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot harian Berita HIFDI — dijalankan GitHub Actions sekali sehari (06.00 WIB).

ALUR:
  1. Tarik 10 feed RSS (Indonesia + internasional) yang sudah diuji hidup.
  2. Saring judul dengan kata kunci relevan HIFDI; buang yang mirip artikel lama.
  3. Ambil isi berita terpilih.
  4. Kirim ke DeepSeek bersama aturan gaya + Posisi HIFDI -> naskah artikel.
  5. Rakit HTML dari template artikel lama, sisipkan kartu, naikkan articleCount.
  6. Workflow yang commit + push. Cloudflare build sendiri.

PRINSIP YANG TIDAK BOLEH DILANGGAR:
  - Fakta SELALU bersandar pada berita nyata dari RSS. Model hanya menulis
    SIKAP HIFDI atas berita itu. Kotak Referensi memuat URL asli dari feed.
  - Gambar HANYA dari daftar putih terkurasi di config.py (sudah diverifikasi
    visual). Bot tidak bisa melihat gambar, jadi haram menebak dari alt text.

Keluar dengan kode 0 tanpa menulis apa pun kalau tidak ada kandidat layak —
itu bukan kegagalan, cuma hari yang sepi berita relevan.
"""

import html
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

import feedparser
from openai import OpenAI

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (  # noqa: E402
    BLOCKLIST, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, DEFAULT_IMAGE, FEEDS, IMAGES,
    IMAGE_BY_CATEGORY, KEYWORDS_MEDIUM, KEYWORDS_STRONG, KEYWORDS_WEAK,
    MAX_SOURCE_CHARS, MIN_SCORE, MIN_TITLE_WORDS,
)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(REPO, "index.html")
WIB = timezone(timedelta(hours=7))
BULAN_ID = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
            "Agustus", "September", "Oktober", "November", "Desember"]


def log(msg):
    print(f"[bot] {msg}", flush=True)


def notify_telegram(text):
    """Lapor ke Telegram. Tidak fatal kalau gagal.

    KENAPA TELEGRAM, BUKAN WHATSAPP: bot ini jalan di server GitHub, sementara
    gateway OpenWA hidup di laptop pemilik repo (localhost:2785) yang tidak bisa
    dijangkau dari luar. Telegram punya endpoint HTTPS publik, jadi bisa.
    Caption WA dikirim sebagai pesan terpisah supaya gampang diteruskan ke WAG.

    Token & chat id dibaca dari env (GitHub Secrets) — TIDAK PERNAH di repo.
    """
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        log("TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID belum diset — lapor dilewati.")
        return
    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            if resp.status != 200:
                log(f"lapor Telegram gagal: HTTP {resp.status}")
    except Exception as exc:
        log(f"lapor Telegram gagal: {exc}")


# --------------------------------------------------------------------------
# 1. Keadaan repo sekarang
# --------------------------------------------------------------------------
def read_index():
    with open(INDEX, encoding="utf-8") as f:
        return f.read()


def existing_titles(index_html):
    """Judul kartu yang sudah tayang — dipakai supaya topik tidak diulang."""
    return re.findall(r'<div class="card-title">(.*?)</div>', index_html, re.S)


def next_article_number():
    """Nomor folder article-XXX tertinggi + 1."""
    nums = [
        int(m.group(1))
        for name in os.listdir(REPO)
        if (m := re.fullmatch(r"article-(\d{3})", name))
        and os.path.isdir(os.path.join(REPO, name))
    ]
    if not nums:
        raise SystemExit("Tidak menemukan folder article-XXX sama sekali.")
    return max(nums) + 1


def template_path():
    """Template = artikel bernomor tertinggi (struktur terbukti tayang)."""
    return os.path.join(REPO, f"article-{next_article_number() - 1:03d}", "index.html")


# --------------------------------------------------------------------------
# 2. Kandidat dari RSS
# --------------------------------------------------------------------------
def normalise(text):
    return re.sub(r"[^a-z0-9 ]", " ", (text or "").lower())


def relevance_score(title):
    """Skor berbobot. 0 = tolak.

    Biner tidak cukup: kata umum seperti 'dokter' muncul di hampir semua
    artikel kesehatan konsumen. Kata kunci KUAT (BPJS, FKTP, akreditasi,
    primary care, health policy) bernilai 10 dan cukup sendirian; kata SEDANG
    bernilai 3 dan perlu berteman; kata LEMAH bernilai 1 dan tidak akan pernah
    meloloskan judul sendirian.
    """
    t = normalise(title)
    if any(b in t for b in BLOCKLIST):
        return 0
    score = 0
    score += 10 * sum(1 for k in KEYWORDS_STRONG if k in t)
    score += 3 * sum(1 for k in KEYWORDS_MEDIUM if k in t)
    score += 1 * sum(1 for k in KEYWORDS_WEAK if k in t)
    return score if score >= MIN_SCORE else 0


def too_similar(title, old_titles):
    """Tolak kalau berbagi banyak kata bermakna dengan judul lama."""
    words = {w for w in normalise(title).split() if len(w) > 4}
    if not words:
        return True
    for old in old_titles:
        old_words = {w for w in normalise(old).split() if len(w) > 4}
        if old_words and len(words & old_words) / len(words) > 0.5:
            return True
    return False


def collect_candidates(old_titles):
    """Kumpulkan kandidat dari semua feed, lalu URUTKAN BERDASAR SKOR.

    Urutan feed TIDAK boleh menentukan pilihan: Detik menyumbang 100 item
    sementara Health Affairs cuma 16, jadi kalau diambil berdasar urutan,
    sumber kebijakan yang paling relevan tidak akan pernah terpilih.
    """
    # feedparser memakai User-Agent sendiri yang diblokir sebagian situs
    # (MedicalXpress balas kosong tanpa ini, padahal via curl 30 item).
    feedparser.USER_AGENT = (
        "Mozilla/5.0 (compatible; BeritaHIFDI-bot/1.0; +https://berita.hifdi.id/)"
    )

    seen_links, candidates = set(), []
    for source_name, url in FEEDS:
        try:
            parsed = feedparser.parse(url)
        except Exception as exc:                      # feed mati / berubah
            log(f"feed gagal: {source_name} ({exc})")
            continue
        if not parsed.entries:
            log(f"feed kosong: {source_name}")
            continue
        kept = 0
        for entry in parsed.entries:
            # Sebagian feed (mis. Fierce Healthcare) menaruh HTML mentah di
            # kolom judul: '<a href="...">Judul</a>'. Bersihkan tag + entitas,
            # kalau tidak judul artikel kita ikut berisi potongan markup.
            title = html.unescape(re.sub(r"<[^>]+>", " ", entry.get("title") or ""))
            title = re.sub(r"\s+", " ", title).strip()
            link = (entry.get("link") or "").strip()
            if not title or not link or link in seen_links:
                continue
            if len(title.split()) < MIN_TITLE_WORDS:
                continue
            score = relevance_score(title)
            if not score:
                continue
            if too_similar(title, old_titles):
                continue
            seen_links.add(link)
            summary = re.sub(r"<[^>]+>", " ", entry.get("summary", ""))
            candidates.append({
                "source": source_name,
                "title": title,
                "link": link,
                "score": score,
                "summary": re.sub(r"\s+", " ", summary).strip(),
            })
            kept += 1
        log(f"{source_name}: {len(parsed.entries)} item -> {kept} lolos")

    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates


# --------------------------------------------------------------------------
# 3. DeepSeek
# --------------------------------------------------------------------------
SYSTEM_PROMPT = """Kamu penulis untuk portal Berita HIFDI (Himpunan Fasyankes Dokter Indonesia).
HIFDI menaungi Fasilitas Kesehatan Tingkat Pertama: klinik pratama, Tempat Praktik
Mandiri Dokter (TPMD), dan puskesmas. Portal ini bukan agregator berita — setiap
artikel WAJIB memuat sikap organisasi.

SUARA EDITORIAL (pegang erat):
- FKTP swasta sistematis terpinggirkan: menanggung porsi besar kepesertaan JKN,
  tapi hampir selalu di luar skema penguatan (APBN, hibah, pengadaan alat).
- Beban setara, dukungan timpang: kontrak dan standar sama dengan fasyankes
  pemerintah, tapi biaya pemenuhannya ditanggung sendiri.
- Layanan primer adalah hulu, bukan pelengkap.
- Berbasis bukti, bukan sentimen. Menuntut, bukan memohon. Tetap konstruktif.

ATURAN KERAS:
- DILARANG mengarang fakta, angka, nama, tanggal, nomor peraturan, atau sumber.
  Kamu HANYA boleh memakai fakta yang ada di berita sumber yang diberikan.
  Kalau sebuah detail tidak ada di sumber, jangan sebut.
- Kalau sumbernya berita luar negeri, tarik relevansinya ke layanan primer
  Indonesia — jangan sekadar menerjemahkan.
- Bahasa Indonesia baku jurnalistik, ±500 kata. Sikap tajam lewat data, bukan
  kata sifat berlebihan.

STRUKTUR BADAN ARTIKEL (HTML, berurutan):
1. <p> pembuka — konteks isu, sebut sumber dan tanggalnya.
2. 2-3 bagian <h2> — uraian isu, data, dampak konkret ke FKTP.
3. Satu <blockquote><p>...</p></blockquote> — satu kalimat sorotan.
4. <h2>Posisi HIFDI</h2> — sikap organisasi (nada mengikuti kategori).
5. <h2>Penutup</h2> — satu paragraf.
Hanya tag <p>, <h2>, <blockquote>, <em>, <strong>. Tanpa <html>/<body>/<div>.
JANGAN tulis kotak Referensi — skrip yang menambahkannya.

KATEGORI dan nada Posisi HIFDI:
- "Advokasi": kebijakan/regulasi berdampak ke FKTP. Tajam. 2-3 tuntutan konkret.
- "Edukasi": literasi medis/panduan klinis. Menjelaskan. 2 poin: yang didukung,
  yang perlu diperbaiki.
- "Mutu": standar layanan, akreditasi, RME/SATUSEHAT. Evaluatif-teknis.
- "Kabar HIFDI": kegiatan organisasi. Hangat.

Balas HANYA JSON valid dengan kunci:
  title            judul artikel (bukan terjemahan mentah judul sumber)
  subtitle         satu kalimat rangkuman
  category         salah satu: Advokasi | Edukasi | Mutu | Kabar HIFDI
  meta_description ringkasan <=200 karakter
  body_html        badan artikel sesuai struktur di atas
  caption          caption WhatsApp: judul dibungkus *bold*, 2-3 paragraf
                   pendek, tanpa menyertakan link (skrip yang menambahkan)
"""


def call_deepseek(candidate):
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise SystemExit("DEEPSEEK_API_KEY tidak ada. Set di GitHub Secrets.")

    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
    today = datetime.now(WIB)
    user_prompt = (
        f"Tanggal hari ini: {today.day} {BULAN_ID[today.month]} {today.year}.\n\n"
        f"BERITA SUMBER (satu-satunya sumber fakta yang boleh kamu pakai):\n"
        f"Media  : {candidate['source']}\n"
        f"Judul  : {candidate['title']}\n"
        f"Tautan : {candidate['link']}\n"
        f"Isi    : {candidate['summary'][:MAX_SOURCE_CHARS]}\n\n"
        f"Tulis artikel Berita HIFDI atas berita ini."
    )

    resp = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.6,
        max_tokens=4000,
    )
    raw = resp.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.M).strip()
    data = json.loads(raw)

    for key in ("title", "subtitle", "category", "body_html", "caption"):
        if not data.get(key):
            raise SystemExit(f"Balasan model tidak lengkap: '{key}' kosong.")
    if data["category"] not in IMAGE_BY_CATEGORY:
        data["category"] = "Advokasi"
    data.setdefault("meta_description", data["subtitle"])
    return data


# --------------------------------------------------------------------------
# 4. Rakit HTML
# --------------------------------------------------------------------------
def build_article_html(tpl, article, image, candidate, date_str):
    """Ganti bagian isi pada salinan template.

    `tpl` HARUS sudah dibaca sebelum folder artikel baru dibuat — kalau tidak,
    next_article_number() akan ikut menghitung folder kosong yang baru dibuat
    dan template-nya jadi menunjuk ke berkas yang belum ada.
    """
    esc = lambda s: html.escape(s, quote=True)
    img_big = f"https://images.unsplash.com/{image['id']}?auto=format&fit=crop&w=1200&h=630&q=80"

    sources = (
        '<div class="sources-box">\n<div class="sources-title">Referensi</div>\n<ul>\n'
        f'<li>{esc(candidate["source"])}, "{esc(candidate["title"])}" — '
        f'<a href="{esc(candidate["link"])}">{esc(candidate["link"])}</a></li>\n'
        "</ul>\n</div>"
    )
    body = f'<div class="article-body">\n{article["body_html"]}\n\n{sources}\n</div>'

    def sub(pattern, repl, text, flags=0):
        new, n = re.subn(pattern, lambda _m: repl, text, count=1, flags=flags)
        if n == 0:
            raise SystemExit(f"Template tidak cocok pola: {pattern[:60]}")
        return new

    t = tpl
    t = sub(r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{esc(article["meta_description"])}">', t)
    t = sub(r'<meta property="og:title" content="[^"]*">',
            f'<meta property="og:title" content="{esc(article["title"])} — HIFDI">', t)
    t = sub(r'<meta property="og:description" content="[^"]*">',
            f'<meta property="og:description" content="{esc(article["subtitle"])}">', t)
    t = sub(r'<meta property="og:image" content="[^"]*">',
            f'<meta property="og:image" content="{img_big}">', t)
    t = sub(r"<title>.*?</title>", f'<title>{esc(article["title"])} — HIFDI</title>', t, re.S)
    t = sub(r'<span class="article-category">.*?</span>',
            f'<span class="article-category">{esc(article["category"])}</span>', t, re.S)
    t = sub(r'<h1 class="article-title">.*?</h1>',
            f'<h1 class="article-title">{esc(article["title"])}</h1>', t, re.S)
    t = sub(r'<div class="article-subtitle">.*?</div>',
            f'<div class="article-subtitle">{esc(article["subtitle"])}</div>', t, re.S)
    t = sub(r'<div class="article-meta">.*?</div>',
            ('<div class="article-meta">\n'
             f"<span>{date_str}</span>\n<span>Redaksi Berita HIFDI</span>\n"
             f'<span>{esc(article["category"])}</span>\n</div>'), t, re.S)
    t = sub(r'<img class="featured-image"[^>]*>',
            f'<img class="featured-image" src="{img_big}" alt="{esc(image["alt"])}">', t)
    t = sub(r'<div class="byline-name">.*?</div>',
            '<div class="byline-name">Redaksi Berita HIFDI</div>', t, re.S)
    t = sub(r'<div class="article-body">.*?</div>\s*(?=<div class="article-footer">)',
            body + "\n", t, re.S)
    return t


def insert_card(index_html, article, number, image, date_str):
    esc = lambda s: html.escape(s, quote=True)
    img_card = f"https://images.unsplash.com/{image['id']}?auto=format&fit=crop&w=800&q=80"
    slug = article["category"].lower().replace(" ", "-")
    excerpt = article["subtitle"]

    card = (
        f'\n    <!-- ARTIKEL {number:03d} — {esc(article["category"])} — {date_str} — INTERNAL (bot) -->\n'
        f'    <a class="article-card" href="./article-{number:03d}/" data-category="{slug}">\n'
        f'      <img class="card-image" src="{img_card}" alt="{esc(image["alt"])}">\n'
        f'      <div class="card-body">\n'
        f'        <div class="card-category-row"><span class="card-category">{esc(article["category"])}</span></div>\n'
        f'        <div class="card-title">{esc(article["title"])}</div>\n'
        f'        <div class="card-excerpt">{esc(excerpt)}</div>\n'
        f'        <div class="card-meta">{date_str} · Redaksi Berita HIFDI</div>\n'
        f"      </div>\n    </a>"
    )

    anchor = '<div class="articles-grid" id="articlesGrid">'
    if anchor not in index_html:
        raise SystemExit("Tidak menemukan grid articlesGrid di index.html")
    out = index_html.replace(anchor, anchor + card, 1)

    def bump(m):
        return f'{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}'
    out, n = re.subn(r'(id="articleCount">)(\d+)( artikel)', bump, out, count=1)
    if n == 0:
        raise SystemExit("Tidak menemukan articleCount di index.html")
    return out


# --------------------------------------------------------------------------
def main():
    index_html = read_index()
    old_titles = existing_titles(index_html)
    log(f"artikel tayang sekarang: {len(old_titles)}")

    candidates = collect_candidates(old_titles)
    log(f"kandidat relevan & belum pernah ditulis: {len(candidates)}")
    if not candidates:
        log("tidak ada kandidat layak hari ini — berhenti tanpa menulis apa pun.")
        return 0

    log("lima teratas:")
    for c in candidates[:5]:
        log(f"   skor {c['score']:>3}  [{c['source']}] {c['title'][:70]}")

    candidate = candidates[0]
    log(f"terpilih: [{candidate['source']}] {candidate['title']}")

    article = call_deepseek(candidate)
    number = next_article_number()
    today = datetime.now(WIB)
    date_str = f"{today.day} {BULAN_ID[today.month]} {today.year}"
    image = IMAGES[IMAGE_BY_CATEGORY.get(article["category"], DEFAULT_IMAGE)]

    # Baca template DULU, sebelum folder baru dibuat (lihat build_article_html).
    with open(template_path(), encoding="utf-8") as f:
        tpl = f.read()

    folder = os.path.join(REPO, f"article-{number:03d}")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(build_article_html(tpl, article, image, candidate, date_str))

    with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
        f.write(insert_card(index_html, article, number, image, date_str))

    link = f"https://berita.hifdi.id/article-{number:03d}/"
    caption = (f"{article['caption']}\n\n{link}\n"
               f"\n_Berita HIFDI — Himpunan Fasyankes Dokter Indonesia_")

    with open(os.path.join(REPO, "wa-caption.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(caption + "\n")

    log(f"SELESAI article-{number:03d}: {article['title']}")
    log(f"kategori={article['category']} gambar={image['id']}")

    # Dua pesan terpisah: laporan dulu, lalu caption polos supaya bisa
    # diteruskan/disalin ke WAG tanpa ikut membawa teks laporan.
    notify_telegram(
        f"BOT HARIAN — artikel {number:03d} tayang\n\n"
        f"Judul    : {article['title']}\n"
        f"Kategori : {article['category']}\n"
        f"Sumber   : {candidate['source']} (skor {candidate['score']})\n"
        f"           {candidate['link']}\n"
        f"Link     : {link}\n\n"
        f"Cloudflare butuh 1-2 menit sebelum tayang.\n"
        f"Caption WA menyusul di pesan berikut — tinggal teruskan ke WAG."
    )
    notify_telegram(caption)
    return 0


if __name__ == "__main__":
    sys.exit(main())
