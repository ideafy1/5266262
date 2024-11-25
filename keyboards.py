from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Keyboards:
    main_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ Help", callback_data="help")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("🤖 Create My Own Clone", callback_data="clone")],
        [InlineKeyboardButton("📢 Update Channel", url="https://t.me/Crazy")]
    ])

    back_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])

    clone_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Clone", callback_data="add_clone")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])