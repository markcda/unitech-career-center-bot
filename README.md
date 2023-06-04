# Бот Центра карьеры Технологического Университета

Бот предназначен для выдачи справочной информации о доступных мероприятиях, стажировках и вакансиях для студентов Технологического Университета.

## Быстрый старт

```bash
git clone https://github.com/markcda/unitech-career-center-bot
cd unitech-career-center-bot
```

Отредактируйте `env-example`, вставив туда необходимые данные, а затем сохраните как `.env`.

```bash
sudo docker build -t uccb .
sudo docker run -d --env-file .env uccb
```
