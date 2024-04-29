# Все команды указаны с учетом ОС Windows:

**1. Создаем рабочую директорию.**

**2. Клонируем репозиторий:**
```
git clone git@github.com:pavuchara/donations.git .
```

## Проверка без докера, если с докером то пропускаем пункты 3-12:


**3. Создаем виртуальное окружение:**
```
python -m venv venv
```
**4. Активируем вирутальное окружение:**
```
source venv/Scripts/activate
```
**5. Обновляем pip:**
```
python -m pip install --upgrade pip
```
**6. Устанавливаем зависимости:**
```
pip install -r requirements.txt
```
**7. Создаем пользователя и БД в Postgres:**
```
CREATE USER test123 WITH PASSWORD 'test123';
```
```
CREATE DATABASE test123 OWNER test123 ENCODING 'UTF8';
```
(эти данные необходимы для .env файла)

**8. .env файл:**
Пункт 14

**9. Создаем и применяем миграции:**
```
python manage.py makemigrations
```
```
python manage.py migrate
```

**10. Запускаем сервер:**
```
python manage.py runserver
```
**11. Проверяем:**
http://127.0.0.1:8000/

**12. Наполнение моковыми данными:**
Пункт 19.

***
***
***
## Проверка с Docker

**14. В корневой директории есть файл:**
```
 .env.template
```
**Необходимо создать .env файл и заполнить его своими данными:**
_Тестовые данные в шаблоне уже есть, если использоуем докер, то можно просто скопировать из шаблона в .env_
Если используем докер, то:
```
POSTGRESQL_HOST='pgdb'
```
если нет то
```
POSTGRESQL_HOST='localhost'
```
_(DJANGO_SECRET_KEY оставлен для удобства, т.к. это тестовое задание)_


**15. Создаем том для для хранения БД.**
```
docker volume create pgdbdata
```
**16. Создаем сеть:**
```
docker network create donations_network
```
**17. Запускаем докер:**
```
docker-compose up
```
**18. Создаем и применяем миграции:**
```
docker-compose exec django python manage.py makemigrations
```
```
docker-compose exec django python manage.py migrate
```

**19. Наполнение моковыми данными (Данными наполяем после запуска контейнера если используем докер):**
**Важно: подеключен бекенд для Email:**

```
'django.core.mail.backends.filebased.EmailBackend'
```
Соотв. писма будут храниться локально:
```
BASE_DIR / 'sent_emails'
```
При создании моковых данных, добавлен флаг (`apps.services.constants.SEND_EMAILS`):
```
SEND_EMAILS = True
```
Его можно переключить на False, тогда при создании тысяч записей, данные не будут захламлять директорию.
apps.core.managment.commands находятся 2 файла:
- `mock_db_data` - наполнение данных, там можно задать конфигурации для наполнения БД определенным кол-вом данных.
- `mock_db_data_delete` - удаление всех данных кроме суперюзера

**Важно: при повтрном наполнени БД, пожалуйста, удалите старые данные, т.к. данные содаются в цикле, и могут быть поворные id:**
**Если используем докер (после создания сети и запуска контейнера):**
```
docker-compose exec django python manage.py mock_db_data
```
```
docker-compose exec django python manage.py mock_db_data_delete
```

**Если нет:**
```
python manage.py mock_db_data
```
```
python manage.py mock_db_data_delete
```

**20. Проверяем работу:**
http://127.0.0.1:8000/

**21. После тестов можно снести таблицу и нового пользвоателя:**
```
DROP USER test123;
```
```
DROP DATABASE test123;
```


## API и суперюзер

**1. Доступы активированы только для суперюзера.**

**2. Создать суперюзера:**
```
python manage.py createsuperuser
```

```
docker-compose exec django python manage.py createsuperuser
```

## Как выглядит:

![визуально](/media/prew.png)
