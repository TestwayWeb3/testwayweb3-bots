#!/bin/bash

# Perbarui sistem dan instal dependensi dasar
echo "Memperbarui sistem dan menginstal dependensi..."
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip git ufw

# Klone repositori dari GitHub
echo "Mengkloning repositori dari GitHub..."
git clone https://github.com/testwayweb3-bots/testwayweb3-bots.git
cd testwayweb3-bots

# Buat dan aktifkan virtual environment
echo "Membuat virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Instal dependensi Python
echo "Menginstal dependensi Python..."
pip install -r requirements.txt

# Minta pengguna untuk memasukkan API key dan token
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

# Atur firewall untuk keamanan
echo "Mengatur firewall (UFW)..."
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP (opsional, jika bot menggunakan webhook)
sudo ufw enable

# Instal PM2 untuk menjalankan bot secara persisten
echo "Menginstal PM2 untuk menjalankan bot 24/7..."
sudo npm install pm2@latest -g

# Jalankan bot menggunakan PM2
echo "Menjalankan bot dengan PM2..."
pm2 start telegram_bot.py --name "web3-bot" --interpreter python3
pm2 save
pm2 startup

# Tampilkan status
echo "Bot telah dijalankan! Status:"
pm2 list

echo "Selesai! Bot sudah berjalan di VPS baru."
