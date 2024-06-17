FROM python:3.10

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы
COPY . /app

# Скопируйте wait-for-it.sh
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest python-dotenv watchdog

# Команда для запуска приложения (можно переопределить в docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
