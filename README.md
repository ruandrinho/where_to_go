# Сайт «Куда пойти — Москва глазами Артёма»

Каталог экскурсионных компаний и проектов на карте Москвы.

Рабочая версия: https://andrinho.pythonanywhere.com/

Админка: https://andrinho.pythonanywhere.com/admin

## Как установить

Клонируйте репозиторий или скачайте архив и распакуйте.

Создайте файл окружения `.env` и заполните необходимым данными:
```
SECRET_KEY=write_your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_PRELOAD=True
```

Для деплоя обязательно укажите `DEBUG=True` и впишите через запятую значения в `ALLOWED_HOSTS`

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

## Запуск

Перед запуском сайта инициализируйте базу данных:
```
python manage.py migrate
```

Для запуска выполните:
```
python manage.py runserver
```

Для работы в админке создайте суперпользователя:
```
python manage.py createsuperuser
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
