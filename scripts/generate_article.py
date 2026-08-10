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
import random
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

import feedparser
from openai import OpenAI

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import photo_pool  # noqa: E402
from config import (  # noqa: E402
    BLOCKLIST, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, DEFAULT_IMAGE, FEEDS, IMAGES,
    IMAGE_BY_CATEGORY, IMAGE_POOLS, KEYWORDS_MEDIUM, KEYWORDS_STRONG,
    KEYWORDS_WEAK, MAX_SOURCE_CHARS, MIN_SCORE, MIN_TITLE_WORDS, SYSTEM_PROMPT,
)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(REPO, "index.html")
USED_SOURCES_FILE = os.path.join(REPO, "scripts", "used_sources.json")
STOCK_DIR = os.path.join(REPO, "stok")
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


def draft_body_text(body_html, subtitle="", limit=3800):
    """Isi artikel sebagai teks polos untuk review draft di Telegram.

    Artikel ±500 kata muat di batas 4096 karakter pesan Telegram; HTML
    dibuang supaya yang direview Prinsipal adalah teks, bukan markup.
    """
    text = re.sub(r"<[^>]+>", " ", body_html or "")
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        text = subtitle
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + " …"
    return text


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
# 1b. Penjaga sumber duplikat (used_sources.json)
# --------------------------------------------------------------------------
def load_used_sources():
    """URL sumber yang sudah pernah dipakai -> folder artikel.

    Pelajaran 3 Agustus 2026: article-063 & 064 kembar karena dedup
    membandingkan JUDUL feed dengan judul terbitan — dua hal yang berbeda.
    Penjaga yang benar membandingkan URL sumber: satu URL = satu artikel,
    selamanya. File ini ditulis mesin, jangan disunting tangan.
    """
    if not os.path.isfile(USED_SOURCES_FILE):
        return {}
    try:
        with open(USED_SOURCES_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError) as exc:
        log(f"used_sources.json tidak terbaca ({exc}) — dianggap kosong")
        return {}


def save_used_sources(used):
    with open(USED_SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, indent=2, ensure_ascii=False)
        f.write("\n")


def normalise_url(url):
    """URL pembanding: buang fragment + trailing slash, turunkan huruf."""
    return (url or "").strip().split("#")[0].rstrip("/").lower()


def mark_source_used(used, url, article_dir):
    """Catat URL ke penjaga. Beri tahu kalau ternyata sudah pernah dipakai."""
    key = normalise_url(url)
    if key and key not in used:
        used[key] = article_dir
    elif key:
        log(f"PERHATIAN: URL sudah pernah dipakai di {used[key]} — {url}")


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


def collect_candidates(old_titles, used_sources):
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
            # PENJAGA DUPLEX: satu URL sumber = satu artikel, selamanya.
            # Pelajaran 3 Agu 2026: article-063 & 064 kembar karena dedup
            # judul gagal menangkap URL yang sama. Cek URL, bukan judul.
            if normalise_url(link) in used_sources:
                log(f"   dibuang (URL sudah dipakai): {link[:80]}")
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
# SYSTEM_PROMPT (suara editorial) dipindahkan ke config.py pada 3 Agu 2026
# atas usulan Sekjen — lihat config.py. Skrip ini hanya memakainya.


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
        # 4000 sempat bikin model kehabisan ruang sebelum menulis caption.
        # Artikel ±500 kata Bahasa Indonesia + HTML + caption butuh kelonggaran.
        max_tokens=8000,
    )
    raw = resp.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.M).strip()
    data = json.loads(raw)

    # HANYA judul & badan artikel yang esensial. Sisanya bisa diturunkan sendiri.
    #
    # Pelajaran 3 Agustus 2026: run pertama gagal total hanya karena model tidak
    # mengisi 'caption'. Membuang artikel yang sudah jadi (dan token yang sudah
    # terpakai) gara-gara caption WA kosong itu keliru — caption bisa disusun
    # dari judul. Jangan pernah lagi menjadikan kolom turunan sebagai syarat.
    for key in ("title", "body_html"):
        if not data.get(key):
            raise SystemExit(f"Balasan model tidak lengkap: '{key}' kosong — ini esensial.")

    if data.get("category") not in IMAGE_BY_CATEGORY:
        data["category"] = "Advokasi"

    if not data.get("subtitle"):
        # Ambil dari PARAGRAF PERTAMA saja, bukan seluruh badan artikel —
        # kalau semua tag disapu, judul <h2> ("Posisi HIFDI") ikut terseret
        # dan subjudulnya jadi kalimat sampah.
        m = re.search(r"<p>(.*?)</p>", data["body_html"], re.S)
        plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip() if m else ""
        if plain:
            potongan = plain[:200]
            data["subtitle"] = (potongan.rsplit(".", 1)[0] + "."
                                if "." in potongan else potongan)
        else:
            data["subtitle"] = data["title"]
        log("subtitle kosong -> diturunkan dari paragraf pertama")

    if not data.get("meta_description"):
        data["meta_description"] = data["subtitle"][:200]

    if not data.get("caption"):
        data["caption"] = f"*{data['title']}*\n\n{data['subtitle']}"
        log("caption kosong -> disusun dari judul + subjudul")

    return data


