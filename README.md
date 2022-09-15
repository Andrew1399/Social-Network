# Social-Network
Graduation project. Social network on Django

# Technology Stack
- Python 3.9
- Django 4.1
- PostgreSQL
- Bootstrap4
- Semantic UI 2.4

# Installation Guide
___1) Clone git repository: git clone https://github.com/Andrew1399/Social-Network.git___

___2) In the root of the project create .env___
```
SECRET_KEY=django-insecure-_m_e-4h&%2yy%)%$wq+*2%)=i95(^krn@ok__26v97uq@th-_-
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DJANGO_DEBUG=TRUE
DB_NAME=network
DB_USER=postgres
DB_PASSWORD=mymindishappy
DB_HOST=pg_db
DB_PORT=5432
```
___3) Create image___
```
docker-compose build
```
___4) Run containers___
```
docker compose up -d migration
docker compose up -d web
docker exec -it conatiner_id python manage.py createsuperuser --> container_id(web)
```
___5) Use the link http://127.0.0.1:8000/users/home/ to go to home page or http://127.0.0.1:8000/admin/ to go to admin page___

