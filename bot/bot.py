import telebot
import requests
import os
from telebot.types import Message
from telebot import types
from dotenv import load_dotenv


load_dotenv()

bot = telebot.TeleBot(token=os.getenv('BOT_TOKEN'))


@bot.callback_query_handler(func=lambda call: True) 
def forecaster(call):
    city = call.data
    url = f"http://api:8000/api/v2/weather/{city}"
    response = requests.get(url, params={"source_type": "telegram"})

    weather = response.json()[city]
    answer = (
        f'Погода в городе {city.capitalize()}:\n'
        f'Температура: {weather["temperature"]}\n'
        f'Давление: {weather["pressure"]}\n'
        f'Скорость ветра: {weather["wind_speed"]}\n'
        f'Источник запроса: {weather["source_type"]}\n'
    )
    
    bot.send_message(call.from_user.id, text=answer)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text='Введите ваш город: ')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_all(message):
    markup = types.InlineKeyboardMarkup()
    item = types.InlineKeyboardButton('Узнать погоду', callback_data=message.text)
    markup.add(item)
    bot.send_message(message.chat.id, f"{message.text}".capitalize(), reply_markup=markup)


bot.polling(none_stop=True)
