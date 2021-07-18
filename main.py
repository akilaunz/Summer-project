import urllib.request
import six
import requests
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import Image
import telebot


bot = telebot.TeleBot('1909610752:AAHnlqIlmQZmiHlge2GFLxiOJHVjXjYSxE8')

genre = ''
ttype = ''
country = ''
channel = ''


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id,
                        "Здравствуйте! Введите, пожалуйста,
                        страну сериала с большой буквы")
        bot.register_next_step_handler(message, get_country)


def get_country(message):
    global country
    country = message.text
    bot.send_message(message.from_user.id,
                     "Введите, пожалуйста, 
                        жанр сериала с маленькой буквы")
    bot.register_next_step_handler(message, get_genre)


def get_genre(message):
    global genre
    genre = message.text
    bot.send_message(message.from_user.id,
                     "Введите, пожалуйста, что именно вы 
                          хотите смотреть. Аниме? Дорама? Фильм? Шоу?")
    bot.register_next_step_handler(message, get_type)


def get_type(message):
    global ttype
    ttype = message.text
    bot.send_message(message.from_user.id,
                     "Введите, пожалуйста, производство
                           какого канала вы бы хотели посмореть?")
    bot.register_next_step_handler(message, get_channel)


def get_channel(message):
    global channel
    channel = message.text
    scrapping()
    i = 0
    for name in names:
        bot.send_message(message.from_user.id,
                       f'{name}, {ratings[i]}\n')
        bot.send_message(message.from_user.id,
                       f'{urls[i]}\n')
        i = i + 1

def scrapping():
    genre_num = tv_genres_code_to_name[f'{genre}']
    channel_num = tv_channels_code_to_name[f'{channel}']
    type_num = tv_types_code_to_name[f'{ttype}']
    country_num = tv_countries_code_to_name[f'{country}']

    url = f'https://softbox.tv/f/cat={genre_num},{country_num},{type_num},
                                     {channel_num}/sort=date/order=asc/'
    response = requests.get(url)
    soup_str = BeautifulSoup(response.content, 'html.parser')

    needed_things_block = soup_str.find_all('article', 'moviebox col-6
                             col-sm-6 col-md-4 col-lg-4 col-xl-4 mb-3')
    names = []
    urls = []
    ratings = []
    for thing in needed_things_block:
        names.append(thing.find('div', 'original-title u-txtcolor-gray
                    u-txt-ellipsis u-small').text)
        urls.append(thing.find('a', 'd-flex flex-column flex-column-reverse
                    an')['href'])
        ratings.append(thing.find_all('span', 'u-small')[1].text)


bot.polling(none_stop=True, interval=0)
