# foodgram
foodgram
Финальная сборка доступна по адресу: 51.250.31.20
Пользователь: email(pirogov@yandex.ru), password(Pfanenshtil1)
Суперпользователь: login(ipl), password(1)

# Описание

Продуктовый помошник Foodgram. Социальная сеть для обмена рецептами, общения и развития кулинарных навыков.

# Шаблон наполнения env-файла

Для корректного старта контейнеров Docker необходимые следующие данные:

1. DB_ENGINE - в данном случае используется postgresql
2. DB_NAME=postgres - имя базы данных
3. POSTGRES_USEК - логин для подключения к базе данных
4. POSTGRES_PASSWORD - пароль для подключения к БД
5. DB_HOST=db - название сервиса контейнера в Docker
5. DB_PORT=5432 - порт для подключения к БД

# Установка

Клонировать репозиторий и перейти в него в командной строке.

Наполнить env-файл.

Запустите docker-compose:

```
docker-compose up
```

В новом окне терминала выполнить миграции:

```
docker-compose exec backend python manage.py migrate --noinput
```

Собрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Открыть проект в браузере по адресу http://127.0.0.1/


# Автор
[IPfa](https://github.com/IPfa).

# Лицензия
MIT License