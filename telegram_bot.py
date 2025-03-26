import requests
from notion_client import Client
import os
from datetime import datetime
import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Validate credentials
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')

logger.debug("Reading TELEGRAM_BOT_TOKEN: %s", TELEGRAM_BOT_TOKEN)
logger.debug("Reading NOTION_API_KEY: %s", NOTION_API_KEY)
logger.debug("Reading NOTION_DATABASE_ID: %s", DATABASE_ID)

if not TELEGRAM_BOT_TOKEN or not NOTION_API_KEY or not DATABASE_ID:
    logger.error("Credentials are incomplete: TELEGRAM_BOT_TOKEN=%s, NOTION_API_KEY=%s, DATABASE_ID=%s", 
                 TELEGRAM_BOT_TOKEN, NOTION_API_KEY, DATABASE_ID)
    raise ValueError("Credentials TELEGRAM_BOT_TOKEN, NOTION_API_KEY, or DATABASE_ID not found. Check .env file.")

# Initialize Notion client
notion = Client(auth=NOTION_API_KEY)

# Define states for ConversationHandler
NAMA_PROYEK, JENIS_AKTIVITAS, JARINGAN, BULAN_PARTISIPASI, TAHUN_PARTISIPASI, TANGGAL_PARTISIPASI, ALAMAT_WALLET, LINK_GARAPAN, CATATAN, STATUS, STATUS_LANDING, TOTAL_HADIAH = range(12)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug("Received /start from user: %s", update.message.from_user.id)
    await update.message.reply_text(
        "🌟 Halo! Saya Web3ActivityBot, siap membantu kamu mencatat semua kegiatan Web3 di Notion dengan mudah! 🚀 "
        "Ketik /add_activity untuk mulai, dan ikuti langkah-langkahnya dengan tombol interaktif yang super praktis! 😊"
    )

async def add_activity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.debug("Received /add_activity from user: %s", update.message.from_user.id)
    await update.message.reply_text("✨ Mari kita mulai! Masukkan Nama Proyek yang kamu ikuti (contoh: MONAD):")
    return NAMA_PROYEK

