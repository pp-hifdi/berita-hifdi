# tools/bridge — SALINAN CADANGAN, bukan yang dijalankan

Berkas di folder ini adalah **cadangan** dari jembatan Telegram yang berjalan di
laptop pemilik repo. Yang benar-benar dieksekusi ada di:

```
C:\Users\Admin\berita-bridge\
```

## Kenapa dicadangkan di sini

Per 3 Agustus 2026, `berita-bridge` **bukan repo git dan tidak punya salinan di
mana pun**. Satu disk rusak = jembatan Telegram hilang permanen dan harus
dibangun ulang dari nol. Padahal akun Claude bisa dibuat ulang dalam lima menit,
sementara `bridge.js` tidak.

Ditaruh di repo HIFDI karena ini yang tercepat dan tanpa infrastruktur baru.
Kalau Hermes menghendaki repo privat tersendiri (bridge melayani tiga portal,
bukan HIFDI saja), silakan pindahkan — cadangan ini boleh dihapus setelahnya.

## Yang TIDAK ada di sini, dan tidak boleh ditambahkan

`config.local.js` — berisi token 3 bot Telegram, kunci & session OpenWA, dan
allowlist. **Jangan pernah di-commit.** Simpan sendiri di password manager.
`config.example.js` di folder ini adalah kerangkanya, tanpa nilai asli.

Kalau memulihkan di mesin baru: salin `config.example.js` jadi `config.local.js`,
lalu isi nilainya dari password manager.

## Isi

| Berkas | Guna |
|---|---|
| `bridge.js` | Kode jembatan. Bersih dari rahasia — sudah diverifikasi. |
| `config.example.js` | Kerangka konfigurasi, tanpa nilai asli |
| `start-bridge.cmd` | Launcher auto-nyala + auto-bangkit kalau mati |

## Memulihkan di mesin baru

1. `mkdir C:\Users\Admin\berita-bridge` lalu salin ketiga berkas ini ke sana
2. Pasang Node.js, lalu salin `config.example.js` → `config.local.js` dan isi
   nilainya dari password manager
3. Pasang Claude Code CLI (`npm i -g @anthropic-ai/claude-code`) lalu login
4. Buat shortcut `start-bridge.cmd` di folder `shell:startup` supaya otomatis
   nyala tiap login
5. Uji: kirim `/status` ke bot Telegram

Langkah lengkap pemulihan Sekjen ada di `SEKJEN.md` bagian **Cold Start**.

## Menjaga cadangan tetap mutakhir

Cadangan yang basi lebih berbahaya daripada tidak ada cadangan — memberi rasa
aman palsu. Setiap `bridge.js` yang dijalankan berubah, salin ulang ke sini:

```powershell
Copy-Item C:\Users\Admin\berita-bridge\bridge.js `
          C:\OneDrive\Documents\GitHub\berita-hifdi\tools\bridge\bridge.js
```

Terakhir disalin: **3 Agustus 2026** (bridge versi config-split + watchdog WA).
