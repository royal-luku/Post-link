import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# Constants
REQST_CHANNEL = 'YOUR_REQUEST_CHANNEL_ID'

# Function to handle the /request command
@client.on_message(filters.command("request"))
async def request_movie(client, message):
    if len(message.command) == 1:
        await message.reply_text(
            "**Please provide a movie name, release year, and language after the /request command.\n\nExample Usage: `/request Pushpa 2 (2024) Hindi`\n\n**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⚠️ Watch Tutorial Video", url="https://youtube.com/shorts/WFJh08EoPsk")]]
            )
        )
        return

    movie_info = message.text.split(maxsplit=1)[1]

    # Regular expression to parse the movie name, year, and language
    match = re.match(r'^(.*?)(\d{4})\s+([A-Za-z]+)$', movie_info)

    if not match:
        if not re.search(r'\d{4}', movie_info):
            await message.reply_text("**Release year not found. Please provide the movie name along with the release year and language.**")
        elif not re.search(r'\s+[A-Za-z]+$', movie_info):
            await message.reply_text("**Language not found. Please provide the movie name along with the release year and language.**")
        return

    movie_name, release_year, language = match.groups()

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✅ Movie Now Available", callback_data=f"available_{message.from_user.id}")],
            [InlineKeyboardButton("❌ Movie Not Released", callback_data=f"not_released_{message.from_user.id}")],
            [InlineKeyboardButton("🚫 Movie Not Available", callback_data=f"not_available_{message.from_user.id}")]
        ]
    )

    try:
        await client.send_message(
            REQST_CHANNEL,
            f"**#New_Movie_Request\n\nRequested Movie:** `{movie_name.strip()} ({release_year}) {language}`\n"
            f"**Requested by:** {message.from_user.mention}\n**User ID:** `{message.from_user.id}`",
            reply_markup=buttons
        )

        await client.send_message(
            message.chat.id,
            "**🍿 Movie request received!\n\n⏰ __Please allow around 2-6 hours for it to be added to the database. "
            "I'll notify you once it's added.__\nThanks!**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⤪ Close ⤨", callback_data="close_data")]])
        )
    except Exception as e:
        await message.reply_text(f"**An error occurred while processing your request: {e}**")

# Callback handler for the "Movie Now Available" button
@client.on_callback_query(filters.regex(r"^available_\d+"))
async def movie_available(client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    await client.send_message(
        user_id,
        "🎉 Your requested movie is now available! You can find it in our database: [Movie Database](https://t.me/swifthornrequest)"
    )
    await callback_query.answer("Notification sent to the user about the movie availability.", show_alert=True)

# Callback handler for the "Movie Not Released" button
@client.on_callback_query(filters.regex(r"^not_released_\d+"))
async def movie_not_released(client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    await client.send_message(
        user_id,
        "🚫 The movie you requested has not been released yet. We will notify you once it is available."
    )
    await callback_query.answer("Notification sent to the user about the movie not being released.", show_alert=True)

# Callback handler for the "Movie Not Available" button
@client.on_callback_query(filters.regex(r"^not_available_\d+"))
async def movie_not_available(client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    await client.send_message(
        user_id,
        "❌ The movie you requested is not available. If it becomes available in the future, we will add it to our database and notify you."
    )
    await callback_query.answer("Notification sent to the user about the movie not being available.", show_alert=True)

# Callback handler for closing messages
@client.on_callback_query(filters.regex(r"^close_data"))
async def close_message(client, callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer()
