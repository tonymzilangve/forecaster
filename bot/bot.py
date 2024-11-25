import telebot
import requests
import os
from telebot.types import Message
from dotenv import load_dotenv


load_dotenv()

bot = telebot.TeleBot(token=os.getenv('BOT_TOKEN'))


def extract_arg(arg):
    return arg.split()[1:]


@bot.message_handler(commands=['weather'])
def start(message: Message):
    city = extract_arg(message.text)
    bot.reply_to(message=message, text=city)
    
    url = f"http://127.0.0.1:8000/api/v2/weather/{city[0]}"
    response = requests.get(url, params={"source_type": "telegram"})
    
    weather = response.json()[city[0]]
    answer = (
        f'Погода в городе {city[0].capitalize()}:\n'
        f'Температура: {weather["temperature"]}\n'
        f'Давление: {weather["pressure"]}\n'
        f'Скорость ветра: {weather["wind_speed"]}\n'
        f'Источник запроса: {weather["source_type"]}\n'
    )
    
    bot.send_message(chat_id=message.chat.id, text=answer)


bot.polling()
