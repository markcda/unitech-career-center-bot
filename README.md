# Бот Центра карьеры Технологического Университета

Бот предназначен для выдачи справочной информации о доступных мероприятиях, стажировках и вакансиях для студентов Технологического Университета.

## Быстрый старт

Отредактируйте `secrets-example.py`, вставив туда `TELEGRAM_TOKEN` и остальные данные (база данных MySQL, ID администраторов в Telegram), сохраните как `secrets.py`.

```bash
git clone https://github.com/markcda/unitech-career-center-bot
cd unitech-career-center-bot
pip install -r requirements.txt
python bot.py
```

## Хостинг на PythonAnywhere.com

Зарегистрируйтесь, войдите в консоль и введите команды:

```bash
git clone https://github.com/markcda/unitech-career-center-bot
cd unitech-career-center-bot
pip install -r requirements.txt
```

Создайте базу данных MySQL (вкладка `Databases`) и задайте пароль.

Отредактируйте `secrets-example.py`, вставив туда `TELEGRAM_TOKEN` и остальные данные (база данных MySQL, ID администраторов в Telegram), сохраните как `secrets.py` в папке `/var/www`.

Создайте новое Web-приложение (вкладка `Web`; выберите `Manual ...` при выборе вида Web-приложения, затем выберите последнюю версию Python). Зайдите в папку `/var/www` и отредактируйте ваш `username_pythonanywhere_com_wsgi.py`, введя туда содержимое файла `pythonanywhere.py`. После этого перезапустите Web-приложение.