def choose_image(category, number=None):
    """Foto lokal dari kolam (sistem gilir) dulu; fallback daftar putih
    (Unsplash + penyedia lain), dipilih acak antar kunci kategori."""
    pool = photo_pool.pick(category, article_no=number, pools=IMAGE_POOLS)
    if pool:
        return pool
    keys = IMAGE_BY_CATEGORY.get(category, [DEFAULT_IMAGE])
    if isinstance(keys, str):
        keys = [keys]
    return IMAGES[random.choice(keys)]


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
    if image.get('local'):
        # foto kolam: og pakai varian 1200x630, tampilan pakai versi display
        og_img = photo_pool.url(image, 'og')
        feat_img = photo_pool.url(image, 'display')
    else:
        og_img = image.get('og') or image.get('url')
        feat_img = image.get('url')
        if not feat_img:  # entri Unsplash lama: bangun dari id
            unsplash = (f"https://images.unsplash.com/{image['id']}"
                        "?auto=format&fit=crop&w=1200&h=630&q=80")
            og_img = feat_img = unsplash

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
            f'<meta property="og:image" content="{og_img}">', t)
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
            f'<img class="featured-image" src="{feat_img}" alt="{esc(image["alt"])}">', t)
    t = sub(r'<div class="byline-name">.*?</div>',
            '<div class="byline-name">Redaksi Berita HIFDI</div>', t, re.S)
    t = sub(r'<div class="article-body">.*?</div>\s*(?=<div class="article-footer">)',
            body + "\n", t, re.S)
    return t


def insert_card(index_html, article, number, image, date_str):
    esc = lambda s: html.escape(s, quote=True)
    if image.get('local'):
        img_card = photo_pool.url(image, 'display')
    else:
        img_card = image.get('url') or (
            f"https://images.unsplash.com/{image['id']}?auto=format&fit=crop&w=800&q=80")
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
# 4b. Amunisi dari folder stok/ (draf jadi tulisan Sekjen)
# --------------------------------------------------------------------------
def extract_stock_meta(html_text):
    """Baca metadata dari HTML draf stok (struktur sama dengan artikel jadi).

    Kalau satu kolom tidak ada, isi fallback yang aman — bot TIDAK menolak
    seluruh draf hanya karena satu tag kosmetik kurang.
    """
    def grab(pattern, flags=0):
        m = re.search(pattern, html_text, flags)
        return m.group(1).strip() if m else ""

    title = grab(r'<h1 class="article-title">(.*?)</h1>', re.S) or \
            grab(r'<meta property="og:title" content="([^"]*)"')
    title = re.sub(r"\s+", " ", title).replace(" — HIFDI", "").strip()

    category = grab(r'<span class="article-category">(.*?)</span>', re.S)
    if category not in IMAGE_BY_CATEGORY:
        category = "Advokasi"

    subtitle = grab(r'<div class="article-subtitle">(.*?)</div>', re.S)
    if not subtitle:
        m = re.search(r"<p>(.*?)</p>", html_text, re.S)
        plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip() if m else ""
        subtitle = plain[:200] if plain else title
        subtitle = re.sub(r"\s+", " ", subtitle).strip()

    meta_desc = grab(r'<meta name="description" content="([^"]*)"')
    if not meta_desc:
        meta_desc = subtitle[:200]

    og_image = grab(r'<meta property="og:image" content="([^"]*)"')
    m = re.search(r"photo-(\d+[-\w]*)", og_image)
    image_id = m.group(1) if m else None

    sources = re.findall(r'href="(https?://[^"]+)"', html_text)
    sources = [s for s in sources if "unsplash" not in s and "hifdi.id" not in s
               and "fonts" not in s and "w3.org" not in s]

    return {
        "title": title,
        "category": category,
        "subtitle": subtitle,
        "meta_description": meta_desc,
        "image_id": image_id,
        "sources": sources,
    }


