# CarSalesPlatform

Backend-платформа для продажи автомобилей: каталог машин, регистрация и авторизация пользователей, избранное, кэширование списка авто и email-уведомления подписчикам при изменении цены или статуса.

Pet-проект на **FastAPI** с разделением на слои `api` → `repos` / `services` → `models` / `schemas`.

---

## Стек

| Технология | Назначение |
|------------|------------|
| **FastAPI** | HTTP API |
| **PostgreSQL** | Основная БД |
| **SQLAlchemy 2 (async)** | ORM |
| **Alembic** | Миграции |
| **Pydantic v2** | Валидация запросов/ответов |
| **Redis** | Кэш списка машин |
| **Celery** | Фоновые задачи (email) |
| **JWT** | Авторизация (cookie `access_token`) |
| **pytest** | Тесты |
| **Docker / Docker Compose** | Контейнеризация и деплой |

---

## Возможности

- Регистрация, логин, logout, профиль текущего пользователя (`/auth`)
- CRUD автомобилей с фильтрацией и partial PATCH
- Избранное для авторизованных пользователей (M2M user ↔ car)
- Кэш `GET /cars` (Redis, fallback на in-memory при недоступности Redis)
- Email-уведомления подписчикам при изменении цены/статуса авто (Celery)
- Кастомные HTTP-исключения: 404, 409, 401, 422
- Структурированное логирование при старте приложения
- 13 автотестов (unit + integration)

---

## Структура проекта

```
CarSalesPlatform/
├── src/
│   ├── api/                 # Роутеры: auth, cars, favorites
│   ├── services/            # Auth, email, уведомления
│   ├── repos/               # Доступ к БД (репозитории)
│   ├── models/              # SQLAlchemy ORM
│   ├── schemas/             # Pydantic-схемы
│   ├── tasks/               # Celery
│   ├── connectors/          # Redis
│   ├── loggers/             # Настройка logging
│   ├── migrations/          # Alembic
│   ├── utils/               # DBManager
│   ├── config.py
│   ├── database.py
│   └── main.py
├── tests/
│   ├── unit_tests/
│   └── integration_tests/
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── pytest.ini
├── requirements.txt
├── .env.example             # Шаблон для локального запуска
├── .env-test                # Настройки для pytest
└── README.md
```

---

## Требования

### Локальная разработка

- Python **3.11+** (в Docker используется 3.13)
- PostgreSQL
- Redis (опционально; без Redis API стартует с in-memory кэшем)

### Деплой через Docker

- Docker **24+**
- Docker Compose **v2+**

---

## Быстрый старт (локально, без Docker)

### 1. Клонирование и зависимости

```bash
git clone <url-репозитория>
cd CarSalesPlatform

python -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 2. Переменные окружения

```bash
cp .env.example .env
```

Отредактируй `.env` под свою локальную БД, Redis, JWT и SMTP.

### 3. База данных

```bash
# создай БД в PostgreSQL, если её ещё нет
createdb car_sales

alembic upgrade head
```

### 4. Запуск API

```bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 5. Celery (опционально)

```bash
celery -A src.tasks.celery_app:celery_app worker --loglevel=info
```

---

## Деплой на сервер (Docker Compose)

Подходит для развёртывания на VPS после `git clone` из **GitHub** или **GitLab**.

### 1. Подготовка сервера

```bash
git clone <url-репозитория>
cd CarSalesPlatform

cp .env.example .env
nano .env   # или vim — см. таблицу для Docker ниже
```

### 2. Docker-сеть

В `docker-compose.yml` сеть `my_network` объявлена как **external**. Создай её один раз:

```bash
docker network create my_network
```

### 3. Сборка и запуск

```bash
docker compose up --build -d
```

### 4. Миграции БД

После первого запуска контейнеров примени миграции из контейнера API:

```bash
docker compose exec car_sale_back_service alembic upgrade head
```

### 5. Проверка

| Сервис | Адрес |
|--------|--------|
| API (Swagger) | http://<IP-сервера>:7777/docs |
| PostgreSQL | Только внутри Docker-сети (`5432`) |
| Redis | Только внутри Docker-сети (`6379`) |

### 6. Остановка

```bash
docker compose down
```

Полная остановка с удалением томов Postgres (осторожно — удалит данные):

```bash
docker compose down -v
```

---

## Docker: сервисы в compose

