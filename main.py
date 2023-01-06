import telebot
from mytoken import keys, TOKEN
from extensions import ConvertionException, Currency

bot = telebot.TeleBot(TOKEN)
# Обрабатываются все сообщения, содержащие команды '/start' или '/help'
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: ' \
            '\n<имя валюты цену которой хотите узнать>' \
            '\n<имя валюты в которой надо узнать цену первой валюты> '\
            '\n<количество первой валюты>'\
            '\n\n Увидеть список доступных валют: /values'
    bot.reply_to(message, text)

# выводиться информация о всех доступных валютах при вводе команды /values
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: \n'
    text = text + '\n'.join(keys.keys())
    bot.reply_to(message, text)

# конвертация валюты
@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров')

        base, quote, amount = values
        amount = float(amount)
        total_base = Currency.get_price(base, quote, amount)
        total_base = total_base * amount #умножаем на введеное количество курс валюты

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя - {e}')

    except Exception as r:
        bot.reply_to(message, f'не удалось обработать команду {r}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)