async def nama_proyek(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['nama_proyek'] = update.message.text

    # Buttons for Jenis Aktivitas
    keyboard = [
        [InlineKeyboardButton("Testnet", callback_data="Testnet"),
         InlineKeyboardButton("Node", callback_data="Node")],
        [InlineKeyboardButton("Airdrop", callback_data="Airdrop"),
         InlineKeyboardButton("Waitlist", callback_data="Waitlist")],
        [InlineKeyboardButton("Staking", callback_data="Staking"),
         InlineKeyboardButton("Daily", callback_data="Daily")],
        [InlineKeyboardButton("Minting", callback_data="Minting")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎯 Apa jenis aktivitas Web3 yang kamu ikuti? Pilih salah satu di bawah ini:", reply_markup=reply_markup)
    return JENIS_AKTIVITAS

async def jenis_aktivitas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['jenis_aktivitas'] = query.data
    await query.message.reply_text(f"Jenis Aktivitas dipilih: {query.data}")

    # Buttons for Jaringan
    keyboard = [
        [InlineKeyboardButton("SOL", callback_data="SOL"),
         InlineKeyboardButton("BSC", callback_data="BSC")],
        [InlineKeyboardButton("ETH", callback_data="ETH"),
         InlineKeyboardButton("BASE", callback_data="BASE")],
        [InlineKeyboardButton("OP", callback_data="OP"),
         InlineKeyboardButton("MONAD", callback_data="MONAD")],
        [InlineKeyboardButton("AVAX", callback_data="AVAX"),
         InlineKeyboardButton("ZK", callback_data="ZK")],
        [InlineKeyboardButton("LINEA", callback_data="LINEA"),
         InlineKeyboardButton("BTC", callback_data="BTC")],
        [InlineKeyboardButton("SUI", callback_data="SUI"),
         InlineKeyboardButton("APTOS", callback_data="APTOS")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("🔗 Proyek ini berjalan di jaringan apa? Pilih jaringan di bawah ini:", reply_markup=reply_markup)
    return JARINGAN

async def jaringan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['jaringan'] = query.data
    await query.message.reply_text(f"Jaringan dipilih: {query.data}")

    # Buttons for Bulan Partisipasi
    keyboard = [
        [InlineKeyboardButton("Jan", callback_data="Jan"),
         InlineKeyboardButton("Feb", callback_data="Feb"),
         InlineKeyboardButton("Mar", callback_data="Mar")],
        [InlineKeyboardButton("Apr", callback_data="Apr"),
         InlineKeyboardButton("May", callback_data="May"),
         InlineKeyboardButton("Jun", callback_data="Jun")],
        [InlineKeyboardButton("Jul", callback_data="Jul"),
         InlineKeyboardButton("Aug", callback_data="Aug"),
         InlineKeyboardButton("Sep", callback_data="Sep")],
        [InlineKeyboardButton("Oct", callback_data="Oct"),
         InlineKeyboardButton("Nov", callback_data="Nov"),
         InlineKeyboardButton("Dec", callback_data="Dec")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("📅 Kapan kamu mulai berpartisipasi? Pilih bulan di bawah ini:", reply_markup=reply_markup)
    return BULAN_PARTISIPASI

async def bulan_partisipasi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['bulan_partisipasi'] = query.data
    await query.message.reply_text(f"Bulan Partisipasi dipilih: {query.data}")

    # Buttons for Tahun Partisipasi
    keyboard = [
        [InlineKeyboardButton("2024", callback_data="2024"),
         InlineKeyboardButton("2025", callback_data="2025"),
         InlineKeyboardButton("2026", callback_data="2026")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("🗓️ Tahun berapa kamu ikut proyek ini? Pilih tahun di bawah ini:", reply_markup=reply_markup)
    return TAHUN_PARTISIPASI

async def tahun_partisipasi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['tahun_partisipasi'] = query.data
    await query.message.reply_text(f"Tahun Partisipasi dipilih: {query.data}")
    await query.message.reply_text("🕒 Masukkan tanggal kamu mulai berpartisipasi (contoh: 26):")
    return TANGGAL_PARTISIPASI

async def tanggal_partisipasi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tanggal = update.message.text
    try:
        tanggal = int(tanggal)
        if not 1 <= tanggal <= 31:
            raise ValueError("Tanggal harus antara 1 dan 31.")
        bulan = context.user_data['bulan_partisipasi']
        tahun = context.user_data['tahun_partisipasi']
        # Map month name to number
        month_map = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }
        month = month_map[bulan]
        year = int(tahun)
        # Validate date
        import calendar
        if month == 2:
            if not calendar.isleap(year) and tanggal > 28:
                raise ValueError("Februari hanya memiliki 28 hari pada tahun non-kabisat.")
            elif calendar.isleap(year) and tanggal > 29:
                raise ValueError("Februari hanya memiliki 29 hari pada tahun kabisat.")
        elif month in [4, 6, 9, 11] and tanggal > 30:
            raise ValueError("Bulan ini hanya memiliki 30 hari.")
        # If valid, format date
        tanggal_partisipasi = datetime(year, month, tanggal).strftime('%Y-%m-%d')
        context.user_data['tanggal_partisipasi'] = tanggal_partisipasi
        await update.message.reply_text("💳 Masukkan alamat wallet yang kamu gunakan untuk proyek ini (contoh: 0x123...):")
        return ALAMAT_WALLET
    except ValueError as e:
        await update.message.reply_text(str(e))
        return TANGGAL_PARTISIPASI

async def alamat_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    alamat_wallet = update.message.text
    jaringan = context.user_data['jaringan']

    # Validate wallet address based on network
    if jaringan != "SOL":
        if not re.match(r'^0x[a-fA-F0-9]{40}$', alamat_wallet):
            await update.message.reply_text(f"Alamat Wallet untuk {jaringan} harus diawali '0x' dan panjang 42 karakter (contoh: 0x123...). Coba lagi:")
            return ALAMAT_WALLET
    else:
        if not re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', alamat_wallet):
            await update.message.reply_text(f"Alamat Wallet untuk SOL harus panjang 32-44 karakter (contoh: 5y2...). Coba lagi:")
            return ALAMAT_WALLET

    context.user_data['alamat_wallet'] = alamat_wallet
    await update.message.reply_text("🔗 Masukkan link garapan proyek, seperti channel Telegram (contoh: https://t.me/channel):")
    return LINK_GARAPAN

async def link_garapan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['link_garapan'] = update.message.text
    await update.message.reply_text("📝 Ada catatan tambahan untuk proyek ini? (contoh: ModerasiArtikel):")
    return CATATAN

async def catatan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['catatan'] = update.message.text

    # Buttons for Status
    keyboard = [
        [InlineKeyboardButton("Sudah Garap", callback_data="Sudah Garap"),
         InlineKeyboardButton("Belum Garap", callback_data="Belum Garap")],
        [InlineKeyboardButton("Waiting List", callback_data="Waiting List")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📊 Bagaimana status partisipasi kamu di proyek ini? Pilih di bawah ini:", reply_markup=reply_markup)
    return STATUS

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['status'] = query.data
    await query.message.reply_text(f"Status dipilih: {query.data}")

    # Buttons for Status Landing
    keyboard = [
        [InlineKeyboardButton("Sudah Landing", callback_data="Sudah Landing"),
         InlineKeyboardButton("Belum Landing", callback_data="Belum Landing")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("🎁 Apakah hadiah dari proyek ini sudah landing? Pilih di bawah ini:", reply_markup=reply_markup)
    return STATUS_LANDING

async def status_landing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['status_landing'] = query.data
    await query.message.reply_text(f"Status Landing dipilih: {query.data}")

    if query.data == "Sudah Landing":
        await query.message.reply_text("💰 Berapa total hadiah yang kamu dapatkan? Masukkan angka (contoh: 100):")
        return TOTAL_HADIAH
    else:
        # Save to Notion if "Belum Landing"
        nama_proyek = context.user_data['nama_proyek']
        jenis_aktivitas = context.user_data['jenis_aktivitas']
        jaringan = context.user_data['jaringan']
        tanggal_partisipasi = context.user_data['tanggal_partisipasi']
        alamat_wallet = context.user_data['alamat_wallet']
        link_garapan = context.user_data['link_garapan']
        catatan = context.user_data['catatan']
        status = context.user_data['status']
        status_landing = context.user_data['status_landing']

        try:
            notion.pages.create(
                parent={"database_id": DATABASE_ID},
                properties={
                    "Nama Proyek": {"title": [{"text": {"content": nama_proyek}}]},
                    "Jenis Aktivitas": {"select": {"name": jenis_aktivitas}},
                    "Jaringan": {"select": {"name": jaringan}},
                    "Tanggal Partisipasi": {"date": {"start": tanggal_partisipasi}},
                    "Alamat Wallet": {"rich_text": [{"text": {"content": alamat_wallet}}]},
                    "Link Garapan": {"url": link_garapan},
                    "Catatan": {"rich_text": [{"text": {"content": catatan}}]},
                    "Status": {"status": {"name": status}},
                    "Status Landing": {"select": {"name": status_landing}},
                }
            )
            logger.debug("Berhasil menambahkan entri ke Notion")
            await query.message.reply_text(f"🎉 Yeay! {nama_proyek} berhasil ditambahkan ke rekap Notion kamu! 🚀")
        except Exception as e:
            logger.error("Gagal menambahkan entri: %s", str(e))
            await query.message.reply_text(f"Gagal menambahkan entri: {str(e)}")
        return ConversationHandler.END

async def total_hadiah(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    total_hadiah = update.message.text
    try:
        total_hadiah = float(total_hadiah)
        if total_hadiah < 0:
            raise ValueError("Total hadiah tidak boleh negatif.")
        context.user_data['total_hadiah'] = total_hadiah

        # Save to Notion
        nama_proyek = context.user_data['nama_proyek']
        jenis_aktivitas = context.user_data['jenis_aktivitas']
        jaringan = context.user_data['jaringan']
        tanggal_partisipasi = context.user_data['tanggal_partisipasi']
        alamat_wallet = context.user_data['alamat_wallet']
        link_garapan = context.user_data['link_garapan']
        catatan = context.user_data['catatan']
        status = context.user_data['status']
        status_landing = context.user_data['status_landing']
        total_hadiah = context.user_data['total_hadiah']

        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Nama Proyek": {"title": [{"text": {"content": nama_proyek}}]},
                "Jenis Aktivitas": {"select": {"name": jenis_aktivitas}},
                "Jaringan": {"select": {"name": jaringan}},
                "Tanggal Partisipasi": {"date": {"start": tanggal_partisipasi}},
                "Alamat Wallet": {"rich_text": [{"text": {"content": alamat_wallet}}]},
                "Link Garapan": {"url": link_garapan},
                "Catatan": {"rich_text": [{"text": {"content": catatan}}]},
                "Status": {"status": {"name": status}},
                "Status Landing": {"select": {"name": status_landing}},
                "Total Hadiah": {"number": total_hadiah},
            }
        )
        logger.debug("Berhasil menambahkan entri ke Notion")
        await update.message.reply_text(f"🎉 Yeay! {nama_proyek} berhasil ditambahkan ke rekap Notion kamu! 🚀")
    except ValueError as e:
        await update.message.reply_text(f"❌ {str(e)} Masukkan angka yang valid (contoh: 100):")
        return TOTAL_HADIAH
    except Exception as e:
        logger.error("Gagal menambahkan entri: %s", str(e))
        await update.message.reply_text(f"Gagal menambahkan entri: {str(e)}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Pencatatan telah dibatalkan. Ketik /add_activity untuk memulai lagi ya! 😊")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # ConversationHandler for add_activity
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_activity", add_activity)],
        states={
            NAMA_PROYEK: [MessageHandler(filters.TEXT & ~filters.COMMAND, nama_proyek)],
            JENIS_AKTIVITAS: [CallbackQueryHandler(jenis_aktivitas)],
            JARINGAN: [CallbackQueryHandler(jaringan)],
            BULAN_PARTISIPASI: [CallbackQueryHandler(bulan_partisipasi)],
            TAHUN_PARTISIPASI: [CallbackQueryHandler(tahun_partisipasi)],
            TANGGAL_PARTISIPASI: [MessageHandler(filters.TEXT & ~filters.COMMAND, tanggal_partisipasi)],
            ALAMAT_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, alamat_wallet)],
            LINK_GARAPAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, link_garapan)],
            CATATAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, catatan)],
            STATUS: [CallbackQueryHandler(status)],
            STATUS_LANDING: [CallbackQueryHandler(status_landing)],
            TOTAL_HADIAH: [MessageHandler(filters.TEXT & ~filters.COMMAND, total_hadiah)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
