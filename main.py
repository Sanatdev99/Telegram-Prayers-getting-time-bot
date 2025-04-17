from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
import requests

TOKEN = '7803966336:AAG2TgozlGsG1ZYca9dDaccjaFgEv7ljoTw'  # Replace with your actual bot token
bot = TeleBot(TOKEN)


# Function to generate a simple keyboard
def generate_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("⚡ Namoz Vaqtlari | Prayer Times"))
    markup.add(KeyboardButton("🌟 Ramazon Kalendari | Ramadan Calendar"))
    return markup


@bot.message_handler(commands=['start'])
def command_start(message: Message):
    chat_id = message.chat.id
    full_name = message.chat.first_name
    bot.send_message(chat_id,
                     f'Salom {full_name}! \U0001F31F\nBu bot sizga namoz vaqtlarini va Ramazon kalendarini taqdim etadi!\nPlease select an option:',
                     reply_markup=generate_keyboard())


@bot.message_handler(regexp='.*Namoz Vaqtlari.*|.*Prayer Times.*')
def ask_city(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Shahar nomini kiriting | Enter city name:')
    bot.register_next_step_handler(msg, answer_to_user)


def answer_to_user(message: Message):
    chat_id = message.chat.id
    city = message.text

    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {"city": city, "country": "Uzbekistan", "method": 2, "lang": "eng"}
    response = requests.get(url, params=params).json()
    timings = response.get("data", {}).get("timings", {})

    prayer_times = (
        f"\U0001F319 *Namoz Vaqtlari ({city}) | Prayer Times* \U0001F319\n\n"
        f"Fajr | Bomdod: {timings.get('Fajr', 'N/A')}\n"
        f"Dhuhr | Peshin: {timings.get('Dhuhr', 'N/A')}\n"
        f"Asr | Asr: {timings.get('Asr', 'N/A')}\n"
        f"Maghrib | Shom: {timings.get('Maghrib', 'N/A')}\n"
        f"Isha | Xufton: {timings.get('Isha', 'N/A')}\n"
    )
    bot.send_message(chat_id, prayer_times, parse_mode="Markdown")



@bot.message_handler(regexp='.*Ramazon Kalendari.*|.*Ramadan Calendar.*')
def send_ramadan_calendar(message: Message):
    chat_id = message.chat.id
    with open("ramadan_calendar.jpg", "rb") as photo:
        bot.send_photo(chat_id, photo, caption="\U0001F31F Ramazon Kalendari | Ramadan Calendar \U0001F31F")

bot.polling(none_stop=True)
