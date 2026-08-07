# SOP TAKE DOWN Artikel — Berita HIFDI

**Status: disetujui Prinsipal, 7 Agu 2026.** Keputusan = level **Admin HIFDI**
(taktis), **tidak perlu ACC Sekjen** — sejajar dengan publish artikel yang juga
tidak butuh ACC. Yang wajib adalah **info**, bukan izin.

## Kapan take down
- Kesalahan fakta yang terverifikasi (angka, nama, tanggal, klaim keliru).
- Permintaan Prinsipal.
- Isu privasi/hukum/sensitivitas (mis. identitas pasien terekspos).

## Kewenangan
- **Admin HIFDI (Hermes):** eksekusi langsung — atas permintaan Prinsipal ATAU
  inisiatif sendiri bila menemukan kesalahan yang bisa diverifikasi.
- **Sekjen (editorial):** tidak perlu ACC; cukup tahu lewat STATUS-SEKJEN.md.
- Bot harian: tidak punya wewenang take down.

## Tiga tingkat penanganan
| Tingkat | Kondisi | Tindakan | Link lama |
|---|---|---|---|
| 1. **Errata/koreksi** | Salah kecil, substansi tetap valid | Perbaiki isi + catatan koreksi di artikel | Tetap hidup |
| 2. **Tarik (unpublish)** | Tidak layak tayang, tapi tidak perlu dihancurkan | Kartu dihapus + folder → `_ditarik/` | 404 (reversibel) |
| 3. **Hapus (total)** | Kasus serius (hukum/privasi/fakta besar) | Kartu dihapus + `git rm` folder | 404 |

## Eksekusi
```bash
# Di clone kerja (Staf Mesin), setelah git pull --rebase:
python3 scripts/takedown.py <NN> --tarik --dry-run   # lihat rencana dulu
python3 scripts/takedown.py <NN> --tarik             # atau --hapus
git commit -m "takedown article-0NN (tarik/hapus)"
git push
```

## Wajib setelah eksekusi (bukan opsional)
1. **STATUS-SEKJEN.md** — catat nomor artikel + alasan + tingkat (Sekjen baca pagi).
2. **Pesan koreksi/pencabutan** ke WAG HIFDI Bangkit + Telegram bila caption
   artikel sudah terlanjur tersebar — jangan hapus diam-diam.
3. **Verifikasi live:** kartu hilang dari portal, articleCount turun, halaman
   artikel 404/terpindah (HTTP cek).
4. **used_sources.json:** URL sumber tetap tercatat (riwayat duplikat tetap
   terjaga) — jangan dihapus.

## Catatan teknis
- `_ditarik/` di repo: git mv → history aman, reversibel (git mv balik + sisip
  kartu lagi).
- Foto di registry rotasi: TIDAK di-rollback (pemakaian tetap tercatat, wajar).
- Beda dengan `stok/_ditolak/`: itu draf belum terbit; `_ditarik/` ini artikel
  yang sudah pernah live.
