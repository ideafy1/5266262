import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

def get_env_or_default(key: str, default: str = None, required: bool = True) -> str:
    value = os.getenv(key, default)
    if required and value is None:
        raise ValueError(f"Environment variable {key} is required but not set")
    return value

def parse_admin_ids(admin_ids_str: str) -> List[int]:
    if not admin_ids_str:
        return []
    return [int(id_str) for id_str in admin_ids_str.split() if id_str.strip()]

class Config:
    try:
        BOT_TOKEN = get_env_or_default("BOT_TOKEN")
        API_ID = int(get_env_or_default("API_ID", "14656169"))  # Using provided default
        API_HASH = get_env_or_default("API_HASH", "a2d5b45af5a62c674591e4eeeddc96d9")  # Using provided default
        ADMIN_IDS = parse_admin_ids(get_env_or_default("ADMIN_ID", "709142820 6133992240"))  # Using provided defaults
        MONGODB_URI = get_env_or_default("MONGODB_URI", "mongodb+srv://adityasinghcompany:Achiadi123@cluster0.8zvpl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        DB_NAME = get_env_or_default("DB_NAME", "Cluster0")
        DATABASE_CHANNEL = int(get_env_or_default("DATABASE_CHANNEL", "-1002475078480"))
    except ValueError as e:
        print(f"Configuration Error: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error in configuration: {str(e)}")
        raise

    # Constants
    START_TEXT = """🚀 Build Your Own File Store Bot with @juststoreitbot

No coding needed! Get a powerful, feature-packed bot to store, share, and manage your files with ease. From custom access controls and batch uploads to real-time stats and 24/7 availability—this bot has it all.

Need more? You can even request additional features to make it truly your own!

👉 Click here to read the full list of features and get started!"""

    HELP_TEXT = """✨ Help Menu

I am a permanent file store bot. You can store files from your public channel without me being admin in there. If your channel or group is private, first make me admin in there. Then you can store your files using the commands below and access stored files using shareable links.

📚 Available Commands:
➛ /start - Check if I am alive.
➛ /genlink - To store a single message or file.
➛ /batch - To store multiple messages from a channel.
➛ /custom_batch - To store multiple random messages.
➛ /shortener - To shorten any shareable links.
➛ /settings - Customize your settings as needed.
➛ /broadcast - Broadcast messages to users (moderators only).
➛ /ban - Ban a user (moderators only).
➛ /unban - Unban a user (moderators only)."""

    ABOUT_TEXT = """✨ ᴀʙᴏᴜᴛ ᴍᴇ

✰ ᴍʏ ɴᴀᴍᴇ: ꜰɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ
✰ ᴍʏ ᴏᴡɴᴇʀ: Crazy Developer
✰ ᴜᴘᴅᴀᴛᴇs: Crazy
✰ sᴜᴘᴘᴏʀᴛ: Crazy
✰ ᴠᴇʀsɪᴏɴ: 0.7.9"""