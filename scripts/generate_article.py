"""
generate_article.py - Jalankan dari root repo pp-hifdi/berita-hifdi.
Env var wajib: ANTHROPIC_API_KEY
"""

import os, re, json, pathlib, datetime
import anthropic

REPO_ROOT  = pathlib.Path(__file__).parent.parent
INDEX_PATH = REPO_ROOT / "index.html"
BULAN_ID   = ["","Januari","Februari","Maret","April","Mei","Juni",
               "Juli","Agustus","September","Oktober","November","Desember"]


def next_article_number() -> int:
    existing = sorted(REPO_ROOT.glob("article-*/index.html"))
    if not existing:
        return 1
    nums = [int(re.search(r"article-(\d+)", str(p)).group(1)) for p in existing]
    return max(nums) + 1


def today_id() -> str:
    d = datetime.date.today()
    return f"{d.day} {BULAN_ID[d.month]} {d.year}"


def build_prompt(article_num: int, tanggal: str) -> str:
    return (
        "Kamu adalah editor senior Berita HIFDI.\n\n"
        "TUGAS: Gunakan web search cari 1 berita/isu terkini (7 hari terakhir) "
        "genuinely relevan fasyankes primer Indonesia: puskesmas, klinik pratama, "
        "BPJS, Kemenkes, akreditasi, Satu Sehat, RME, mutu fasyankes, kebijakan kesehatan, "
        "atau berita kesehatan Asia/Eropa/Teluk dengan koneksi nyata ke fasyankes primer.\n"
        "DILARANG: topik Amerika, kesehatan generik tanpa koneksi fasyankes.\n\n"
        "OUTPUT: JSON saja.\n"
        '{"article_html":"<FULL HTML artikel self-contained>","card_html":"<card HTML>","category_slug":"advokasi|edukasi|mutu|kabar-hifdi","category_label":"Advokasi|Edukasi|Mutu|Kabar HIFDI"}\n\n'
        "ARTIKEL: Font Playfair Display+DM Sans+DM Mono. CSS vars: --green-900:#122B1A, --green-800:#1B4028, --gold-400:#E8AB28. "
        "Header: logo ../images/logo-hifdi.png + back link. Body: category badge,h1,subtitle,meta,Unsplash img,byline Redaksi,article-body,sources-box,back link. Footer: hifdi.id. "
        "Narasi: Pembukaan>Data>Fasyankes>Dokter>blockquote>Posisi HIFDI>Penutup. Min 600 kata.\n"
        f"Tanggal: {tanggal}. Path: article-{article_num:03d}/\n\n"
        f"CARD pattern: <a class=\"article-card\" href=\"./article-{article_num:03d}/\" data-category=\"[slug]\">..."
    )


def generate_article(article_num: int, tanggal: str) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    print(f"[generate] article-{article_num:03d}...")
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": build_prompt(article_num, tanggal)}],
    )
    text_parts = [b.text for b in response.content if hasattr(b, "text")]
    raw = "\n".join(text_parts).strip()
    raw = re.sub(r"^```json\s*", "", raw, flags=re.MULTILINE).strip()
    raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE).strip()
    return json.loads(raw)


def write_article(article_num: int, html: str):
    folder = REPO_ROOT / f"article-{article_num:03d}"
    folder.mkdir(exist_ok=True)
    (folder / "index.html").write_text(html, encoding="utf-8")
    print(f"[write] article-{article_num:03d}/index.html")


def update_index(card_html: str, article_num: int):
    content = INDEX_PATH.read_text(encoding="utf-8")
    marker = '<div class="articles-grid" id="articlesGrid">'
    if marker not in content:
        raise ValueError("Marker articlesGrid tidak ditemukan")
    new_content = content.replace(marker, marker + "\n" + card_html, 1)
    def inc(m): return f"{int(m.group(1))+1} artikel"
    new_content = re.sub(r"(\d+) artikel", inc, new_content, count=1)
    INDEX_PATH.write_text(new_content, encoding="utf-8")
    print(f"[update] index.html")


def main():
    tanggal = today_id()
    art_num = next_article_number()
    print(f"[start] article-{art_num:03d} — {tanggal}")
    result  = generate_article(art_num, tanggal)
    write_article(art_num, result["article_html"])
    update_index(result["card_html"], art_num)
    print(f"[done] article-{art_num:03d}")


if __name__ == "__main__":
    main()
