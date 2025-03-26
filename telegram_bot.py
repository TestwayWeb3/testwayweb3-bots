import telebot
import requests
from notion_client import Client
import os
from datetime import datetime

bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'))
notion = Client(auth=os.environ.get('NOTION_API_KEY'))
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Saya bot untuk menambah kegiatan Web3 ke Notion. Gunakan perintah /add_activity untuk menambah entri. Contoh:\n/add_activity Stride Testnet Jul2024 0x123 https://x.com/TestwayWeb3 ModerasiArtikel Selesai 30Apr2025")

@bot.message_handler(commands=['add_activity'])
def add_activity(message):
    try:
        parts = message.text.split(' ', 8)
        if len(parts) != 9:
            bot.reply_to(message, "Format salah. Gunakan: /add_activity [NamaProyek] [JenisAktivitas] [TanggalPartisipasi] [AlamatWallet] [AkunMediaSosial] [Catatan] [Status] [HadiahDiharapkan]\nContoh: /add_activity Stride Testnet Jul2024 0x123 https://x.com/TestwayWeb3 ModerasiArtikel Selesai 30Apr2025")
            return

        nama_proyek, jenis_aktivitas, tanggal_partisipasi, alamat_wallet, akun_media_sosial, catatan, status, hadiah_diharapkan = parts[1:9]

        tanggal_partisipasi = datetime.strptime(tanggal_partisipasi, '%b%Y').strftime('%Y-%m-%d')
        hadiah_diharapkan = datetime.strptime(hadiah_diharapkan, '%d%b%Y').strftime('%Y-%m-%d')

        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Nama Proyek": {"title": [{"text": {"content": nama_proyek}}]},
                "Jenis Aktivitas": {"select": {"name": jenis_aktivitas}},
                "Tanggal Partisipasi": {"date": {"start": tanggal_partisipasi}},
                "Alamat Wallet": {"rich_text": [{"text": {"content": alamat_wallet}}]},
                "Akun Media Sosial Terkait": {"url": akun_media_sosial},
                "Catatan": {"rich_text": [{"text": {"content": catatan}}]},
                "Status": {"select": {"name": status}},
                "Hadiah/Acara yang Diharapkan": {"date": {"start": hadiah_diharapkan}},
            }
        )
        bot.reply_to(message, f"Berhasil menambahkan {nama_proyek} ke rekap Notion!")
    except Exception as e:
        bot.reply_to(message, f"Gagal menambahkan entri: {str(e)}")

bot.infinity_polling()