def publish_from_stock(used):
    """Kalau ada draf jadi di stok/, terbitkan yang paling awal.

    Prioritas (keputusan Prinsipal 3 Agu 2026): ada tulisan Sekjen -> push
    itu, TANPA mencari RSS. Kosong -> main() lanjut ke RSS seperti biasa.

    Draf yang memakai URL sumber yang SUDAH PERNAH TERBIT ditolak (aturan
    mutu §3: satu URL = satu artikel, selamanya) — penjaga duplikat berlaku
    untuk stok juga, bukan cuma RSS.
    """
    if not os.path.isdir(STOCK_DIR):
        return False
    drafts = sorted(
        d for d in os.listdir(STOCK_DIR)
        if os.path.isfile(os.path.join(STOCK_DIR, d, "index.html"))
    )
    if not drafts:
        log("stok/ kosong — lanjut RSS seperti biasa")
        return False

    for draft in drafts:
        src = os.path.join(STOCK_DIR, draft, "index.html")
        with open(src, encoding="utf-8") as f:
            html_text = f.read()

        meta = extract_stock_meta(html_text)
        if not meta["title"] or len(meta["title"].split()) < 2:
            log(f"stok: draf {draft} tidak punya judul layak — dilewati")
            continue

        # PENJAGA DUPLEX untuk stok: kalau ada URL sumber yang sudah pernah
        # terbit, tolak draf ini (aturan §3). Jangan terbitkan pelanggaran.
        dup = [u for u in meta["sources"] if normalise_url(u) in used]
        if dup:
            log(f"stok: draf {draft} DITOLAK — URL sudah pernah terbit: {dup[0][:80]}")
            log(f"       {len(dup)} URL kembar. Pindah ke stok/_ditolak/ ...")
            os.makedirs(os.path.join(STOCK_DIR, "_ditolak"), exist_ok=True)
            os.rename(
                os.path.join(STOCK_DIR, draft),
                os.path.join(STOCK_DIR, "_ditolak", draft),
            )
            continue

        return _publish_draft(draft, meta, used)

    log("stok: tidak ada draf layak — lanjut RSS seperti biasa")
    return False


