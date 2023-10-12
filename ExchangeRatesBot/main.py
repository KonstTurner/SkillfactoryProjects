import telebot
from extensions import APIException, Convertor
from config import TOKEN, currency
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ["start", "help"])
def help(message: telebot.types.Message):
    text = "Данный бот возвращает цену на определённое количество валюты (евро, доллар или рубль).\
    Чтобы начать работу, нужно отправить сообщение боту в виде:\
    <имя валюты, цену которой нужно узнать>  <имя валюты, в которой надо узнать цену первой валюты>  <количество первой валюты>. \
    Увидеть список всех доступных валют: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands = ["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in currency.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)

bot.polling(none_stop = True)