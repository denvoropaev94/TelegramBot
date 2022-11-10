import telebot, wikipedia, re
from datetime import datetime

bot = telebot.TeleBot('5733840828:AAFDX6A3NwWlU5GD2p_4t5AEzdzPlQR3mUo')

value = ''
old_value = ''

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(   telebot.types.InlineKeyboardButton(' ', callback_data='no'),
                telebot.types.InlineKeyboardButton('C', callback_data='C'),
                telebot.types.InlineKeyboardButton('<=', callback_data='<='),
                telebot.types.InlineKeyboardButton('/', callback_data='/'))

keyboard.row(   telebot.types.InlineKeyboardButton('7', callback_data='7'),
                telebot.types.InlineKeyboardButton('8', callback_data='8'),
                telebot.types.InlineKeyboardButton('9', callback_data='9'),
                telebot.types.InlineKeyboardButton('*', callback_data='*'))

keyboard.row(   telebot.types.InlineKeyboardButton('4', callback_data='4'),
                telebot.types.InlineKeyboardButton('5', callback_data='5'),
                telebot.types.InlineKeyboardButton('6', callback_data='6'),
                telebot.types.InlineKeyboardButton('-', callback_data='-'))

keyboard.row(   telebot.types.InlineKeyboardButton('1', callback_data='1'),
                telebot.types.InlineKeyboardButton('2', callback_data='2'),
                telebot.types.InlineKeyboardButton('3', callback_data='3'),
                telebot.types.InlineKeyboardButton('+', callback_data='+'))

keyboard.row(   telebot.types.InlineKeyboardButton(' ', callback_data='no'),
                telebot.types.InlineKeyboardButton('0', callback_data='0'),
                telebot.types.InlineKeyboardButton(',', callback_data='.'),
                telebot.types.InlineKeyboardButton('=', callback_data='='))


@bot.message_handler(commands=['start'])  
def start_command(message):  
    bot.send_message(  
        message.chat.id,  
        'Hello! I can calculate something on a /calculater\n' +  
        'or I can find something on wikipedia /wiki\n'   
  )

@bot.message_handler(commands=['calculater'])
def getMessage(message):
    if value == '':
        bot.send_message(message.from_user.id, '0',reply_markup = keyboard)
    else:
         bot.send_message(message.from_user.id, value,reply_markup = keyboard)
    a_log = open(f'log_{message.chat.id}.txt', 'a')
    a_log.write(f'{message.from_user.first_name}: {datetime.now()}: {message.text}\n')
    a_log.close()


@bot.callback_query_handler(func=lambda call:True)
def callback_func(query):
    global value, old_value
    data = query.data

    if data == 'no':
        pass
    elif data == 'C':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value)-1]
    elif data == '=':
        try:
            value = str(eval(value))
        except:
            value = 'Ошибка!'
    else:
        value+=data

    if ( value != old_value and value != '') or ('0' != old_value and value == ''):
        if value == '':
            bot.edit_message_text(chat_id = query.message.chat.id, message_id=query.message.message_id,text='0',reply_markup=keyboard)
            old_value='0'
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,text=value,reply_markup=keyboard)
            old_value = value


# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")
# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


@bot.message_handler(commands=["wiki"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')
    a_log = open(f'log_{m.chat.id}.txt', 'a')
    a_log.write(f'{m.from_user.first_name}: {datetime.now()}: {m.text}\n')
    a_log.close()

@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, getwiki(message.text))
    a_log = open(f'log_{message.chat.id}.txt', 'a')
    a_log.write(f'{message.from_user.first_name}: {datetime.now()}: {message.text}\n')
    a_log.close()

print("server start")

bot.polling(non_stop = False, interval = 0)