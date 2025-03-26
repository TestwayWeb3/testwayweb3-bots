# Panduan Instalasi Web3ActivityBot (Bahasa Indonesia)

Panduan ini memberikan langkah-langkah terperinci untuk menginstal dan menjalankan **Web3ActivityBot** di VPS baru. Bot ini membantu Anda mencatat aktivitas Web3 (seperti testnet, airdrop) ke dalam database Notion melalui Telegram. Anda dapat memilih untuk mengikuti langkah instalasi manual atau menggunakan skrip otomatis `install.sh`.

## Prasyarat

Sebelum memulai, pastikan Anda memiliki:

- VPS yang menjalankan Ubuntu (misalnya, Ubuntu 20.04 atau versi lebih baru).
- Token bot Telegram (dapatkan dengan membuat bot melalui [BotFather](https://t.me/BotFather) di Telegram).
- Kunci API Notion dan ID database (lihat bagian [Pengaturan API Notion](#pengaturan-api-notion)).
- Token Akses Pribadi GitHub (PAT) untuk mengakses repositori (jika repositori bersifat privat).
- Pengetahuan dasar tentang perintah terminal Linux.
- Cadangan file `.env` dari VPS saat ini (berisi `TELEGRAM_BOT_TOKEN`, `NOTION_API_KEY`, dan `NOTION_DATABASE_ID`) sebelum VPS berakhir.

## Opsi 1: Instalasi Otomatis Menggunakan `install.sh`

### 1. Hubungkan ke VPS Baru Anda
Gunakan SSH untuk terhubung ke VPS baru Anda:
ssh username@your-vps-ip
Ganti username dengan nama pengguna VPS Anda.
Ganti your-vps-ip dengan alamat IP VPS Anda.

### 2. Kloning Repositori
Kloning repositori bot dari GitHub:
```bash
git clone https://github.com/TestwayWeb3/testwayweb3-bots.git ~/testwayweb3-bots
```
Jika repositori bersifat privat, gunakan PAT GitHub Anda:
```bash
git clone https://<your-github-pat>@github.com/TestwayWeb3/testwayweb3-bots.git ~/testwayweb3-bots
```
Ganti <your-github-pat> dengan Token Akses Pribadi GitHub Anda.
### 3. Jalankan Skrip install.sh
Masuk ke direktori proyek:
```bash
cd ~/testwayweb3-bots
```
Jadikan skrip dapat dieksekusi:
```bash
chmod +x install.sh
```
Jalankan skrip:
```bash
./install.sh
```
Ikuti petunjuk yang muncul:
Jika repositori privat, masukkan PAT GitHub Anda saat diminta.
Jika file .env tidak ada atau Anda memilih untuk menimpanya, masukkan token bot Telegram, kunci API Notion, dan ID database Notion (pastikan Anda telah mencadangkan informasi ini dari VPS sebelumnya).
Uji bot di Telegram saat diminta dengan mengirimkan perintah `/start` dan `/add_activity`, lalu konfirmasi apakah bot berfungsi dengan baik.

### 4. Verifikasi Bot
Setelah skrip selesai, periksa status bot:
```bash
pm2 list
```
Lihat log jika diperlukan:
```bash
pm2 logs web3-bot
```
## Opsi 2: Instalasi Manual
### 1. Hubungkan ke VPS Baru Anda
Gunakan SSH untuk terhubung ke VPS baru Anda:
```bash
ssh username@your-vps-ip
```
Ganti username dengan nama pengguna VPS Anda.
Ganti your-vps-ip dengan alamat IP VPS Anda.

## 2. Perbarui Sistem
Pastikan sistem Anda sudah terbarui:
```bash
sudo apt update && sudo apt upgrade -y
```
### 3. Instal Perangkat Lunak yang Diperlukan
Instal Python 3, pip, dan Git:
```bash
sudo apt install python3 python3-pip git -y
```
Instal Node.js dan npm (diperlukan untuk PM2, manajer proses agar bot tetap berjalan):
```bash
sudo apt install nodejs npm -y
```
Instal PM2 secara global:
```bash
sudo npm install -g pm2
```
### 4. Kloning Repositori
Kloning repositori bot dari GitHub:
```bash
git clone https://github.com/TestwayWeb3/testwayweb3-bots.git ~/testwayweb3-bots
```
Jika repositori bersifat privat, gunakan PAT GitHub Anda:
```bash
git clone https://<your-github-pat>@github.com/TestwayWeb3/testwayweb3-bots.git ~/testwayweb3-bots
```
Ganti <your-github-pat> dengan Token Akses Pribadi GitHub Anda.
### 5. Siapkan Lingkungan Virtual
Masuk ke direktori proyek:
```bash
cd ~/testwayweb3-bots
```
Buat dan aktifkan lingkungan virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```
Instal paket Python yang diperlukan menggunakan requirements.txt:
```bash
pip install -r requirements.txt
```
Jika requirements.txt tidak ada, buat file tersebut dengan konten berikut:
`plaintext
python-telegram-bot==20.0
notion-client
python-dotenv`
Kemudian jalankan:
```bash
echo -e "python-telegram-bot==20.0\nnotion-client\npython-dotenv" > requirements.txt
pip install -r requirements.txt
```
### 6. Konfigurasi Variabel Lingkungan
Buat file .env di direktori proyek:
```bash
nano ~/testwayweb3-bots/.env
```
Tambahkan variabel lingkungan berikut (gunakan nilai dari file .env yang telah dicadangkan):
```plaintext
TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
NOTION_API_KEY="your-notion-api-key"
NOTION_DATABASE_ID="your-notion-database-id"
TELEGRAM_BOT_TOKEN: Token bot Telegram Anda dari BotFather.
NOTION_API_KEY: Kunci API Notion Anda.
NOTION_DATABASE_ID: ID database Notion Anda.
```
Simpan file (Ctrl+O, Enter, Ctrl+X di nano).

### 7. Verifikasi Struktur Database Notion
Buka database Notion Anda. Pastikan database memiliki kolom berikut dengan tipe dan opsi yang benar:
Nama Proyek: Tipe Title
Jenis Aktivitas: Tipe Select (opsi: `Testnet`, `Node`, `Airdrop`, `Waitlist`, `Staking`, `Daily`, `Minting`)
Jaringan: Tipe Select (opsi: `SOL`, `BSC`, `ETH`, `BASE`, `OP`, `MONAD`, `AVAX`, `ZK`, `LINEA`, `BTC`, `SUI`, `APTOS`)
Tanggal Partisipasi: Tipe Date
Alamat Wallet: Tipe Rich Text
Link Garapan: Tipe URL
Catatan: Tipe Rich Text
Status: Tipe Status (opsi: Waiting List, Belum Garap, Sudah Garap)
Status Landing: Tipe Select (opsi: Sudah Landing, Belum Landing)
Total Hadiah: Tipe Number
Jika ada opsi atau kolom yang hilang atau berbeda, perbarui database atau modifikasi kode bot (telegram_bot.py) agar sesuai.

### 8. Uji Bot
Jalankan bot secara manual untuk memastikan berfungsi:
```bash
python3 telegram_bot.py
```
Buka Telegram, cari bot Anda, dan kirim perintah `/start` serta `/add_activity`. Ikuti petunjuk untuk memastikan bot berjalan dengan benar dan mencatat entri di database Notion Anda. Periksa database Notion untuk memastikan entri ditambahkan dengan nilai yang benar.

### 9. Jalankan Bot dengan PM2
Jika bot berjalan dengan sukses, atur agar berjalan terus-menerus menggunakan PM2:
```bash
pm2 start ~/testwayweb3-bots/telegram_bot.py --name "web3-bot" --interpreter ~/testwayweb3-bots/venv/bin/python3
```
Simpan daftar proses PM2 untuk memastikan bot restart saat VPS reboot:
```bash
pm2 save
```
Konfigurasi PM2 untuk mulai saat boot:
```bash
pm2 startup
```
Ikuti instruksi di layar untuk menjalankan perintah yang dihasilkan (misalnya, sudo ...).
Periksa status bot:
```bash
pm2 list
```
Lihat log bot jika diperlukan:
```bash
pm2 logs web3-bot
```
### 10. (Opsional) Perbarui Kode Bot
Jika Anda perlu memperbarui kode bot di masa depan, tarik perubahan terbaru dari GitHub:
```bash
cd ~/testwayweb3-bots
git pull origin main
```
Jika repositori bersifat privat, gunakan PAT GitHub Anda:
```bash
export GITHUB_PAT=your-github-pat
git pull https://${GITHUB_PAT}@github.com/TestwayWeb3/testwayweb3-bots.git main
unset GITHUB_PAT
```
Restart bot setelah memperbarui:
```bash
pm2 restart web3-bot
```
## Mendorong Perubahan ke GitHub
Jika Anda membuat perubahan pada kode bot atau file lain (misalnya, install.sh, README.md), Anda dapat mendorongnya ke GitHub untuk memastikan versi terbaru tersimpan di repositori.
### 1. Masuk ke Direktori Proyek
Pastikan Anda berada di direktori testwayweb3-bots:
```bash
cd ~/testwayweb3-bots
```
### 2. Periksa Status Perubahan
Lihat file mana yang telah dimodifikasi atau ditambahkan:
```bash
git status
```
### 3. Stage Perubahan
Tambahkan file yang dimodifikasi atau baru ke area staging:
```bash
git add <file1> <file2>
```
Misalnya, jika Anda memodifikasi install.sh dan README.md:
```bash
git add install.sh README.md
```
### 4. Commit Perubahan
Buat commit dengan pesan deskriptif:
```bash
git commit -m "Memperbarui install.sh dan README.md untuk pengaturan otomatis"
```
### 5. Push ke GitHub
Gunakan Token Akses Pribadi GitHub (PAT) Anda untuk mendorong perubahan ke branch main:
```bash
export GITHUB_PAT=your-github-pat
git push https://${GITHUB_PAT}@github.com/TestwayWeb3/testwayweb3-bots.git main
unset GITHUB_PAT
```
Jika Anda tidak memiliki PAT, buat satu:
Buka GitHub Settings > Developer settings > Personal access tokens.
Klik "Generate new token," pilih scope repo, dan buat token.

### 6. Verifikasi Push
Periksa repositori [GitHub](https://github.com/TestwayWeb3/testwayweb3-bots) di browser Anda untuk memastikan file yang diperbarui ada di branch main. Alternatifnya, periksa riwayat commit di VPS:
```bash
git log --oneline -n 1
```
## Pengaturan API Notion
### 1. Buat Integrasi Notion
Buka Notion Integrations.
Klik "New Integration," beri nama (misalnya, "`Web3ActivityBot`"), dan submit.
Salin "Internal Integration Token" (ini adalah NOTION_API_KEY Anda).
### 2. Bagikan Database Anda dengan Integrasi
Buka database Notion Anda.
Klik "Share" di pojok kanan atas.
Aktifkan "Share to web" jika diperlukan, dan di bawah "Share with an integration," pilih integrasi Anda (misalnya, "Web3ActivityBot").
Pastikan integrasi memiliki akses penuh (edit, komentar, dll.).
### 3. Verifikasi ID Database
ID database dapat ditemukan di URL database Notion Anda. Pastikan ini sesuai dengan NOTION_DATABASE_ID di file .env Anda.
Pemecahan Masalah
Bot Tidak Merespons di Telegram
Periksa log:
```bash
pm2 logs web3-bot
```
Pastikan TELEGRAM_BOT_TOKEN di `.env` benar dan bot tidak diblokir di Telegram.
Pastikan bot berjalan:
```bash
pm2 list
```
Kesalahan API Notion (misalnya, "Property not found")
Pastikan `NOTION_API_KEY` dan `NOTION_DATABASE_ID` di `.env` benar.
Pastikan database dibagikan dengan integrasi (lihat Pengaturan API Notion (#pengaturan-api-notion)).
Periksa struktur database Notion (lihat Verifikasi Struktur Database Notion (#verifikasi-struktur-database-notion)) untuk memastikan semua kolom dan opsi sesuai dengan harapan bot.
Masalah Dependensi
Pastikan semua paket terinstal:
```bash
pip install -r requirements.txt
```
Jika ada paket yang hilang, instal secara manual (misalnya, pip install python-telegram-bot==20.0).
Restart VPS
Jika VPS restart, PM2 seharusnya secara otomatis menjalankan ulang bot jika Anda mengatur pm2 startup dan menjalankan pm2 save.
Versi Bot Lama Berjalan
Hentikan semua instance bot:
```bash
pm2 delete web3-bot
```
Jalankan bot secara manual untuk menguji:
```bash
python3 telegram_bot.py
```
Restart dengan PM2:
```bash
pm2 start ~/testwayweb3-bots/telegram_bot.py --name "web3-bot" --interpreter ~/testwayweb3-bots/venv/bin/python3
```
Kesalahan Push Git
"remote: Permission denied": PAT GitHub mungkin salah atau kadaluarsa. Buat PAT baru dan coba lagi.
"remote: Repository not found": Pastikan URL repositori dan izin akses Anda benar.
Sebelum VPS Saat Ini Berakhir
Cadangkan File .env
Salin file .env ke lokasi aman (misalnya, komputer lokal Anda):
```bash
scp username@your-vps-ip:~/testwayweb3-bots/.env ~/backup_env
```
Ganti username dan your-vps-ip dengan detail VPS Anda.
File ini berisi TELEGRAM_BOT_TOKEN, NOTION_API_KEY, dan NOTION_DATABASE_ID, yang akan Anda perlukan untuk VPS baru.
Cadangkan Perubahan Kode Kustom
Jika Anda telah membuat perubahan pada telegram_bot.py, cadangkan file:
```bash
scp username@your-vps-ip:~/testwayweb3-bots/telegram_bot.py ~/backup_telegram_bot.py
```
Alternatifnya, commit dan push perubahan ke GitHub (lihat Mendorong Perubahan ke GitHub (#mendorong-perubahan-ke-github)).

## Kontribusi
### Untuk berkontribusi pada bot ini, fork repositori, buat perubahan, dan ajukan pull request ke [TestwayWeb3](https://github.com/TestwayWeb3/testwayweb3-bots).

## Lisensi
### Proyek ini dilisensikan di bawah Lisensi [MIT](https://opensource.org/licenses/MIT).
