from flask import Flask, render_template, request
import telebot
import random

app = Flask(__name__)

# Замените 'YOUR_BOT_TOKEN' и 'YOUR_TELEGRAM_ID' на ваши реальные данные
BOT_TOKEN = '6650939517:AAEy21IfKOMRXu7e8uuh-GnxDodPs31KhZE'
TELEGRAM_ID = '603723021'

bot = telebot.TeleBot(BOT_TOKEN)

crossword_data = {
    "words": ["ЭНКОДЕР", "АЛГОРИТМ", "БАЛКА", "ШТИФТ", "ОСЬ", "ЧЕРВЯЧНАЯ", "ЗУБЧАТАЯ", "ПОВЫШАЮЩАЯ", "РАВНАЯ",
              "РЕМЕННАЯ"],
    "questions": [
        "Преобразователь перемещения в код",
        "Последовательность действий для решения задачи",
        "Несущая конструкция",
        "Крепежная деталь",
        "Линия, вокруг которой происходит вращение",
        "Тип передачи с червяком",
        "Тип передачи с зубьями",
        "Передача, увеличивающая момент",
        "Передача с одинаковыми шкивами",
        "Тип передачи с ремнем"
    ]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fio = request.form['fio']
        answers = [request.form.get(f'answer{i + 1}', '').upper() for i in
                   range(len(crossword_data["words"]))]

        # Проверка ответов (исправлено)
        correct_count = 0
        error_count = 0
        message = f"ФИО: {fio}\n"
        message += "\n"
        message += "Ответы по порядку:\n"
        for i, answer in enumerate(answers):
            # Сравниваем ответы в верхнем регистре:
            if answer == crossword_data["words"][i]:
                correct_count += 1
                message += f"{i + 1}. {answer.lower()}\n"
            elif answer:
                error_count += 1
                message += f"{i + 1}. {answer.lower()} ❌\n"
            else:
                message += f"{i + 1}. нет ответа\n"

        # Вывод количества правильных ответов ПОСЛЕ цикла:
        message += f"\nПравильно угаданных слов: {correct_count}\n"
        message += f"Количество Ошибок: {error_count}\n"

        bot.send_message(TELEGRAM_ID, message)
        return "Ответы отправлены!"

    colors = ["lightblue", "lightgreen", "lightcoral", "lightyellow", "lightcyan"]
    random.shuffle(colors)

    shuffled_words = crossword_data["words"].copy()
    random.shuffle(shuffled_words)

    return render_template('index.html',
                           crossword_data=crossword_data,
                           shuffled_words=shuffled_words,
                           colors=colors)

if __name__ == '__main__':
    app.run(debug=True)