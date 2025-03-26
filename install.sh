#!/bin/bash

# Pastikan skrip dijalankan sebagai root atau dengan sudo
if [ "$EUID" -ne 0 ]; then
    echo "Harap jalankan skrip ini sebagai root atau dengan sudo."
    exit 1
fi

# Baca file .env jika sudah ada
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Baca PAT dari variabel lingkungan atau file lokal
if [ -f ~/.env.local ]; then
    source ~/.env.local
fi

# Perbarui sistem dan instal dependensi dasar
echo "Memperbarui sistem dan menginstal dependensi..."
apt-get update && apt-get upgrade -y
apt-get install -y python3 python3-pip python3-venv git ufw

# Instal Node.js v18
echo "Menginstal Node.js v18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Klone repositori dari GitHub atau gunakan yang sudah ada
echo "Mengatur repositori testwayweb3-bots..."
if [ -d "testwayweb3-bots" ]; then
    echo "Direktori testwayweb3-bots sudah ada. Menggunakan direktori yang ada..."
    cd testwayweb3-bots
else
    if [ -z "$GITHUB_PAT" ]; then
        echo "Masukkan GitHub Personal Access Token (PAT):"
        read -s GITHUB_PAT  # -s menyembunyikan input di terminal
    fi
    git clone https://${GITHUB_PAT}@github.com/TestwayWeb3/testwayweb3-bots.git
    if [ $? -ne 0 ]; then
        echo "Gagal mengkloning repositori. Periksa GITHUB_PAT atau koneksi jaringan."
        exit 1
    fi
    cd testwayweb3-bots
fi

# Buat dan aktifkan virtual environment
echo "Membuat virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment sudah ada. Menggunakan yang ada..."
else
    python3 -m venv venv
fi
source venv/bin/activate

# Pastikan file requirements.txt ada, jika tidak buat dengan dependensi default
if [ ! -f requirements.txt ]; then
    echo "File requirements.txt tidak ditemukan. Membuat file default..."
    cat <<EOL > requirements.txt
python-telegram-bot
requests
notion-client
EOL
fi

# Instal dependensi Python
echo "Menginstal dependensi Python..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Gagal menginstal dependensi Python. Periksa requirements.txt atau koneksi internet."
    exit 1
fi

# Minta pengguna untuk memasukkan API key dan token jika belum ada di .env
if [ -z "$NOTION_API_KEY" ] || [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$NOTION_DATABASE_ID" ]; then
    echo "Masukkan NOTION_API_KEY:"
    read NOTION_API_KEY
    echo "Masukkan TELEGRAM_BOT_TOKEN:"
    read TELEGRAM_BOT_TOKEN
    echo "Masukkan NOTION_DATABASE_ID:"
    read NOTION_DATABASE_ID

    # Simpan ke file .env
    echo "Menyimpan kredensial ke file .env..."
    echo "NOTION_API_KEY=$NOTION_API_KEY" > .env
    echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" >> .env
    echo "NOTION_DATABASE_ID=$NOTION_DATABASE_ID" >> .env
else
    echo "Kredensial sudah ada di .env, melewati input manual."
fi

# Atur firewall untuk keamanan
echo "Mengatur firewall (UFW)..."
ufw allow 22/tcp  # SSH
ufw allow 80/tcp  # HTTP (opsional, jika bot menggunakan webhook)
ufw allow 443/tcp # HTTPS untuk koneksi API Notion dan Telegram
ufw --force enable

# Instal PM2 untuk menjalankan bot secara persisten
echo "Menginstal PM2 untuk menjalankan bot 24/7..."
npm install pm2@latest -g

# Jalankan bot menggunakan PM2 dengan interpreter dari virtual environment
echo "Menjalankan bot dengan PM2..."
pm2 start telegram_bot.py --name "web3-bot" --interpreter ./venv/bin/python3
pm2 save
pm2 startup

# Tampilkan status
echo "Bot telah dijalankan! Status:"
pm2 list

echo "Selesai! Bot sudah berjalan di VPS baru."
