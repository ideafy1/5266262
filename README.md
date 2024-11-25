# Telegram File Store Bot

A powerful Telegram bot for storing and sharing files with features like:
- File storage and link generation
- Batch file processing
- Bot cloning capability
- Admin controls
- And more!

## Setup
1. Create a `.env` file with your credentials
2. Install dependencies: `pip install -r requirements.txt`
3. Run the bot: `python bot.py`

## Environment Variables
- `BOT_TOKEN`: Your Telegram bot token
- `API_ID`: Telegram API ID
- `API_HASH`: Telegram API Hash
- `ADMIN_ID`: Admin user IDs (space-separated)
- `MONGODB_URI`: MongoDB connection URI
- `DB_NAME`: MongoDB database name
- `DATABASE_CHANNEL`: Channel ID for storing files

## Features
- Store files and generate shareable links
- Batch process multiple files
- Clone bot functionality
- Admin commands for broadcast and user management
- Customizable settings