| Сервис | Контейнер | Образ / сборка | Порт (host:container) |
|--------|-----------|----------------|------------------------|
| API | `car_sale_back` | `build: .` | `7777:8000` |
| PostgreSQL | — | `postgres:16` | Только внутренний `5432` |
| Redis | `car_sale_cache` | `redis:7` | Только внутренний `6379` |
| Celery worker | `car_sale_celery_worker` | `build: .` | — |

**Важно:** значения `POSTGRES_*` в `docker-compose.yml` должны совпадать с `DB_*` в `.env`.

Compose получает `POSTGRES_USER`, `POSTGRES_PASSWORD` и `POSTGRES_DB` из
`DB_USER`, `DB_PASS` и `DB_NAME` в `.env`.

---

## Переменные окружения

Файл `.env` **не коммитить** в git. Используй `.env.example` как шаблон.

### Локальный запуск (venv)

| Переменная | Пример | Описание |
|------------|--------|----------|
| `MODE` | `LOCAL` | Режим приложения |
| `DB_HOST` | `localhost` | Хост PostgreSQL |
| `DB_PORT` | `5432` | Порт PostgreSQL |
| `DB_USER` | `postgres` | Пользователь БД |
| `DB_PASS` | `***` | Пароль БД |
| `DB_NAME` | `car_sales` | Имя БД |
| `REDIS_HOST` | `localhost` | Хост Redis |
| `REDIS_PORT` | `6379` | Порт Redis |
| `JWT_SECRET_KEY` | длинная случайная строка | Секрет JWT |
| `JWT_ALGORITHM` | `HS256` | Алгоритм JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Время жизни токена |
| `SMTP_HOST` | `smtp.mail.ru` | SMTP-сервер |
| `SMTP_PORT` | `465` | Порт SMTP |
| `SMTP_USER` | `email@list.ru` | Логин SMTP |
| `SMTP_PASS` | `***` | Пароль приложения |
| `MAIL_FROM` | `email@list.ru` | Отправитель писем |

### Docker Compose (внутри сети контейнеров)

Для API и Celery в `.env` на сервере:

```env
MODE=PROD

DB_HOST=car_sale_postgres_service
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=sales_platform

REDIS_HOST=car_sale_cache_service
REDIS_PORT=6379

JWT_SECRET_KEY=<сгенерируй_длинный_секрет>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

SMTP_HOST=smtp.mail.ru
SMTP_PORT=465
SMTP_USER=your_email@list.ru
SMTP_PASS=your_app_password
MAIL_FROM=your_email@list.ru
```

> **Примечание:** `DB_PORT=5432` и `REDIS_PORT=6379` — внутренние порты
> Docker-сети. PostgreSQL и Redis намеренно не публикуются наружу.

---

## API

### Авторизация — `/auth`

| Метод | Путь | Auth | Описание |
|-------|------|------|----------|
| POST | `/auth/register` | Нет | Регистрация |
| POST | `/auth/login` | Нет | Вход, JWT в cookie `access_token` |
| GET | `/auth/get_me` | Да | Текущий пользователь |
| POST | `/auth/logout` | Нет | Выход (удаление cookie) |

**Регистрация:**

```json
{
  "email": "user@mail.com",
  "password": "12345678",
  "first_name": "Oleg",
  "last_name": "Petrov",
  "phone_number": "89097651212"
}
```

### Автомобили — `/cars`

| Метод | Путь | Auth | Описание |
|-------|------|------|----------|
| GET | `/cars` | Нет | Список (фильтры + кэш 30 сек) |
| GET | `/cars/{car_id}` | Нет | Одна машина |
| POST | `/cars` | Нет | Создание |
| PUT | `/cars/{car_id}` | Нет | Полное обновление |
| PATCH | `/cars/{car_id}` | Нет | Частичное обновление |
| DELETE | `/cars/{car_id}` | Нет | Удаление |

**Фильтры (query):** `engine_type`, `litres`, `horse_power`, `year`, `color`, `country`.

**Тело (создание / PUT):**

```json
{
  "engine_type": "gasoline",
  "litres": 3,
  "horse_power": 255,
  "year": 1986,
  "color": "white",
  "country": "Japan",
  "price": 1000000,
  "status": "active"
}
```

**PATCH** — можно передать только изменяемые поля, например:

```json
{
  "price": 850000
}
```

Допустимые значения:

- `engine_type`: `gasoline`, `diesel`, `electric`, `hybrid`
- `status`: `active`, `sold`, `reserved`

### Избранное — `/favorites`

