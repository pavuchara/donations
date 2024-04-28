# Установка базового образа.
FROM python:3.12.0-alpine

# Установка рабочей директории.
WORKDIR /usr/src/app

# Установка переменных среды.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка зависимостей.
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# Копирование исходного кода в рабочий каталог.
COPY . /usr/src/app

# Порт.
EXPOSE 8000

# Исполняемые команды в контейнере.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
