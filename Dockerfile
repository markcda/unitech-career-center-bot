FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Moscow

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["python", "-u", "bot.py"]
