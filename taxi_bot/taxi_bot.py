from telegram import Update, InputFile, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime
import tempfile
import os
from dotenv import load_dotenv

# ========= Загрузка токена из .env ==========
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Не найден токен бота. Добавьте BOT_TOKEN в файл .env")

# ========= Состояния пользователей ==========
user_state = {}   # состояние пользователя
user_data = {}    # храним пробег


# ========= 1. Команда /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_state[user_id] = "wait_mileage"
    await update.message.reply_text(
        "Привет! Я бот для создания электронного путевого листа.\n"
        "Отправь мне пробег в километрах или начальный и конечный километраж через пробел."
    )


# ========= 2. Общий обработчик сообщений ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    state = user_state.get(user_id)
    text = update.message.text.replace(",", ".").strip()

    if state == "wait_mileage":
        parts = text.split()
        try:
            if len(parts) == 1:
                mileage = float(parts[0])
            elif len(parts) == 2:
                start = float(parts[0])
                end = float(parts[1])
                if end < start:
                    await update.message.reply_text(
                        "Конечный километраж не может быть меньше начального. Введите заново."
                    )
                    return
                mileage = end - start
            else:
                await update.message.reply_text(
                    "Введите одно число или два числа через пробел, например: 123 или 10500 10520"
                )
                return
        except ValueError:
            await update.message.reply_text(
                "Введите числа корректно, например: 123 или 10500 10520"
            )
            return

        user_data[user_id] = mileage
        user_state[user_id] = "wait_format"

        keyboard = ReplyKeyboardMarkup(
            [["PDF", "TXT"]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
        await update.message.reply_text(
            f"Пробег составил: {mileage} км\nВ каком формате сделать путевой лист?",
            reply_markup=keyboard
        )
        return

    elif state == "wait_format":
        fmt = text.upper()
        if fmt not in ["PDF", "TXT"]:
            await update.message.reply_text("Выберите формат: PDF или TXT")
            return

        mileage = user_data.get(user_id)
        if fmt == "PDF":
            file_path = create_pdf_temp(mileage)
            filename = "putevoy_list.pdf"
        else:
            file_path = create_txt_temp(mileage)
            filename = "putevoy_list.txt"

        # Отправка файла в Telegram в бинарном режиме
        with open(file_path, "rb") as f:
            await update.message.reply_document(InputFile(f, filename=filename))

        # Удаляем временный файл
        os.remove(file_path)

        # Сбрасываем состояние
        user_state.pop(user_id, None)
        user_data.pop(user_id, None)


# ========= Создание PDF через временный файл ==========
def create_pdf_temp(mileage):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.close()  # закрываем, чтобы ReportLab мог писать

    c = canvas.Canvas(tmp.name, pagesize=A4)
    c.setFont("Helvetica", 14)
    c.drawString(50, 800, "ПУТЕВОЙ ЛИСТ")
    c.drawString(50, 770, f"Дата: {datetime.date.today()}")
    c.drawString(50, 740, f"Пробег: {mileage} км")
    c.save()

    return tmp.name


# ========= Создание TXT через временный файл ==========
def create_txt_temp(mileage):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
    tmp.write("Путевой лист\n")
    tmp.write(f"Дата: {datetime.date.today()}\n")
    tmp.write(f"Пробег: {mileage} км\n")
    tmp.close()
    return tmp.name


# ========= MAIN ==========
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
