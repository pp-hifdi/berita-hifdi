#!/usr/bin/env python3
"""Penerbit draft HIFDI — baca balasan ACC/TOLAK di Telegram, lalu publish.

Dijalankan GitHub Actions tiap 5 menit (workflow publish-on-acc.yml).

Alur:
1. getUpdates Telegram, cari balasan terbaru "ACC" / "TOLAK" dari chat admin
   (TELEGRAM_CHAT_ID). Pesan dari chat lain diabaikan.
2. ACC   -> merge branch `draft` ke `main` (artikel tayang), balas konfirmasi.
3. TOLAK -> hapus branch `draft` (artikel dibatalkan), balas konfirmasi.

State (update_id terakhir yang diproses) disimpan di scripts/telegram_state.json
dan di-commit supaya pesan lama tidak diproses ulang antar run.

Perilaku penting: ACC/TOLAK berlaku untuk SEMUA draft yang sedang menunggu di
branch draft (bila beberapa hari tidak di-ACC, satu ACC menerbitkan semuanya).
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT = os.environ.get("TELEGRAM_CHAT_ID")
STATE_FILE = "scripts/telegram_state.json"
BOT_URL = f"https://api.telegram.org/bot{TOKEN}" if TOKEN else None
WIB = timezone(timedelta(hours=7))


def log(msg):
    print(f"[publish-on-acc] {msg}", flush=True)


def tg(method, **params):
    req = urllib.request.Request(
        f"{BOT_URL}/{method}",
        data=json.dumps(params).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def get_updates(**params):
    """getUpdates dengan retry untuk HTTP 409 (konflik polling bot lain).

    Telegram mengizinkan hanya SATU sesi getUpdates per bot; kalau bot ini
    sedang dipolling proses lain (mis. gateway Hermes), 409 muncul. Setelah
    3 percobaan gagal, kembalikan None — jangan bikin workflow merah tiap
    5 menit; run berikutnya mencoba lagi.
    """
    for i, delay in enumerate((0, 5, 10)):
        try:
            return tg("getUpdates", **params)
        except urllib.error.HTTPError as exc:
            if exc.code == 409 and i < 2:
                log("getUpdates 409 (konflik polling bot lain) — coba lagi")
                time.sleep(delay + 5)
            else:
                raise
    return None


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            log(f"state korup ({exc}) — mulai kosong")
    return {}


def save_state(state):
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    os.replace(tmp, STATE_FILE)


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} gagal: {r.stderr.strip()[:300]}")
    return r


def draft_number():
    """Nomor artikel draft tertinggi di origin/draft (buat link konfirmasi)."""
    r = git("ls-tree", "-r", "--name-only", "origin/draft", check=False)
    if r.returncode != 0:
        return None
    nos = sorted(re.findall(r"article-(\d{3})/", r.stdout))
    return nos[-1] if nos else None


def publish_draft():
    """Merge origin/draft -> origin/main (rebase dulu supaya fast-forward)."""
    git("checkout", "--detach", "origin/draft")
    r = subprocess.run(["git", "rebase", "origin/main"], capture_output=True, text=True)
    if r.returncode != 0:
        git("rebase", "--abort", check=False)
        raise RuntimeError("rebase draft ke main konflik — publish dibatalkan")
    git("push", "origin", "HEAD:main")


def commit_offset(state):
    """Simpan offset ke git supaya persist lintas run; tidak commit bila
    tidak ada perubahan (mencegah spam commit tiap 5 menit)."""
    save_state(state)
    git("add", STATE_FILE)
    r = git("commit", "-m", "state: telegram offset", check=False)
    if r.returncode == 0:
        git("push", "origin", "HEAD:main")


def main():
    if not TOKEN or not CHAT:
        log("TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID belum diset — keluar.")
        return 0

    # Runner GitHub tidak punya identitas git default — set sebelum commit.
    git("config", "user.name", "HIFDI Bot", check=False)
    git("config", "user.email", "bot@hifdi.id", check=False)

    state = load_state()

    # Run pertama: jangan proses pesan lama — cukup catat offset terakhir.
    if "offset" not in state:
        try:
            upd = get_updates(offset=-1, timeout=1)
        except Exception as exc:
            log(f"getUpdates gagal: {exc}")
            return 1
        if upd is None:
            return 1
        res = upd.get("result", [])
        state["offset"] = res[-1]["update_id"] if res else 0
        save_state(state)
        git("add", STATE_FILE)
        r = git("commit", "-m", "state: telegram offset awal", check=False)
        if r.returncode == 0:
            git("push", "origin", "HEAD:main")
        log(f"inisialisasi: offset awal {state['offset']} (pesan lama dilewati)")
        return 0

    try:
        upd = get_updates(offset=state["offset"] + 1, timeout=1,
                          allowed_updates=["message"])
    except Exception as exc:
        log(f"getUpdates gagal: {exc}")
        return 1
    if upd is None:
        return 1
    res = upd.get("result", [])

    cmd = None
    new_offset = state["offset"]
    for u in res:
        new_offset = max(new_offset, u["update_id"])
        msg = u.get("message", {})
        if str(msg.get("chat", {}).get("id")) != str(CHAT):
            continue  # abaikan chat lain — hanya admin yang bisa ACC/TOLAK
        text = (msg.get("text") or "").strip().upper()
        if re.search(r"\bACC\b", text):
            cmd = "ACC"
        elif re.search(r"\bTOLAK\b", text):
            cmd = "TOLAK"
    state["offset"] = new_offset

    if not cmd:
        commit_offset(state)
        log("tidak ada perintah baru")
        return 0

    # Fetch semua branch supaya origin/draft & origin/main fresh.
    git("fetch", "origin")
    has_draft = git("rev-parse", "--verify", "origin/draft", check=False).returncode == 0
    if not has_draft:
        commit_offset(state)
        log("ACC/TOLAK tapi tidak ada branch draft")
        return 0

    same = git("rev-parse", "origin/main").stdout.strip() == git(
        "rev-parse", "origin/draft").stdout.strip()

    try:
        if cmd == "ACC":
            if same:
                tg("sendMessage", chat_id=CHAT,
                   text="✅ Tidak ada draft baru — main sudah sama dengan draft.")
                log("draft == main, tidak ada yang diterbitkan")
            else:
                publish_draft()
                no = draft_number()
                link = f"https://berita.hifdi.id/article-{no}/" if no else "halaman beranda"
                now = datetime.now(WIB).strftime("%d-%m-%Y %H:%M")
                tg("sendMessage", chat_id=CHAT,
                   text=f"✅ Artikel {no or ''} sudah tayang: {link}\n\n"
                        f"({now} WIB, otomatis dari bot)")
                log(f"ACC -> diterbitkan article-{no}")
        elif cmd == "TOLAK":
            git("push", "origin", "--delete", "draft")
            tg("sendMessage", chat_id=CHAT,
               text="🗑 Draft dibatalkan (TOLAK) — tidak tayang.")
            log("TOLAK -> draft dihapus")
    except Exception as exc:
        log(f"gagal: {exc}")
        try:
            tg("sendMessage", chat_id=CHAT,
               text=f"⚠️ Gagal memproses: {str(exc)[:200]}")
        except Exception:
            pass
        return 1

    # Simpan offset & commit (setelah ACC, HEAD sudah == main terbaru).
    commit_offset(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
