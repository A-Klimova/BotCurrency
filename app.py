import telebot
from extensions import API, APIException
from T_K import TOKEN

bot = telebot.TeleBot(TOKEN)


# Приветствие пользователя при команде /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Добро пожаловать, {message.chat.first_name} {message.chat.last_name} !')


# Дает инструкции при команде /help
@bot.message_handler(commands=['help'])
def help(message):
    text = 'Чтобы начать работу введите команду боту в следующим формате:\n <Имя валюты> <В какую валюту перевести> <Количество валюты>.\n Вы можете увидить список доступных валют с помощью команды /values'
    bot.reply_to(message, text)


# Список доступных валют при команде /values
@bot.message_handler(commands=['values'])
def values(message):
    api = API()
    text = api.get_values()
    bot.reply_to(message, text)


# Обработка запроса пользователя
@bot.message_handler(content_types=['text', ])
def convert(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Слишком много параметров!')
        quote, base, amount = values
        total_base = API.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n {e}')
    except Exception as e:
        bot.send_message(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {float(total_base) * float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)