import telebot
from logic import detect_dima

# Замени 'TOKEN' на токен твоего бота
bot = telebot.TeleBot("")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь фото и я скажу Дима это или нет")

@bot.message_handler(content_types=['photo'])
def photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    model = "keras_model.h5"
    labels = "labels.txt"
    result,conf = detect_dima(file_name, model, labels)
    print(list(result))
    if result == "Class 1\n":
        result = "Это Дима"
    else:
        result = "Это не Дима"
    bot.reply_to(message, f"{result}, уверенность:{conf}")
    


# Запускаем бота
bot.polling()