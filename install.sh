#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Harap jalankan skrip ini sebagai root atau dengan sudo."
    exit 1
fi

if [ -f ~/testwayweb3-bots/.env ]; then
    export $(grep -v '^#' ~/testwayweb3-bots/.env | xargs)
fi

if [ -f ~/.env.local ]; then
    source ~/.env.local
fi

echo "Memperbarui sistem dan menginstal dependensi..."
apt-get update && apt-get upgrade -y
apt-get install -y python3 python3-pip python3-venv git ufw

echo "Menginstal Node.js v18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

echo "Mengatur repositori testwayweb3-bots..."
cd ~
if [ -d "testwayweb3-bots" ]; then
    echo "Direktori testwayweb3-bots sudah ada. Menggunakan direktori yang ada..."
    cd testwayweb3-bots
else
    if [ -z "$GITHUB_PAT" ]; then
        echo "Masukkan GitHub Personal Access Token (PAT):"
        read -s GITHUB_PAT
    fi
    git clone https://${GITHUB_PAT}@github.com/TestwayWeb3/testwayweb3-bots.git
    if [ $? -ne 0 ]; then
        echo "Gagal mengkloning repositori. Periksa GITHUB_PAT atau koneksi jaringan."
        exit 1
    fi
    cd testwayweb3-bots
fi

echo "Membuat virtual environment baru..."
rm -rf venv
python3 -m venv venv
source venv/bin/activate

echo "Memverifikasi interpreter Python..."
PYTHON_PATH=$(which python3)
if [ "$PYTHON_PATH" != "/root/testwayweb3-bots/venv/bin/python3" ]; then
    echo "Interpreter Python tidak sesuai: $PYTHON_PATH. Harusnya /root/testwayweb3-bots/venv/bin/python3."
    exit 1
fi

if [ ! -f requirements.txt ]; then
    echo "File requirements.txt tidak ditemukan. Membuat file default..."
    cat <<EOL > requirements.txt
python-telegram-bot
requests
notion-client
python-dotenv
EOL
fi

echo "Menginstal dependensi Python..."
pip install --upgrade pip
pip cache purge
pip install -r requirements.txt --verbose
if [ $? -ne 0 ]; then
    echo "Gagal menginstal dependensi dari requirements.txt. Mencoba instalasi manual..."
    pip install python-telegram-bot requests notion-client python-dotenv --force-reinstall --verbose
    if [ $? -ne 0 ]; then
        echo "Gagal menginstal dependensi secara manual."
        exit 1
    fi
fi

echo "Memverifikasi instalasi dependensi..."
python3 -c "from telegram import Update; from telegram.ext import Application; import requests; import notion_client; import dotenv; print('Semua dependensi terinstal dengan benar')" || {
    echo "Verifikasi gagal. Salah satu dependensi tidak terinstal."
    exit 1
}

if [ -z "$NOTION_API_KEY" ] || [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$NOTION_DATABASE_ID" ]; then
    echo "Masukkan NOTION_API_KEY:"
    read NOTION_API_KEY
    echo "Masukkan TELEGRAM_BOT_TOKEN:"
    read TELEGRAM_BOT_TOKEN
    echo "Masukkan NOTION_DATABASE_ID:"
    read NOTION_DATABASE_ID

    echo "Menyimpan kredensial ke file .env..."
    echo "NOTION_API_KEY=$NOTION_API_KEY" > .env
    echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" >> .env
    echo "NOTION_DATABASE_ID=$NOTION_DATABASE_ID" >> .env
else
    echo "Kredensial sudah ada di .env, melewati input manual."
fi

# Verifikasi kredensial dari .env
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('TELEGRAM_BOT_TOKEN:', os.environ.get('TELEGRAM_BOT_TOKEN')); print('NOTION_API_KEY:', os.environ.get('NOTION_API_KEY')); print('NOTION_DATABASE_ID:', os.environ.get('NOTION_DATABASE_ID'))"

echo "Mengatur firewall (UFW)..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo "Menginstal PM2 untuk menjalankan bot 24/7..."
npm install pm2@latest -g

echo "Menjalankan bot dengan PM2..."
pm2 start ~/testwayweb3-bots/telegram_bot.py --name "web3-bot" --interpreter ~/testwayweb3-bots/venv/bin/python3
pm2 save
pm2 startup

echo "Bot telah dijalankan! Status:"
pm2 list

echo "Selesai! Bot sudah berjalan di VPS baru."
