from pyrogram import Client, filters, idle
from pyrogram.types import Message, CallbackQuery
from config import Config
from database import Database
from keyboards import Keyboards
from utils import extract_channel_id, is_valid_bot_token
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot
try:
    app = Client(
        "file_store_bot",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN
    )
    db = Database()
except Exception as e:
    logger.error(f"Failed to initialize bot: {str(e)}")
    raise

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    try:
        await db.add_user(message.from_user.id, message.from_user.username)
        await message.reply_text(Config.START_TEXT, reply_markup=Keyboards.main_keyboard)
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}")
        await message.reply_text("An error occurred. Please try again later.")

@app.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    try:
        if callback_query.data == "help":
            await callback_query.message.edit_text(Config.HELP_TEXT, reply_markup=Keyboards.back_button)
        elif callback_query.data == "about":
            await callback_query.message.edit_text(Config.ABOUT_TEXT, reply_markup=Keyboards.back_button)
        elif callback_query.data == "clone":
            await callback_query.message.edit_text(
                "✨ Manage Clone's\n\nYou can now manage and create your very own identical clone bot, "
                "mirroring all my awesome features, using the given buttons.",
                reply_markup=Keyboards.clone_keyboard
            )
        elif callback_query.data == "add_clone":
            await callback_query.message.edit_text(
                "1) Create a bot using @BotFather\n"
                "2) Then you will get a message with bot token\n"
                "3) Send that bot token to me",
                reply_markup=Keyboards.back_button
            )
        elif callback_query.data == "back":
            await callback_query.message.edit_text(Config.START_TEXT, reply_markup=Keyboards.main_keyboard)
    except Exception as e:
        logger.error(f"Error in callback handler: {str(e)}")
        await callback_query.answer("An error occurred. Please try again.")

@app.on_message(filters.command("genlink") & filters.reply)
async def generate_link(client: Client, message: Message):
    try:
        reply = message.reply_to_message
        if not reply:
            await message.reply_text("Please reply to a file to generate a link.")
            return

        forwarded = await reply.forward(Config.DATABASE_CHANNEL)
        file_id = forwarded.id
        bot_username = (await client.get_me()).username
        link = f"https://t.me/{bot_username}?start=file_{file_id}"
        
        await db.add_file(file_id, message.from_user.id, message.date)
        await message.reply_text(f"Here's your file link:\n{link}")
    except Exception as e:
        logger.error(f"Error in generate_link: {str(e)}")
        await message.reply_text("Failed to generate link. Please try again later.")

@app.on_message(filters.command("batch"))
async def batch_command(client: Client, message: Message):
    try:
        command_parts = message.text.split()
        if len(command_parts) != 3:
            await message.reply_text(
                "Please provide the first and last message links.\n"
                "Format: /batch first_link last_link"
            )
            return

        first_link = command_parts[1]
        last_link = command_parts[2]
        
        channel_id = extract_channel_id(first_link)
        if channel_id:
            try:
                chat_member = await client.get_chat_member(channel_id, "me")
                if chat_member.status not in ["administrator", "creator"]:
                    await message.reply_text("I am not admin in this channel!")
                    return
            except Exception:
                await message.reply_text("I am not admin in this channel!")
                return

        first_msg_id = int(first_link.split('/')[-1])
        last_msg_id = int(last_link.split('/')[-1])
        
        status_msg = await message.reply_text("Processing batch...")
        processed = 0
        
        for msg_id in range(first_msg_id, last_msg_id + 1):
            try:
                msg = await client.get_messages(channel_id, msg_id)
                if msg and not msg.empty:
                    forwarded = await msg.forward(Config.DATABASE_CHANNEL)
                    await db.add_file(forwarded.id, message.from_user.id, message.date)
                    processed += 1
                    
                    if processed % 10 == 0:
                        await status_msg.edit_text(f"Processed {processed} messages...")
            except Exception as e:
                logger.warning(f"Error processing message {msg_id}: {str(e)}")
                continue
        
        bot_username = (await client.get_me()).username
        batch_link = f"https://t.me/{bot_username}?start=batch_{first_msg_id}_{last_msg_id}"
        await status_msg.edit_text(f"Batch processing complete!\nProcessed {processed} messages.\nBatch link: {batch_link}")
        
    except Exception as e:
        logger.error(f"Error in batch command: {str(e)}")
        await message.reply_text("Failed to process batch. Please try again later.")

@app.on_message(filters.regex(r'^[\d\w\-_]{20,}:[\w\-]{35,}$'))
async def handle_bot_token(client: Client, message: Message):
    try:
        if not message.text:
            return
        
        token = message.text.strip()
        if not is_valid_bot_token(token):
            await message.reply_text("Invalid bot token format. Please send a valid bot token.")
            return
        
        await db.add_clone(
            message.from_user.id,
            message.from_user.username,
            token,
            message.date
        )
        
        await message.reply_text(
            "✅ YOUR BOT IS SUCCESSFULLY CLONED\n"
            "YOU CAN START USING THE BOT AFTER 24 HOURS"
        )
        
    except Exception as e:
        logger.error(f"Error in handle_bot_token: {str(e)}")
        await message.reply_text("Failed to create clone. Please try again later.")

async def main():
    try:
        await app.start()
        logger.info("Bot started successfully!")
        await idle()
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())