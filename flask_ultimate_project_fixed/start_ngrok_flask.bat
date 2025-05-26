@echo off
:: ดาวน์โหลด ngrok.exe (ถ้ายังไม่มี)
IF NOT EXIST ngrok.exe (
    echo 🔄 กำลังดาวน์โหลด ngrok...
    powershell -Command "Invoke-WebRequest -Uri https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-windows-amd64.zip -OutFile ngrok.zip"
    powershell -Command "Expand-Archive -Path ngrok.zip -DestinationPath ."
    del ngrok.zip
)

:: เพิ่ม Authtoken ของคุณ
echo 🔐 กำลังเชื่อมบัญชี ngrok...
ngrok config add-authtoken 2xPLIapTx7AFLmi3YWbBP7vTvob_QY9C2kC25iXghzU3qFqf

:: รัน Flask App ด้วย ngrok (port 5000)
start /min python app.py
timeout /t 2 >nul
start ngrok http 5000