| Метод | Путь | Auth | Описание |
|-------|------|------|----------|
| GET | `/favorites` | Да | Список избранных машин (`[]` если пусто) |
| POST | `/favorites` | Да | Добавить в избранное |
| DELETE | `/favorites/{car_id}` | Да | Удалить из избранного |

```json
{
  "car_id": 1
}
```

---

## Модели данных

### users

| Поле | Тип | Описание |
|------|-----|----------|
| id | int | PK |
| email | str | Уникальный |
| password | str | Хэш (argon2) |
| first_name | str | |
| last_name | str | |
| phone_number | str | |

### cars

| Поле | Тип | Описание |
|------|-----|----------|
| car_id | int | PK |
| engine_type | str | Тип двигателя |
| litres | int | Объём |
| horse_power | int | Мощность |
| year | int | Год |
| color | str | Цвет |
| country | str | Страна |
| price | int | Цена |
| status | str | `active` / `sold` / `reserved` |

### favorites

| Поле | Тип | Описание |
|------|-----|----------|
| user_id | int | FK → users.id |
| car_id | int | FK → cars.car_id |

Составной PK: `(user_id, car_id)`.

---

## Архитектура

```
HTTP Request
    ↓
api/              # FastAPI-роутеры, HTTP-исключения
    ↓
repos/            # Запросы к БД, domain-исключения
services/         # Auth, email, бизнес-логика уведомлений
    ↓
models/           # SQLAlchemy ORM → PostgreSQL

Celery worker  →  email подписчикам (favorites)
Redis          →  кэш GET /cars
```

**DBManager** — одна async-сессия на HTTP-запрос (`yield` в dependency), автоматический rollback при ошибке.

---

## Коды ответов

| Код | Когда |
|-----|-------|
| 200 | Успех |
| 401 | Нет токена / неверный email или пароль |
| 404 | Пользователь, машина или запись в избранном не найдены |
| 409 | Email уже занят / машина уже в избранном |
| 422 | Невалидные данные (Pydantic) |
| 500 | Необработанная ошибка сервера |

---

## Тесты

```bash
pytest -v
```

Используется `.env-test` (отдельная тестовая БД, `MODE=TEST`).

### Покрытие (13 тестов)

| Файл | Что проверяет |
|------|---------------|
| `unit_tests/test_auth.py` | Создание JWT |
| `integration_tests/test_auth.py` | Encode/decode JWT |
| `integration_tests/auth/test_api.py` | Register 409, полный auth flow |
| `integration_tests/test_validation.py` | 5 parametrized кейсов 422 |
| `integration_tests/cars/test_db.py` | CRUD через репозиторий |
| `integration_tests/cars/test_api.py` | GET `/cars` |
| `integration_tests/favorites/test_api.py` | GET/POST избранного |

### Инфраструктура тестов

- `dependency_overrides` — тестовая БД
- мок `@cache` — обход Redis в API-тестах
- фикстуры `ac`, `auth_client`, `db`

---

## Миграции (Alembic)

```bash
# создать миграцию
alembic revision --autogenerate -m "описание"

# применить
alembic upgrade head

# откатить на одну
alembic downgrade -1
```

---

## Сборка Docker-образа вручную

```bash
docker build -t car_sale_image .
docker run --rm -p 8000:8000 --env-file .env car_sale_image
```

Для полного стека используй `docker compose up` (см. раздел деплоя).

---

## Деплой: GitHub и GitLab

Один и тот же репозиторий можно зеркалировать на GitHub и GitLab.

**Рекомендуемый порядок на сервере:**

1. `git clone` из нужного remote
2. `cp .env.example .env` → заполнить production-значения
3. `docker network create my_network`
4. `docker compose up --build -d`
5. `alembic upgrade head`
6. Открыть порт **7777** в firewall / security group
7. Проверить http://`<server-ip>`:7777/docs

**Не коммитить:**

- `.env`
- `venv/`
- `__pycache__/`, `.pytest_cache/`

---

## Планы развития

- [ ] CI (GitHub Actions / GitLab CI) — `pytest` на push
- [ ] Тесты: login 401, car 404, DELETE favorites, PATCH одного поля
- [ ] Healthcheck для postgres в compose
- [ ] Пагинация списка машин
- [ ] Загрузка авто по СТС (ручной ввод / OCR)
- [ ] `.env.docker.example` в репозитории

---

## Лицензия

Учебный / pet-проект. Свободное использование.

---

## Автор

Pet-проект **CarSalesPlatform** — backend для платформы продажи автомобилей.
