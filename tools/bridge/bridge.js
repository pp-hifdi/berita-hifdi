// =====================================================================
//  BERITA BRIDGE  — Telegram -> Claude Code (headless) -> WhatsApp
//  Satu proses, tiga bot, tiga folder. Node murni. + WA watchdog.
//  Jalan:  node bridge.js     Hentikan:  Ctrl+C
// =====================================================================

// --------- KONFIGURASI (dipisah ke config.local.js, gitignored) -------
const { BOTS, ALLOWED_CHAT_IDS, JOB_TIMEOUT_MIN, OPENWA } = require("./config.local.js");
// ---------------------------------------------------------------------

const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

async function tg(token, method, body) {
  const r = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  });
  return r.json();
}
async function send(token, chatId, text) {
  const chunks = text.match(/[\s\S]{1,3800}/g) || ["(kosong)"];
  for (const c of chunks) await tg(token, "sendMessage", { chat_id: chatId, text: c });
}

function buildPrompt(userText) {
  const draft = /^\s*(draft|\/draft)\b/i.test(userText);
  const topic = userText.replace(/^\s*(draft|\/draft)\s*:?\s*/i, "").trim();
  if (draft) {
    return `Baca CLAUDE.md di folder ini. Tulis DRAFT artikel baru dengan topik/instruksi dari prinsipal (via Telegram): "${topic}". JANGAN publish, JANGAN push, JANGAN kirim WhatsApp. Cukup riset + tulis draft, lalu tampilkan draftnya + usulan gambar untuk saya review. Ringkas.`;
  }
  return `Baca CLAUDE.md di folder ini dan jalankan alur penerbitan LENGKAP untuk artikel baru dengan topik/instruksi dari prinsipal (via Telegram): "${topic}".

MODE OTONOM PENUH (tidak ada operator untuk menyetujui di tengah proses):
- LANGKAH PERTAMA WAJIB: jalankan \`git pull --rebase\` SEBELUM menghitung nomor artikel. Ada bot harian di GitHub Actions yang push ke origin tanpa laptop ini tahu, jadi repo lokal bisa basi. Menghitung nomor dari keadaan basi = nomor bentrok + push ditolak. Kalau nanti push ditolak (non-fast-forward), jalankan \`git pull --rebase\` lalu ulangi push.
- Riset topik lewat web search, pastikan faktual & belum pernah ditulis (cek index/register).
- Tulis artikel sesuai gaya & struktur CLAUDE.md.
- GAMBAR — PRINSIP UTAMA (WAJIB, semua portal): gambar HARUS berkaitan langsung dengan KATA KUNCI di JUDUL artikel. Langkah: (1) ekstrak kata kunci inti dari judul; (2) pilih/cari gambar yang subjeknya cocok kata kunci itu. DILARANG memakai gambar yang subjeknya tidak berhubungan dengan judul, seberapa pun "aman tayang"-nya. Uji akhir: kalau orang baca judul lalu lihat gambar, harus terasa nyambung.
  Cara sesuai metode portal (di CLAUDE.md):
  * FMI: HANYA file lokal di berita/img/ (haram hotlink). Cari gambar yang cocok kata kunci judul: download baru dari Wikimedia/Pexels (bisa diverifikasi, atribusi lengkap) simpan sebagai berita/img/{NNN}-{slug}.jpg, ATAU pakai ulang file lokal lama yang subjeknya cocok kata kunci judul.
  * HIFDI & ummanitarian: Unsplash (jangan mengarang ID; tak bisa diverifikasi curl). Baca daftar ID lama + ALT TEXT-nya dari index.html, cocokkan ALT dengan kata kunci judul, pilih yang paling cocok. Kalau TIDAK ADA ID lama yang cocok kata kunci judul, JANGAN paksa gambar salah tema -> download foto cocok dari Wikimedia/Pexels, host LOKAL di folder images/, pakai itu. Alt gambar baru harus jujur menggambarkan foto asli.
- Publish penuh: commit + push sesuai konvensi CLAUDE.md, verifikasi tayang.
- JANGAN kirim WhatsApp sendiri. Setelah artikel tayang & terverifikasi, tulis CAPTION FINAL ke file bernama wa-caption.txt di folder repo ini (root folder), UTF-8, ISI TEKS MURNI caption saja (bukan JSON, bukan objek, tanpa tanda kutip pembungkus). Bridge yang akan membaca file itu dan mengirimnya ke grup WhatsApp yang benar. Kalau mode draft, JANGAN buat wa-caption.txt.
- Di akhir laporkan RINGKAS: nomor artikel, judul, link live, gambar yang dipakai, status kirim WA.
- Kalau ada langkah yang benar-benar gagal (bukan sekadar perlu approval), berhenti dan laporkan alasannya.`;
}

// Path lengkap ke CLI claude. Pakai path absolut supaya tidak bergantung PATH
// proses induk — pernah gagal ("'claude' is not recognized") saat bridge
// dijalankan dari shell yang PATH-nya tidak memuat folder npm global.
const CLAUDE_BIN = process.env.CLAUDE_BIN
  || path.join(process.env.APPDATA || "C:\\Users\\Admin\\AppData\\Roaming", "npm", "claude.cmd");

function runClaude(folder, prompt) {
  return new Promise((resolve) => {
    let out = "";
    const child = spawn(`"${CLAUDE_BIN}"`, ["-p", "--dangerously-skip-permissions"], { cwd: folder, shell: true });
    const timer = setTimeout(() => { child.kill(); resolve("[TIMEOUT] Melewati batas waktu. Cek repo manual."); }, JOB_TIMEOUT_MIN * 60000);
    child.stdout.on("data", (d) => (out += d.toString()));
    child.stderr.on("data", (d) => (out += d.toString()));
    child.on("close", (code) => { clearTimeout(timer); resolve(out.trim() || `[selesai, kode ${code}, tanpa output]`); });
    child.on("error", (e) => { clearTimeout(timer); resolve(`[GAGAL menjalankan claude] ${e.message}`); });
    child.stdin.write(prompt);
    child.stdin.end();
  });
}

