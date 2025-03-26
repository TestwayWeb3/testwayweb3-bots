# Web3ActivityBot Installation Guide

This guide provides detailed instructions to install and run the Web3ActivityBot on a new VPS. The bot helps you record Web3 activities (e.g., testnets, airdrops) in a Notion database using Telegram. You can either follow the manual installation steps or use the automated `install.sh` script.

## Prerequisites
- A VPS running Ubuntu (e.g., Ubuntu 20.04 or later).
- A Telegram bot token (get one by creating a bot via [BotFather](https://t.me/BotFather) on Telegram).
- A Notion API key and database ID (see [Notion API Setup](#notion-api-setup) below).
- A GitHub Personal Access Token (PAT) for accessing your repository (if private).
- Basic familiarity with Linux terminal commands.
- Back up your `.env` file from the current VPS (contains `TELEGRAM_BOT_TOKEN`, `NOTION_API_KEY`, and `NOTION_DATABASE_ID`) before the VPS expires.

## Option 1: Automated Installation Using `install.sh`

### 1. Connect to Your New VPS
- Use SSH to connect to your new VPS:
  ```bash
  ssh username@your-vps-ip
  Replace username with your VPS username and your-vps-ip with your VPS IP address.
2. Clone the Repository
Clone the bot's repository from GitHub:
bash
git clone https://github.com/TestwayWeb3/testwayweb3-bots.git ~/testwayweb3-bots
If the repository is private, use your GitHub PAT:
bash
git clone https://<your-github-pat>@github.com/TestwayWeb3/testwayweb3-bots.git ~/testwayweb3-bots
Replace <your-github-pat> with your GitHub Personal Access Token.
3. Run the install.sh Script
Navigate to the project directory:
bash
cd ~/testwayweb3-bots
Make the script executable:
bash
chmod +x install.sh
Run the script:
bash
./install.sh
Follow the prompts:
If the repository is private, enter your GitHub PAT when prompted.
If a .env file does not exist or you choose to overwrite it, provide your Telegram bot token, Notion API key, and Notion database ID (you should have these backed up from your current VPS).
Test the bot in Telegram when prompted by sending /start and /add_activity, then confirm if it works.
4. Verify the Bot
After the script completes, check the bot's status:
bash
pm2 list
View logs if needed:
bash
pm2 logs web3-bot
Option 2: Manual Installation Steps
1. Connect to Your New VPS
Use SSH to connect to your new VPS:
bash
ssh username@your-vps-ip
Replace username with your VPS username and your-vps-ip with your VPS IP address.
2. Update the System
Ensure your system is up to date:
bash
sudo apt update && sudo apt upgrade -y
3. Install Required Software
Install Python 3, pip, and Git:
bash
sudo apt install python3 python3-pip git -y
Install Node.js and npm (required for PM2, a process manager to keep the bot running):
bash
sudo apt install nodejs npm -y
Install PM2 globally:
bash
sudo npm install -g pm2
4. Clone the Repository
Clone the bot's repository from GitHub:
bash
git clone https://github.com/TestwayWeb3/testwayweb3-bots.git ~/testwayweb3-bots
If the repository is private, use your GitHub PAT:
bash
git clone https://<your-github-pat>@github.com/TestwayWeb3/testwayweb3-bots.git ~/testwayweb3-bots
Replace <your-github-pat> with your GitHub Personal Access Token.
5. Set Up a Virtual Environment
Navigate to the project directory:
bash
cd ~/testwayweb3-bots
Create and activate a virtual environment:
bash
python3 -m venv venv
source venv/bin/activate
Install the required Python packages using requirements.txt:
bash
pip install -r requirements.txt
If requirements.txt does not exist, create it with the following content:
python-telegram-bot==20.0
notion-client
python-dotenv
Then run:
bash
echo -e "python-telegram-bot==20.0\nnotion-client\npython-dotenv" > requirements.txt
pip install -r requirements.txt
6. Configure Environment Variables
Create a .env file in the project directory:
bash
nano ~/testwayweb3-bots/.env
Add the following environment variables (use the values from your backed-up .env file):
TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
NOTION_API_KEY="your-notion-api-key"
export GITHUB_PAT="your-github-pat"
TELEGRAM_BOT_TOKEN: Your Telegram bot token from BotFather.
NOTION_API_KEY: Your Notion API key (see Notion API Setup (#notion-api-setup)).
NOTION_DATABASE_ID: Your Notion database ID.
Save the file (Ctrl+O, Enter, Ctrl+X).
7. Verify Notion Database Structure
Open your Notion database: Notion Database.
Ensure the database has the following columns with the correct types and options:
Nama Proyek: Title type
Jenis Aktivitas: Select type (options: Testnet, Node, Airdrop, Waitlist, Staking, Daily, Minting)
Jaringan: Select type (options: SOL, BSC, ETH, BASE, OP, MONAD, AVAX, ZK, LINEA, BTC, SUI, APTOS)
Tanggal Partisipasi: Date type
Alamat Wallet: Rich Text type
Link Garapan: URL type
Catatan: Rich Text type
Status: Status type (options: Waiting List, Belum Garap, Sudah Garap)
Status Landing: Select type (options: Sudah Landing, Belum Landing)
Total Hadiah: Number type
If any options or columns are missing or different, update the database or modify the bot's code (telegram_bot.py) to match.
8. Test the Bot
Run the bot manually to ensure it works:
bash
python3 telegram_bot.py
Open Telegram, find your bot, and send /start and /add_activity. Follow the prompts to ensure the bot runs correctly and records entries in your Notion database.
Check the Notion database to confirm the entry is added with the correct values.
9. Run the Bot with PM2
If the bot runs successfully, set it up to run continuously using PM2:
bash
pm2 start ~/testwayweb3-bots/telegram_bot.py --name "web3-bot" --interpreter ~/testwayweb3-bots/venv/bin/python3
Save the PM2 process list to ensure the bot restarts on VPS reboot:
bash
pm2 save
Configure PM2 to start on boot:
bash
pm2 startup
Follow the on-screen instructions to run the generated command (e.g., sudo ...).
Check the bot's status:
bash
pm2 list
View the bot's logs if needed:
bash
pm2 logs web3-bot
10. (Optional) Update the Bot Code
If you need to update the bot's code in the future, pull the latest changes from GitHub:
bash
cd ~/testwayweb3-bots
git pull origin main
If the repository is private, use your GitHub PAT:
bash
export GITHUB_PAT=your-github-pat
git pull https://${GITHUB_PAT}@github.com/TestwayWeb3/testwayweb3-bots.git main
unset GITHUB_PAT
Restart the bot after updating:
bash
pm2 restart web3-bot
Notion API Setup
Create a Notion Integration:
Go to Notion Integrations.
Click "New Integration," name it (e.g., "Web3ActivityBot"), and submit.
Copy the "Internal Integration Token" (this is your NOTION_API_KEY).
Share Your Database with the Integration:
Open your Notion database: Notion Database.
Click "Share" in the top right corner.
Enable "Share to web" if needed, and under "Share with an integration," select your integration (e.g., "Web3ActivityBot").
Ensure the integration has full access (edit, comment, etc.).
Verify Database ID:
The database ID in the URL 2. Ensure this matches the NOTION_DATABASE_ID in your .env file.
Troubleshooting
Bot Not Responding in Telegram:
Check the logs: pm2 logs web3-bot.
Verify the TELEGRAM_BOT_TOKEN in .env is correct and the bot is not blocked in Telegram.
Ensure the bot is running: pm2 list.
Notion API Errors (e.g., "Property not found"):
Verify the NOTION_API_KEY and NOTION_DATABASE_ID in .env.
Ensure the database is shared with the integration (see Notion API Setup (#notion-api-setup)).
Check the Notion database structure (see Verify Notion Database Structure (#verify-notion-database-structure)) to ensure all columns and options match the bot's expectations.
Dependency Issues:
Ensure all packages are installed: pip install -r requirements.txt.
If a package is missing, install it manually (e.g., pip install python-telegram-bot==20.0).
VPS Restart:
If the VPS restarts, PM2 should automatically restart the bot if you configured pm2 startup and ran pm2 save.
Old Bot Version Running:
Stop all bot instances: pm2 delete web3-bot.
Run the bot manually to test: python3 telegram_bot.py.
Restart with PM2: pm2 start ~/testwayweb3-bots/telegram_bot.py --name "web3-bot" --interpreter ~/testwayweb3-bots/venv/bin/python3.
Before Your Current VPS Expires
Back Up the .env File:
Copy the .env file to a safe location (e.g., your local computer):
bash
scp username@your-vps-ip:~/testwayweb3-bots/.env ~/backup_env
Replace username and your-vps-ip with your VPS details.
This file contains your TELEGRAM_BOT_TOKEN, NOTION_API_KEY, and NOTION_DATABASE_ID, which you'll need for the new VPS.
Back Up Any Custom Code Changes:
If you've made changes to telegram_bot.py, back up the file:
bash
scp username@your-vps-ip:~/testwayweb3-bots/telegram_bot.py ~/backup_telegram_bot.py
Alternatively, commit and push changes to GitHub:
bash
cd ~/testwayweb3-bots
git add telegram_bot.py
git commit -m "Backed up bot code before VPS expiration"
export GITHUB_PAT=your-github-pat
git push https://${GITHUB_PAT}@github.com/TestwayWeb3/testwayweb3-bots.git main
unset GITHUB_PAT
Contributing
To contribute to the bot, fork the repository, make changes, and submit a pull request to TestwayWeb3/testwayweb3-bots.
License
This project is licensed under the MIT License.

#### Steps to Implement
1. **Save the Updated `install.sh`:**
   - Replace your current `install.sh` with the updated script:
     ```bash
     nano ~/testwayweb3-bots/install.sh
     ```
     Paste the updated script, save (`Ctrl+O`, Enter, `Ctrl+X`).

2. **Make the Script Executable:**
   - Ensure the script is executable:
     ```bash
     chmod +x ~/testwayweb3-bots/install.sh
     ```

3. **Save the Updated README:**
   - Replace your current `README.md` with the updated content:
     ```bash
     nano ~/testwayweb3-bots/README.md
     ```
     Paste the updated README, save (`Ctrl+O`, Enter, `Ctrl+X`).

4. **Push Changes to GitHub:**
   - Add and commit the updated files:
     ```bash
     cd ~/testwayweb3-bots
     git add install.sh README.md
     git commit -m "Updated install.sh and README with instructions for automated setup"
     export GITHUB_PAT="your-github-API"
     git push https://${GITHUB_PAT}@github.com/TestwayWeb3/testwayweb3-bots.git main
     unset GITHUB_PAT
     ```

#### Additional Notes
- **Script Improvements:** The updated `install.sh` script:
  - Allows running as a non-root user with sudo privileges.
  - Uses the correct Python dependencies (`python-telegram-bot==20.0`, `notion-client`, `python-dotenv`).
  - Includes a testing step to verify the bot works before starting with PM2.
  - Removes unnecessary firewall configuration.
  - Improves user experience with colored output and clear prompts.
  - Configures PM2 to start on boot.
- **README Update:** The README now includes a dedicated section for using the `install.sh` script, making it easy for the user to choose between automated and manual installation.
- **Future Use:** When your current VPS expires, you can use the `install.sh` script on a new VPS by following the "Option 1: Automated Installation Using `install.sh`" section in the README. Ensure you have backed up your `.env` file to provide the necessary credentials during setup.

---

### Survey Note: Detailed Analysis and Implementation

This section provides a comprehensive analysis of the `install.sh` script and the README update, based on the user's request.

#### Background and Context
The user provided their existing `install.sh` script for automating the Web3ActivityBot installation and requested a review and update, along with instructions in the README for running the script on a new VPS. The script was analyzed, improved, and aligned with the latest setup requirements, and the README was updated to include a section for automated installation.

#### Analysis of the `install.sh` Script
1. **Existing Script:**
   - The script automates system updates, software installation, repository cloning, virtual environment setup, dependency installation, `.env` configuration, firewall setup, and PM2 configuration.
   - It requires root privileges, includes unnecessary dependencies (`requests`), lacks a testing step, and has room for improved user experience.

2. **User's Needs:**
   - The user wants an optimized script that automates the installation process and clear instructions in the README for running the script on a new VPS.

#### Implementation Details
- **Script Update:** The `install.sh` script was updated to:
  - Allow running as a non-root user with sudo privileges.
  - Use the correct Python dependencies.
  - Add a testing step to verify the bot works.
  - Remove unnecessary firewall configuration.
  - Improve user experience with colored output and clear prompts.
  - Configure PM2 to start on boot.
- **README Update:** A new section was added to the README for automated installation using `install.sh`, providing clear steps to run the script and verify the bot.

#### Tables for Clarity
Below is a table summarizing the changes made to the `install.sh` script:

| Aspect                 | Previous Version                          | Updated Version                          |
|------------------------|-------------------------------------------|------------------------------------------|
| Root User Requirement  | Required root (`sudo`)                   | Runs as non-root with sudo privileges   |
| Python Dependencies    | Included `requests`                      | Only `python-telegram-bot==20.0`, `notion-client`, `python-dotenv` |
| Testing Step           | Not included                             | Added to verify bot functionality       |
| Firewall (UFW)         | Enabled with ports 22, 80, 443           | Removed (only port 22 needed)           |
| User Experience        | Basic output                             | Colored output, clear prompts           |
| PM2 Startup            | Generated command but not executed       | Executes `pm2 startup` command          |

#### Unexpected Detail
An unexpected detail is that the original script included UFW configuration for ports 80 and 443, which are not needed for the bot. This was removed to simplify the setup, as the bot only requires SSH access (port 22).

#### Conclusion
The `install.sh` script was updated to align with the latest setup requirements, improving usability, dependency management, and error handling. The README was updated with a dedicated section for automated installation, ensuring the user can easily set up the bot on a new VPS in the future.

---

### Key Citations
- [Notion Database Page](https://www.notion.so/1c2fd260347b80bbb49cec16e02d2132?v=1c2fd260347b80e5836f000c068d5f77)
