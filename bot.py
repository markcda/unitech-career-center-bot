#!/usr/bin/env python

import MySQLdb
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
import logging


main_conn = MySQLdb.connect(
  host=os.getenv('MYSQL_ADDR'),
  user=os.getenv('MYSQL_USER'),
  password=os.getenv('MYSQL_PASS'),
  database=os.getenv('MYSQL_DATABASE')
)

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
back_keyboard = [
  [InlineKeyboardButton("Назад", callback_data="0")]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Отправляет сообщение старта."""
  reply_markup = InlineKeyboardMarkup(main_keyboard)
  await update.message.reply_text("Приветствуем тебя в боте Центра Карьеры! Выбери нужную тебе категорию:", reply_markup=reply_markup)


def get_posts(post_query_type: str) -> list[dict]:
  """Получает посты нужного типа из базы данных."""
  posts = []
  with main_conn.cursor() as cursor:
    select_query = 'SELECT * FROM posts WHERE type = %s ORDER BY id DESC LIMIT 10'
    data = (post_query_type,)
    cursor.execute(select_query, data)
    events = cursor.fetchall()
    if events:
      for event in events:
        posts.append(
          {'text': event[1], 'type': event[3]}
        )
  posts.reverse()  # Новые посты будут сверху, а не снизу
  return posts


def generate_scheduled_keyboard(num_of_buttons: int):
  """Формирует клавиатуру в три ряда для выбора постов."""
  reply_keyboard = []
  for i in range(num_of_buttons):
    if i in (0, 3, 6, 9):
      reply_keyboard.append([InlineKeyboardButton(str(i + 1), callback_data=f"get_scheduled_{i}")])
    else:
      reply_keyboard[-1].append(InlineKeyboardButton(str(i + 1), callback_data=f"get_scheduled_{i}"))
  return reply_keyboard


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Проверяет, что за кнопка была нажата."""
  query = update.callback_query
  await query.answer()
  if query.data == "0":
    context.user_data["scheduled"] = None
    context.user_data["posts_type"] = None
    reply_markup = InlineKeyboardMarkup(main_keyboard)
    await query.edit_message_text("Приветствуем тебя в боте Центра Карьеры! Выбери нужную тебе категорию:", reply_markup=reply_markup)
  elif query.data in ("1", "2", "3", "showed"):
    # Получаем посты, связанные с нужной темой
    posts = []
    post_query_type = None
    posts_type = ''
    if query.data == "showed":
      posts = context.user_data.get("scheduled")
      posts_type = context.user_data.get("posts_type")
      if posts_type == '1': post_query_type = 'мероприятия'
      elif posts_type == '2': post_query_type = 'стажировки'
      else: post_query_type = 'вакансии'
    else:
      if query.data == '1': post_query_type = 'мероприятия'
      elif query.data == '2': post_query_type = 'стажировки'
      else: post_query_type = 'вакансии'
      posts = get_posts(post_query_type)
      context.user_data["scheduled"] = posts
      context.user_data["posts_type"] = query.data
      posts_type = query.data
    # Формируем текст сообщения и клавиатуру
    reply_text = f'Предстоящие {post_query_type}:' if posts_type == '1' else f'Доступные {post_query_type}:'
    for i in range(len(posts)):
      # Показываем укороченные версии постов
      shortened = posts[i]['text'][:128].strip().replace('\n', ' ')
      tripledot = '...' if len(shortened) != len(posts[i]['text']) else ''
      reply_text += f'\n\n🔹{i+1}. {shortened}{tripledot}'
    if not len(posts): reply_text += '\n\n🔹Пока что ничего нет...'
    reply_keyboard = generate_scheduled_keyboard(len(posts))
    reply_keyboard.append([InlineKeyboardButton("Назад", callback_data="0")])
    reply_markup = InlineKeyboardMarkup(reply_keyboard)
    await query.edit_message_text(reply_text, reply_markup=reply_markup)
  elif "get_scheduled_" in query.data:
    # Отдаём пользователю нужный ему пост
    num = int(query.data.replace('get_scheduled_', ''))
    post = context.user_data.get("scheduled")[num]
    reply_keyboard = [[InlineKeyboardButton("Назад", callback_data="showed")]]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)
    await query.edit_message_text(post['text'], reply_markup=reply_markup)


def main() -> None:
  """Запускает бота."""
  application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button))
  application.run_polling()
  print('Бот запущен.')


if __name__ == '__main__':
  main()
