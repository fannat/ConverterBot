import telebot
from extensions import APIException, Converter
from Config import TOKEN, val


bot = telebot.TeleBot(TOKEN)

keys = val.keys()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать в бот конвертер валют.")
    bot.send_message(message.chat.id, "Нажмите /help, чтобы ознакомиться с инструкциями")
    bot.send_message(message.chat.id, "Нажмите /values, чтобы ознакомиться сo списком доступных валют")


@bot.message_handler(commands=['help'])
def send_help(message):
    text = """Для конвертации необходимо отправить сообщение боту в виде:\n
Название валюты,цену которой хотите узнать\n
Название валюты, в которой надо узнать цену первой валюты\n
Количество первой валюты\n 
Например:  доллар евро 25, евро рубль 150  """
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def currencies_info(message):
    curr_info = "На данный момент поддерживаются:"
    for key in val.keys():
        curr_info = '\n'.join((curr_info, key))
    bot.reply_to(message, curr_info)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        base, quote, amount = values
        if len(values) != 3:
            raise APIException('Слишком много параметров,пожалуйста следуйте инструкций')
        if base not in keys or quote not in keys:
            raise APIException('Данная валюта пока не поддерживается.Нажмите /values чтобы увидеть доступные валюты')
        rate = Converter.get_price(quote, base, amount)
    except APIException as error:
        bot.reply_to(message, f'Ошибка пользователя:\n{error}')
    except Exception as error:
        bot.reply_to(message, f'Не удалось обработать команду\n{error}')
    else:
        text = f'Цена {amount} {quote} равна {rate} {base} '
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)




