import requests
from notion_client import Client
import os
from datetime import datetime
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Muat file .env
load_dotenv()

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Validasi kredensial
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')

logger.debug("Membaca TELEGRAM_BOT_TOKEN: %s", TELEGRAM_BOT_TOKEN)
logger.debug("Membaca NOTION_API_KEY: %s", NOTION_API_KEY)
logger.debug("Membaca NOTION_DATABASE_ID: %s", DATABASE_ID)

if not TELEGRAM_BOT_TOKEN or not NOTION_API_KEY or not DATABASE_ID:
    logger.error("Kredensial tidak lengkap: TELEGRAM_BOT_TOKEN=%s, NOTION_API_KEY=%s, DATABASE_ID=%s", 
                 TELEGRAM_BOT_TOKEN, NOTION_API_KEY, DATABASE_ID)
    raise ValueError("Kredensial TELEGRAM_BOT_TOKEN, NOTION_API_KEY, atau DATABASE_ID tidak ditemukan. Periksa file .env.")

# Inisialisasi bot dan Notion client
notion = Client(auth=NOTION_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Menerima perintah /start dari user: %s", update.message.from_user.id)
    await update.message.reply_text(
        "Halo! Saya bot untuk menambah kegiatan Web3 ke Notion. Gunakan perintah /add_activity untuk menambah entri. Contoh:\n"
        "/add_activity Stride Testnet Jul2024 0x123 https://x.com/TestwayWeb3 ModerasiArtikel Selesai 30Apr2025"
    )

async def add_activity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Menerima perintah /add_activity: %s", update.message.text)
    try:
        parts = update.message.text.split(' ', 8)
        logger.debug("Memisahkan input: %s", parts)
        if len(parts) != 9:
            await update.message.reply_text(
                "Format salah. Gunakan: /add_activity [NamaProyek] [JenisAktivitas] [TanggalPartisipasi] [AlamatWallet] "
                "[AkunMediaSosial] [Catatan] [Status] [HadiahDiharapkan]\n"
                "Contoh: /add_activity Stride Testnet Jul2024 0x123 https://x.com/TestwayWeb3 ModerasiArtikel Selesai 30Apr2025"
            )
            return

        nama_proyek, jenis_aktivitas, tanggal_partisipasi, alamat_wallet, akun_media_sosial, catatan, status, hadiah_diharapkan = parts[1:9]
        logger.debug("Data yang diambil: %s, %s, %s, %s, %s, %s, %s, %s", 
                     nama_proyek, jenis_aktivitas, tanggal_partisipasi, alamat_wallet, 
                     akun_media_sosial, catatan, status, hadiah_diharapkan)

        try:
            tanggal_partisipasi = datetime.strptime(tanggal_partisipasi, '%b%Y').strftime('%Y-%m-%d')
        except ValueError:
            logger.error("Format tanggal partisipasi salah: %s", tanggal_partisipasi)
            await update.message.reply_text("Format Tanggal Partisipasi salah. Gunakan format 'BulanTahun' (contoh: Jul2024).")
            return

        try:
            hadiah_diharapkan = datetime.strptime(hadiah_diharapkan, '%d%b%Y').strftime('%Y-%m-%d')
        except ValueError:
            logger.error("Format hadiah diharapkan salah: %s", hadiah_diharapkan)
            await update.message.reply_text("Format Hadiah Diharapkan salah. Gunakan format 'TanggalBulanTahun' (contoh: 30Apr2025).")
            return

        logger.debug("Tanggal setelah konversi: %s, %s", tanggal_partisipasi, hadiah_diharapkan)

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
        logger.debug("Berhasil menambahkan entri ke Notion")
        await update.message.reply_text(f"Berhasil menambahkan {nama_proyek} ke rekap Notion!")
    except Exception as e:
        logger.error("Gagal menambahkan entri: %s", str(e))
        await update.message.reply_text(f"Gagal menambahkan entri: {str(e)}")

def main() -> None:
    # Buat aplikasi dengan token bot
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Tambahkan handler untuk perintah
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_activity", add_activity))

    # Jalankan bot
    application.run_polling()

if __name__ == '__main__':
    main()