def _publish_draft(draft, meta, used):
    """Terbitkan satu draf stok yang sudah lolos pemeriksaan."""
    number = next_article_number()
    today = datetime.now(WIB)
    date_str = f"{today.day} {BULAN_ID[today.month]} {today.year}"
    folder = os.path.join(REPO, f"article-{number:03d}")

    # Pindahkan draf -> artikel jadi (rename folder). Ini "terbit".
    os.rename(os.path.join(STOCK_DIR, draft), folder)
    log(f"stok: {draft} -> article-{number:03d}")

    # Gambar kartu: ID unsplash dari draf kalau ada; kalau tidak, kolam foto lokal
    # (sistem gilir); terakhir default daftar putih.
    if meta["image_id"]:
        image = {"id": meta["image_id"], "alt": meta["subtitle"][:100]}
    else:
        image = choose_image(meta["category"], number)

    index_html = read_index()
    with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
        f.write(insert_card(index_html, meta, number, image, date_str))

    # Catat sumber draf ke penjaga duplikat — sekali dipakai, tak boleh lagi.
    for url in meta["sources"]:
        mark_source_used(used, url, f"article-{number:03d}")
    save_used_sources(used)

    link = f"https://berita.hifdi.id/article-{number:03d}/"
    caption = (f"*{meta['title']}*\n\n{meta['subtitle']}\n\n{link}\n"
               f"\n_Berita HIFDI — Himpunan Fasyankes Dokter Indonesia_")
    with open(os.path.join(REPO, "wa-caption.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(caption + "\n")

    log(f"SELESAI article-{number:03d} (dari stok Sekjen): {meta['title']}")
    notify_telegram(
        f"📝 DRAF {number:03d} SIAP REVIEW (dari stok Sekjen)\n\n"
        f"Judul    : {meta['title']}\n"
        f"Kategori : {meta['category']}\n"
        f"\nBalas ACC untuk tayang, TOLAK untuk buang."
    )
    notify_telegram(draft_body_text(meta.get("body_html", ""), meta.get("subtitle", "")))
    return True


# --------------------------------------------------------------------------
def main():
    used = load_used_sources()
    log(f"URL sumber terpakai tercatat: {len(used)}")

    # PRIORITAS AMUNISI (keputusan Prinsipal 3 Agu 2026): kalau ada draf
    # jadi dari Sekjen di stok/, terbitkan itu DULU, tanpa sentuh RSS.
    # Kosong -> lanjut RSS seperti biasa.
    if publish_from_stock(used):
        log("selesai dari stok — RSS tidak disentuh hari ini.")
        return 0

    index_html = read_index()
    old_titles = existing_titles(index_html)
    log(f"artikel tayang sekarang: {len(old_titles)}")

    candidates = collect_candidates(old_titles, used)
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
    image = choose_image(article["category"], number)

    # Baca template DULU, sebelum folder baru dibuat (lihat build_article_html).
    with open(template_path(), encoding="utf-8") as f:
        tpl = f.read()

    folder = os.path.join(REPO, f"article-{number:03d}")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(build_article_html(tpl, article, image, candidate, date_str))

    with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
        f.write(insert_card(index_html, article, number, image, date_str))

    # PENJAGA DUPLEX: catat URL sumber ke used_sources.json — sekali dipakai,
    # tak boleh terbit lagi. Ini yang mencegah article-063/064 terulang.
    mark_source_used(used, candidate["link"], f"article-{number:03d}")
    save_used_sources(used)

    link = f"https://berita.hifdi.id/article-{number:03d}/"
    caption = (f"{article['caption']}\n\n{link}\n"
               f"\n_Berita HIFDI — Himpunan Fasyankes Dokter Indonesia_")

    with open(os.path.join(REPO, "wa-caption.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(caption + "\n")

    log(f"SELESAI article-{number:03d}: {article['title']}")
    log(f"kategori={article['category']} gambar={image['id']}")

    # Dua pesan terpisah: laporan draft dulu, lalu isi artikel untuk review.
    # Caption WAG tetap ditulis ke wa-caption.txt (dipakai saat artikel tayang
    # setelah ACC — cron WAG Hermes yang meneruskannya).
    notify_telegram(
        f"📝 DRAF {number:03d} SIAP REVIEW\n\n"
        f"Judul    : {article['title']}\n"
        f"Kategori : {article['category']}\n"
        f"Sumber   : {candidate['source']} (skor {candidate['score']})\n"
        f"           {candidate['link']}\n"
        f"\nBalas ACC untuk tayang, TOLAK untuk buang."
    )
    notify_telegram(draft_body_text(article.get("body_html", ""), article.get("subtitle", "")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
