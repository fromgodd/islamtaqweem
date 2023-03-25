import json
import datetime
import calendar
import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from globals import BOT_TOKEN
from dua import SUHUR_DUA_CLOSE_FAST, IFTAR_DUA_BREAKING_FAST

# Load Taqweem data from JSON file
with open("taqweem.json") as f:
    taqweem_data = json.load(f)

# Initialize bot and dispatcher instances
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Handler function for the /start command
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    # Create the inline keyboard with two buttons
    markup = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("🗓🍚 View Taqweem", callback_data="view_taqweem"),
        InlineKeyboardButton("📖🤲 View duas", callback_data="view_duas")
    )
    # Send a welcome message with the inline keyboard
    await message.reply("👋 Welcome to Ramadan Companion Bot! Type /start to start bot!. This bot is used to create powerful Muslim's environment, check Iftar time and main goal of bot is simplifying everything. Author/Creator - @fromgodd", reply_markup=markup)

# Handler function for the "View Taqweem" button
@dp.callback_query_handler(lambda query: query.data == "view_taqweem")
async def view_taqweem(callback_query: types.CallbackQuery):
    # Get current date in the format used in the Taqweem data
    now = datetime.datetime.now()
    today_str = now.strftime("%d-%m-%Y")

    # Find the Taqweem data for today's date
    for key, data in taqweem_data.items():
        if data["date"] == today_str:
            today_data = data
            break
    else:
        today_data = None

    # Check if Taqweem data exists for today's date
    if today_data is None:
        await callback_query.answer("😢 Sorry, Taqweem data for today is not available.")
        return

    # Format the Taqweem data message
    month_name = calendar.month_name[int(today_data["date"][3:5])]
    taqweem_message = f"⚡️Taqweem data for today (Tashkent):\n\n🗓 {today_data['date']} ({month_name})\n⏰ Iftar: {today_data['iftar']}\n🔃 Suhur: {today_data['suhur']}"

    # Send the Taqweem data for today's date as a message
    await bot.send_message(callback_query.from_user.id, taqweem_message)

# Handler function for the "View duas" button
@dp.callback_query_handler(lambda query: query.data == "view_duas")
async def view_duas(callback_query: types.CallbackQuery):
    # Format the duas message with line breaks
    duas_message = f"<b>🤲 Suhur dua:</b>\n{SUHUR_DUA_CLOSE_FAST}\n\n<b>🤲 Iftar dua:</b>\n{IFTAR_DUA_BREAKING_FAST}\n\n\n💰 <b>Support author:</b> 8600 1402 7455 4485 (Uzcard)"
    # Send the duas message as a message with HTML parse mode
    await bot.send_message(callback_query.from_user.id, duas_message, parse_mode=types.ParseMode.HTML)

# Start the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
