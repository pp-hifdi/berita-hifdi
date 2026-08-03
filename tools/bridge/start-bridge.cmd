@echo off
REM ===================================================================
REM  Berita Bridge - launcher otomatis
REM
REM  Dipanggil oleh shortcut di folder Startup Windows, jadi bridge
REM  nyala sendiri tiap laptop dinyalakan. Tidak perlu buka PowerShell.
REM
REM  Kalau bridge mati (crash / koneksi putus), loop di bawah
REM  menghidupkannya lagi setelah 10 detik. Jadi Telegram tetap
REM  responsif tanpa Anda pantau.
REM
REM  MEMATIKAN OTOMATIS-NYALA:
REM    tekan Win+R, ketik  shell:startup  , Enter,
REM    lalu hapus "Berita Bridge.lnk" dari folder yang terbuka.
REM
REM  MELIHAT LOG:  C:\Users\Admin\berita-bridge\bridge.log
REM ===================================================================

cd /d "%~dp0"
set NODE="C:\Program Files\nodejs\node.exe"
set LOG=%~dp0bridge.log

:loop
echo. >> "%LOG%"
echo ===== bridge dijalankan %DATE% %TIME% ===== >> "%LOG%"
%NODE% bridge.js >> "%LOG%" 2>&1
echo ----- bridge berhenti %DATE% %TIME%, coba lagi 10 detik ----- >> "%LOG%"
timeout /t 10 /nobreak > nul
goto loop
