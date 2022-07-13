#!/bin/sh
echo 'Устанавливаем окружение...'
python3 -m venv venv

echo 'Активация окружения...'
source venv/bin/activate

echo 'Установка зависимостей...'
python3 -m pip install -r requirements.txt

echo 'Создание пользователя и базы данных...'
sh ./create_db.sh

echo 'Запуск бота...'
python3 bot.py