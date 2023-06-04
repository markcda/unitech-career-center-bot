import MySQLdb, os, signal, threading
from vk_api import VkApi
from datetime import datetime

stop_sig = threading.Event()


def db_update() -> None:
  """Обновляет базу данных каждые 15 минут в фоне."""
  updater_conn = MySQLdb.connect(
    host=os.getenv('MYSQL_ADDR'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASS'),
    database=os.getenv('MYSQL_DATABASE')
  )
  updater_conn.cursor().execute("""
    CREATE TABLE IF NOT EXISTS posts (
      id INT AUTO_INCREMENT PRIMARY KEY,
      text TEXT,
      date_published DATETIME,
      type VARCHAR(50)
    )
  """)
  while not stop_sig.is_set():
    # Получаем дату, начиная с которой мы будем добавлять новые события в базу данных.
    start_date = None
    with updater_conn.cursor() as cursor:
      select_last_post_query = 'SELECT date_published FROM posts ORDER BY id DESC LIMIT 1'
      cursor.execute(select_last_post_query)
      ndate = cursor.fetchone()
      if ndate: start_date = ndate[0].timestamp()
    if start_date is None: start_date = datetime(2023, 5, 1).timestamp()

    # Получаем последние 50 постов.
    vk_session = VkApi(token=os.getenv('VK_SERVICE_TOKEN'))
    vk = vk_session.get_api()
    response = vk.wall.get(owner_id=-int(os.getenv('VK_GROUP_ID')), count=50)  # {'items': []}

    # Фильтруем записи, отбрасывая те, что не содержат нужного хэштега или же старше начального времени.
    posts = response['items']
    filtered_posts = []
    for post in posts:
      post_date = post['date']
      if post_date > start_date:
        text = post['text']
        ll = text.split('#')
        if len(ll) != 2: continue
        post_type = ll[1].strip()
        if post_type in ('стажировки@career_unitech', 'вакансии@career_unitech', 'мероприятия@career_unitech'):
          filtered_posts.append(post)

    # Добавляем посты в базу данных.
    filtered_posts = sorted(filtered_posts, key=lambda x: x['date'])
    for post in filtered_posts:
      text = post['text']
      ll = text.split('#')
      text = ll[0].strip()
      date_published = datetime.fromtimestamp(post['date'])
      post_type = ll[1].strip().split('@')[0]

      insert_query = 'INSERT INTO posts (text, date_published, type) VALUES (%s, %s, %s)'
      data = (text, date_published, post_type)

      with updater_conn.cursor() as cursor:
        cursor.execute(insert_query, data)
      updater_conn.commit()

    print(f'Added {len(filtered_posts)} posts.')
    # Наконец, спим 15 минут.
    stop_sig.wait(900)


def graceful_app_shutdown(*args):
  stop_sig.set()
  exit(0)


if __name__ == "__main__":
  signal.signal(signal.SIGINT, graceful_app_shutdown)
  db_update()