async function sendWa(group, text) {
  const r = await fetch(`${OPENWA.url}/api/sessions/${OPENWA.session}/messages/send-text`, {
    method: "POST",
    headers: { "X-API-Key": OPENWA.key, "Content-Type": "application/json" },
    body: JSON.stringify({ chatId: group, text: String(text) }),
  });
  return r.ok;
}

// Setelah job publish: kalau Claude menulis wa-caption.txt, bridge yang kirim ke WA (dijamin string).
async function deliverCaption(bot) {
  try {
    const f = path.join(bot.folder, "wa-caption.txt");
    if (!fs.existsSync(f)) return "(tidak ada wa-caption.txt; WA tidak dikirim)";
    const text = fs.readFileSync(f, "utf8").trim();
    if (!text) return "(wa-caption.txt kosong; WA tidak dikirim)";
    const ok = await sendWa(bot.group, text);
    try { fs.unlinkSync(f); } catch (e) {}
    return ok ? "Caption WA terkirim oleh bridge." : "Caption WA GAGAL dikirim (cek status WA / Docker).";
  } catch (e) { return "Error kirim caption: " + e.message; }
}

const offsets = {}, busy = {}, jobStart = {};

async function statusText() {
  let lines = ["STATUS BRIDGE"];
  for (const b of BOTS) {
    if (busy[b.name]) {
      const mins = Math.round((Date.now() - (jobStart[b.name] || Date.now())) / 60000);
      lines.push(`- ${b.name}: SIBUK (${mins} menit)`);
    } else lines.push(`- ${b.name}: idle`);
  }
  try {
    const r = await fetch(`${OPENWA.url}/api/sessions/${OPENWA.session}`, { headers: { "X-API-Key": OPENWA.key } });
    const j = await r.json();
    lines.push(`- WhatsApp: ${j.status || "?"}`);
  } catch (e) { lines.push("- WhatsApp: gateway tidak terjangkau (Docker mati?)"); }
  return lines.join("\n");
}

async function pollBot(bot) {
  try {
    const res = await tg(bot.token, "getUpdates", { offset: offsets[bot.name] || 0, timeout: 30 });
    if (!res.ok) return;
    for (const upd of res.result) {
      offsets[bot.name] = upd.update_id + 1;
      const msg = upd.message; if (!msg || !msg.text) continue;
      const chatId = msg.chat.id, fromId = msg.from.id, text = msg.text.trim();
      if (/^\/id\b/i.test(text)) { await send(bot.token, chatId, `Telegram ID Anda: ${fromId}\nBot: ${bot.name}`); continue; }
      if (/^\/start\b/i.test(text)) { await send(bot.token, chatId, `Bot ${bot.name} aktif. Kirim topik untuk PUBLISH. Awali "draft:" untuk draft saja.`); continue; }
      if (/^\/status\b/i.test(text)) { await send(bot.token, chatId, await statusText()); continue; }
      if (ALLOWED_CHAT_IDS.length && !ALLOWED_CHAT_IDS.includes(fromId)) { await send(bot.token, chatId, "Ditolak."); continue; }
      if (busy[bot.name]) { await send(bot.token, chatId, "Masih mengerjakan tugas sebelumnya. Tunggu selesai."); continue; }
      busy[bot.name] = true; jobStart[bot.name] = Date.now();
      const mode = /^\s*(draft|\/draft)\b/i.test(text) ? "DRAFT" : "PUBLISH";
      await send(bot.token, chatId, `Diterima (${bot.name}, mode ${mode}). Sedang mengerjakan, bisa beberapa menit...`);
      runClaude(bot.folder, buildPrompt(text)).then(async (result) => {
        await send(bot.token, chatId, result);
        if (mode === "PUBLISH") { const waMsg = await deliverCaption(bot); await send(bot.token, chatId, waMsg); }
        busy[bot.name] = false;
      });
    }
  } catch (e) {}
}

// -------- WA watchdog: auto-reconnect + alert QR ----------------------
let lastQrAlert = 0;
async function waWatch() {
  try {
    const r = await fetch(`${OPENWA.url}/api/sessions/${OPENWA.session}`, { headers: { "X-API-Key": OPENWA.key } });
    const s = await r.json(); const st = s.status;
    if (st === "qr_ready") {
      if (Date.now() - lastQrAlert > 30 * 60000) {
        lastQrAlert = Date.now();
        await send(BOTS[0].token, ALLOWED_CHAT_IDS[0], "PERINGATAN: Sesi WhatsApp putus & minta scan QR ulang. Buka http://localhost:2785 (login pakai API key), scan QR di session berita-wa. Sampai discan, kirim caption WA akan gagal.");
        console.log("WA qr_ready -> alert dikirim ke Telegram");
      }
    } else if (st && st !== "ready" && st !== "initializing") {
      await fetch(`${OPENWA.url}/api/sessions/${OPENWA.session}/start`, { method: "POST", headers: { "X-API-Key": OPENWA.key } });
      console.log("WA status", st, "-> coba sambung ulang otomatis");
    }
  } catch (e) {}
}
setInterval(waWatch, 60000);

console.log("Berita Bridge jalan. Bot:", BOTS.map((b) => b.name).join(", "));
console.log("WA watchdog aktif (cek tiap 60 detik). Ctrl+C untuk berhenti.");
(async function loop() { while (true) { await Promise.all(BOTS.map(pollBot)); } })();
