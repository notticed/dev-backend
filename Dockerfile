# Используем базовый образ Python
FROM python:3.9

# Устанавливаем переменные среды
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости проекта
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . /app/

# Открываем порт, который будет использоваться Uvicorn
EXPOSE 8000

# Запускаем Uvicorn при старте контейнера
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8888"]