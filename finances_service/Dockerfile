# Используйте официальный образ Python как базовый
FROM python:3.9
ENV API_PORT=$API_PORT

# Установите рабочую директорию в контейнере
WORKDIR /usr/src/app

# Установите зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте код проекта в контейнер
COPY . .

# Сделайте порт 8000 доступным за пределами контейнера
EXPOSE $API_PORT


# Укажите команду для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:$API_PORT"]