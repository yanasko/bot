import telebot
from config import keys, TOKEN
from extensoins import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helpme(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты, цену которой вы хотите узнать> \
            <имя валюты, в которой надо узнать цену первой валюты> \
            <количество переводимой валюты>\nУвидеть список всех доступных валют: /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def get_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n' .join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler()
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise ConvertionException('Неверное число параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        total_price = float(amount) * total_base
        t_price = round(total_price, 2)
        text = f'Цена {amount} {quote} в {base} - {t_price}'
        bot.send_message(message.chat.id, text)


bot.polling()
