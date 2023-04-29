#!/usr/bin/env python

# import mysql.connector
import secrets
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
import logging

# mydb = mysql.connector.connect(
#   host=secrets.MYSQL_ADDR,
#   user=secrets.MYSQL_USER,
#   password=secrets.MYSQL_PASS
# )

# Включаем логгирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

main_keyboard = [
  [InlineKeyboardButton("📅Мероприятия", callback_data="1")],
  [InlineKeyboardButton("🗿Стажировки", callback_data="2")],
  [InlineKeyboardButton("💯Вакансии", callback_data="3")],
]

back_keyboard = [
  [InlineKeyboardButton("Назад", callback_data="0")]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Отправляет сообщение старта."""
  reply_markup = InlineKeyboardMarkup(main_keyboard)
  await update.message.reply_text("Приветствуем тебя в боте Центра Карьеры! Выбери нужную тебе категорию:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Parses the CallbackQuery and updates the message text."""
  query = update.callback_query
  await query.answer()
  if query.data == "0":
    reply_markup = InlineKeyboardMarkup(main_keyboard)
    await query.edit_message_text("Приветствуем тебя в боте Центра Карьеры! Выбери нужную тебе категорию:", reply_markup=reply_markup)
  elif query.data == "1":
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    await query.edit_message_text("Предстоящие мероприятия:\n\n🔹Пока что предстоящих мероприятий нет.", reply_markup=reply_markup)
  elif query.data == "2":
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    await query.edit_message_text("Доступные стажировки:\n\n🔹Пока что стажировок нет.", reply_markup=reply_markup)
  elif query.data == "3":
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    await query.edit_message_text("Открытые вакансии:\n\n🔹Пока что открытых вакансий нет.", reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Displays info on how to use the bot."""
  await update.message.reply_text("Используйте /start для запуска бота.")


def main() -> None:
  """Запускает бота."""
  application = Application.builder().token(secrets.TELEGRAM_TOKEN).build()
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button))
  application.add_handler(CommandHandler("help", help_command))
  print('Бот запущен.')
  application.run_polling()


if __name__ == '__main__':
  main()
