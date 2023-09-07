import telebot
from config import TOKEN, keys
from extensions import ExchangeException, Exchange

bot = telebot.TeleBot(TOKEN)


# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    start = "Привет! Я бот, который может вернуть цену на определенное количество валюты.\n\n" \
                   "Пример использования: <имя валюты, цену которой вы хотите узнать> " \
                   "<имя валюты, в которой нужно узнать цену первой валюты> <количество первой валюты>\n\n" \
                   "Команды:\n" \
                   "/start - выводит инструкции по применению бота\n" \
                   "/help - выводит список команд бота\n" \
                   "/values - выводит информацию о всех доступных валютах\n\n" \
                   "Пример запроса: Рубль доллар 100"
    bot.reply_to(message, start)


# Обработка команды /help
@bot.message_handler(commands=['help'])
def help(message):
    help = "/start - выводит инструкции по применению бота\n" \
           "/help - выводит список команд бота\n" \
           "/values - выводит информацию о всех доступных валютах\n\n" \
           "Регистр значения не имеет.\n\n" \
           "Пример запроса: Рубль доллар 100"
    bot.reply_to(message,help)

# Обработка команды /values
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

# Обработка текстовых сообщений от пользователя
@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')  # преобразование в нижний регистр регистр

        if len(values) != 3:
            raise ExchangeException('Введите команду или 3 параметра')

        quote, base, amount = values
        total_base = Exchange.get_price(quote, base, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()