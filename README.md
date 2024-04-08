# Foodgram
Backend in form of REST API, written on Python, for Foodgram application. Foodgram is an learning project and frontend for this project was developed my other team. This application is a social media for people who love cooking and need some place, where they could public and exchange recipes. Foodgram offers following functionality:

- User Managment System
- System of subscriptions
- Users could public recipes with pictures and tag recipes to different groups
- Tags and ingredients are managed by application administrators in the admin zone
- Users could create add recipes to favorites section and to the shopping list
- Ingredients needed for recipes from the shopping list could be exported in a PDF form

Whole project runs on Docker and uses Docker containers. Configuration of the infrastructure is in infra folder.

# Technology Stack
Python, Django, Django REST, PostgreSQL, Docker, NGNIX, Gunicorn, Djoser, Pillow.

# Launching
For launch Docker application is needed.

Go to the infra folder.
```
Foodgram/infra
```

In the infra folder create an env-file (.env)  Please see env-file section below.

From infra folder start docker containers.
```
docker-compose up -d
```

After successful app start run following commands. By superuser creation set your own data .
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic
docker-compose exec backend python manage.py createsuperuser
```

**Project is available on:**
http://localhost
**Admin zone:**
http://localhost/admin
**Redoc with API endpoints:**
http://localhost/api/docs/

# Template for env-file
For correct functionality of database following data is needed:

DB_ENGINE - in our case this is postgresql (default: django.db.backends.postgresql)
DB_NAME - database name (default: postgres)
POSTGRES_USER - login for database connection (default: postgres)
POSTGRES_PASSWORD - password for database connection (default: Password1)
DB_HOST - name of service container in Docker (default: db)
DB_PORT - port for the database connection (default: 5432)

# Автор
[IPfa](https://github.com/IPfa)