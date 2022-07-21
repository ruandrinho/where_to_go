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

Для деплоя обязательно укажите `DEBUG=False` и впишите через запятую значения в `ALLOWED_HOSTS`

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

## Загрузка данных

Помимо создания объектов в админке, можно воспользоваться специальной командой.

Загрузите на сервер файл с новым объектом в формате json по [образцу](https://github.com/devmanorg/where-to-go-places/blob/master/places/%D0%94%D0%BE%D0%BC%2C%20%D0%B3%D0%B4%D0%B5%20%D1%81%D0%BD%D0%B8%D0%BC%D0%B0%D0%BB%D1%81%D1%8F%20%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%20%C2%AB%D0%9F%D0%BE%D0%BA%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B5%20%D0%B2%D0%BE%D1%80%D0%BE%D1%82%D0%B0%C2%BB.json).

Выполните команду:
```
python manage.py load_place url_файла_с_данными
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
