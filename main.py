import telebot
import json

# Замените на свой токен от BotFather
TOKEN = "7615599383:AAGfPUfPBe-FCSfNl0vMvB77DVX0J-uPC3Y"

bot = telebot.TeleBot(TOKEN)

# Загружаем данные о виртуальных турах из JSON-файла
with open('tours.json', 'r', encoding='utf-8') as f:
    tours = json.load(f)

# Функция для обработки команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет! Я бот для виртуальных путешествий. Выбери тур из списка: /tours")

# Функция для обработки команды /tours
@bot.message_handler(commands=['tours'])
def tours_handler(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for tour in tours:
        keyboard.add(telebot.types.InlineKeyboardButton(text=tour['name'], callback_data=tour['id']))
    bot.send_message(message.chat.id, "Доступные туры:", reply_markup=keyboard)

# Функция для обработки callback-запросов (нажатий на кнопки)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    tour_id = call.data
    tour = next((tour for tour in tours if tour['id'] == tour_id), None)
    if tour:
        message_text = f"<b>{tour['name']}</b>\n\n{tour['description']}\n\n<a href='{tour['link']}'>Посмотреть тур</a>"
        bot.send_message(call.message.chat.id, message_text, parse_mode='HTML')
    else:
        bot.send_message(call.message.chat.id, "Тур не найден.")

# Запускаем бота
bot.polling(none_stop=True)
