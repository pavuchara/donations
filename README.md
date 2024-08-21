# Все команды указаны с учетом ОС Windows:

**1. Клонируем репозиторий:**
```
git clone git@github.com:pavuchara/donations.git .
```
**2. Заполняем .env по примеру:**
```
.env.example
```
**3. Поднимаем в докере:**
```
docker compose up --build -d
```
TODO: образы бы на докерхаб, но нет смысла уже ...

## Прочее:
**1. При создании моковых данных, добавлен флаг (apps.services.constants.SEND_EMAILS):**
```
SEND_EMAILS = True
```
**2. Моковые данные для БД, конфиг для кол-ва в apps.core.managment.commands:**
```
python manage.py mock_db_data
python manage.py mock_db_data_delete
```

## URLS:
### Главная:
```
http://127.0.0.1:8000/
```

### АPI Doc:
```
http://127.0.0.1:8000/api/v1/docs/
```

## Как выглядит:
(В идеале смотреть на API)

![визуально](/media/prew.png)
