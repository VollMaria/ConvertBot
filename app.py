import telebot
from config import keys, TOKEN
from extensions import APIException, Exchanger

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для начала работы введите данные в следующем формате: \n<валюта, которую хотите конвертировать> \
\n<валюта, в которой хотите конвертировать> \n<количество первой валюты> \nНапример: доллар рубль 1\
\n\nПосмотреть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список доступных валют:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        base, quote, amount = values
        total_base = Exchanger.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка со стороны пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Стоимость {amount} {base} в {quote}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()