#!/usr/bin/env python

# import mysql.connector
import secrets
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler
import logging

# mydb = mysql.connector.connect(
#   host=secrets.MYSQL_ADDR,
#   user=secrets.MYSQL_USER,
#   password=secrets.MYSQL_PASS,
#   database=secrets.MYSQL_DATABASE
# )

# Создаём необходимые таблицы в базе данных
# cur = mydb.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS events (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), text VARCHAR)")
# cur.execute("CREATE TABLE IF NOT EXISTS internships (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), text VARCHAR)")
# cur.execute("CREATE TABLE IF NOT EXISTS vacancies (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), text VARCHAR)")

# Включаем логгирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Клавиатуры:
main_keyboard = [
  [InlineKeyboardButton("📅 Мероприятия", callback_data="1")],
  [InlineKeyboardButton("🗿 Стажировки", callback_data="2")],
  [InlineKeyboardButton("💯 Вакансии", callback_data="3")],
]
admin_keyboard = [
  [InlineKeyboardButton("📅 Мероприятия", callback_data="1")],
  [InlineKeyboardButton("🗿 Стажировки", callback_data="2")],
  [InlineKeyboardButton("💯 Вакансии", callback_data="3")],
  [InlineKeyboardButton("🆕 Администрирование", callback_data="adm")]
]
admin_actions_keyboard = [
  [InlineKeyboardButton("📎 Добавить...", callback_data="adm_add")],
  [InlineKeyboardButton("🚫 Удалить...", callback_data="adm_del")],
  [InlineKeyboardButton("Назад", callback_data="0")]
]
admin_add_actions_keyboard = [
  [InlineKeyboardButton("Мероприятие", callback_data="add_vnt")],
  [InlineKeyboardButton("Стажировка", callback_data="add_int")],
  [InlineKeyboardButton("Вакансия", callback_data="add_vcn")],
  [InlineKeyboardButton("Назад", callback_data="adm")]
]
back_keyboard = [
  [InlineKeyboardButton("Назад", callback_data="0")]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Отправляет сообщение старта."""
  if context.user_data.get("adm", False):
    reply_markup = InlineKeyboardMarkup(admin_keyboard)
    await update.message.reply_text("Приветствуем тебя в боте Центра Карьеры! Выбери нужную тебе категорию:", reply_markup=reply_markup)
  else:
    reply_markup = InlineKeyboardMarkup(main_keyboard)
    await update.message.reply_text("Приветствуем тебя в боте Центра Карьеры! Выбери нужную тебе категорию:", reply_markup=reply_markup)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Обрабатывает отправляемые пользователем сообщения в зависимости от контекста."""
  text = update.message.text
  if text == secrets.ADMIN_SECRET:
    context.user_data["adm"] = True
  elif context.user_data.get("adding_init", False):
    pass
  elif context.user_data.get("adding_set_title", False):
    pass
  elif context.user_data.get("adding_set_text", False):
    pass


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Проверяет, что за кнопка была нажата."""
  query = update.callback_query
  await query.answer()
  if query.data == "0":
    # Начало
    if context.user_data.get("adm", False):
      reply_markup = InlineKeyboardMarkup(admin_keyboard)
      await query.edit_message_text("Приветствуем тебя в боте Центра Карьеры! Выбери нужную тебе категорию:", reply_markup=reply_markup)
    else:
      reply_markup = InlineKeyboardMarkup(main_keyboard)
      await query.edit_message_text("Приветствуем тебя в боте Центра Карьеры! Выбери нужную тебе категорию:", reply_markup=reply_markup)
  elif query.data == "1":
    # Мероприятия
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    await query.edit_message_text("Предстоящие мероприятия:\n\n🔹Пока что предстоящих мероприятий нет.", reply_markup=reply_markup)
  elif query.data == "2":
    # Стажировки
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    await query.edit_message_text("Доступные стажировки:\n\n🔹Пока что стажировок нет.", reply_markup=reply_markup)
  elif query.data == "3":
    # Вакансии
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    await query.edit_message_text("Открытые вакансии:\n\n🔹Пока что открытых вакансий нет.", reply_markup=reply_markup)
  elif query.data == "adm":
    # Администрирование
    if not context.user_data.get("adm", False): return
    reply_markup = InlineKeyboardMarkup(admin_actions_keyboard)
    await query.edit_message_text("Выберите действие:", reply_markup=reply_markup)
  elif query.data == "adm_add":
    pass


def main() -> None:
  """Запускает бота."""
  application = Application.builder().token(secrets.TELEGRAM_TOKEN).build()
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button))
  application.add_handler(MessageHandler(None, handle_text))
  print('Бот запущен.')
  application.run_polling()


if __name__ == '__main__':
  main()
