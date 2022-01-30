# Foodgram

REST API веб приложения Foodgram написанный на Python. Foodgram - это социальная сеть для публикации и обмена рецептами. Реализованы: авторизация, публикация и редактирование рецептов, спискок избранного, список покупок с возможностью генерации pdf файла, фильтрация по тегам. 
В рабочей конфигурации бэкенд, фроненд, база данных и NGNIX запускаются на сервере через докер контейнеры. Конфигурация инфраструктуры находится в папке infra. Фронтэнд был написан сторонними разработчиками.

# Стек Технологий
Python, Django, Django REST, SQLite, PostgreSQL, Docker, NGNIX, сторонние библиотеки.

# Запуск
Для запуска необходим Docker.

Перейти в папку infra.
```
Foodgram/infra
```

В папке infra создать файл .env. Смотри пример наполнения файла ниже.

Из папки infra запустить докер контейнеры выполнив команду.
```
docker-compose up -d
```

Выполнить команды. При создании суперюзера установить свой логин и пароль.
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic
docker-compose exec backend python manage.py createsuperuser
```

**Проект доступен по адресу:**
http://localhost
**Админ зона:**
http://localhost/admin
**Redoc с endpoints для API:**
http://localhost/api/docs/

# Шаблон наполнения env-файла
Для корректного старта контейнеров Docker необходимые следующие данные:

1. DB_ENGINE - в данном случае используется postgresql (default: django.db.backends.postgresql)
2. DB_NAME - имя базы данных (default: postgres)
3. POSTGRES_USER - логин для подключения к базе данных (default: postgres)
4. POSTGRES_PASSWORD - пароль для подключения к БД (default: Password1)
5. DB_HOST - название сервиса контейнера в Docker (default: db)
5. DB_PORT - порт для подключения к БД (default: 5432)

# Автор
[IPfa](https://github.com/IPfa)