# CarSalesPlatform

Backend для продажи автомобилей: каталог, регистрация, избранное, распознавание VIN по фото СТС и чат покупателя с продавцом.

Pet-проект на **FastAPI**. Данные в PostgreSQL, кэш списка машин в Redis, письма подписчикам через Celery. VIN читает PaddleOCR. Чат идёт по Socket.IO и сохраняется в базу.

---

## Стек

| Технология | Назначение |
|------------|------------|
| **FastAPI** | HTTP API |
| **PostgreSQL** | Основная БД |
| **SQLAlchemy 2 (async)** | ORM |
| **Alembic** | Миграции |
| **Pydantic v2** | Валидация запросов и ответов |
| **Redis** | Кэш `GET /cars` |
| **Celery** | Письма при смене цены или статуса |
| **JWT** | Авторизация, cookie `access_token` |
| **PaddleOCR** | Поиск и чтение VIN на фото СТС |
| **Tesseract** | Общий текст документа |
| **python-socketio** | Комнаты чата |
| **pytest** | Тесты |
| **Docker Compose** | Postgres, Redis, API и Celery |

---

## Что умеет

- Регистрация, логин, logout, текущий пользователь (`/auth`)
- Машины: список с фильтрами, карточка, создание, полное и частичное обновление, удаление. Менять и удалять может только владелец
- Избранное
- Кэш списка машин на 30 секунд. Если Redis недоступен, кэш переключается на память процесса
- Письмо подписчикам из избранного, когда меняются цена или статус
- Фото СТС: PaddleOCR находит подпись VIN, вырезает строку и читает номер. Отдельный запрос подставляет пример характеристик по уже известному VIN
- Чат: один диалог на пару «машина + покупатель». Продавец — это `cars.owner_id`, в чате он не хранится
- Сообщение пишется в таблицу `message` и уходит в комнату `chat:{chat_id}`
- История сообщений: `GET /chat/{chat_id}/history`. Её видят покупатель и владелец машины
- При выходе из сокета вкладка покидает комнату, если успела в неё войти

Списка чатов нет: клиент открывает диалог по `chat_id`.

Демо-страницы для ручной проверки, не часть API:

- http://127.0.0.1:8000/demo/chat.html
- http://127.0.0.1:8000/demo/chat-reel.html

---

## Структура

```
CarSalesPlatform/
├── src/
│   ├── api/            # auth, cars, favorites, vrc, chat
│   ├── services/
│   │   ├── auth/
│   │   ├── cars/
│   │   ├── notifications/
│   │   └── sts/        # предобработка фото, PaddleOCR, разбор VIN
│   ├── repos/
│   ├── models/
│   ├── schemas/
│   ├── sockets/        # connect, join_room, send_message, disconnect
│   ├── tasks/          # Celery
│   ├── connectors/     # Redis
│   ├── migrations/
│   ├── static/         # демо чата
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
├── .env.example
└── .env-test
```

---

## Требования

Локально: Python 3.11+ (в Docker — 3.13), PostgreSQL, Redis по желанию.

Для Compose: Docker 24+ и Docker Compose v2.

---

## Локальный запуск

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

В `.env` для запуска из venv:

```env
DB_HOST=localhost
REDIS_HOST=localhost
```

Postgres и Redis можно поднять отдельно:

```bash
docker compose up -d car_sale_postgres_service car_sale_cache_service
alembic upgrade head
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Swagger: http://127.0.0.1:8000/docs

Celery, если нужны письма:

```bash
celery -A src.tasks.celery_app:celery_app worker --loglevel=info
```

---

## Docker Compose

Сеть `my_network` в compose внешняя. Один раз:

```bash
docker network create my_network
docker compose up --build -d
docker compose exec car_sale_back_service alembic upgrade head
```

API с хоста: http://127.0.0.1:7777/docs

Compose подставляет контейнерам `DB_HOST=car_sale_postgres_service` и `REDIS_HOST=car_sale_cache_service` поверх `.env`. Один файл окружения подходит и для venv, и для Docker.

Остановка: `docker compose down`. С томом Postgres: `docker compose down -v`.

| Сервис | Контейнер | Порт на хосте |
|--------|-----------|----------------|
| API | `car_sale_back` | 7777 |
| PostgreSQL 16 | `car_sale_postgres_service` | 5432 |
| Redis 7 | `car_sale_cache_service` | 6379 |
| Celery | `car_sale_celery_worker` | — |

---

## Окружение

`.env` не коммитится. Шаблон — `.env.example`. Тесты читают `.env-test` (`MODE=TEST`).

| Переменная | Зачем |
|------------|--------|
| `MODE` | `LOCAL` или `TEST` |
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME` | PostgreSQL |
| `REDIS_HOST`, `REDIS_PORT` | Redis |
| `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` | Токен |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `MAIL_FROM` | Почта. Для Mail.ru нужен пароль приложения |

`POSTGRES_USER`, `POSTGRES_PASSWORD` и `POSTGRES_DB` в compose берутся из `DB_USER`, `DB_PASS` и `DB_NAME`.

---

## API

Авторизация — cookie `access_token`. Тело логина клиент не использует как источник `user_id`.

### `/auth`

| Метод | Путь | Кто | Что |
|-------|------|-----|-----|
| POST | `/auth/register` | нет | Регистрация |
| POST | `/auth/login` | нет | Вход, cookie |
| GET | `/auth/get_me` | да | `id` и `email` |
| POST | `/auth/logout` | нет | Стирает cookie |

```json
{
  "email": "user@mail.com",
  "password": "12345678",
  "first_name": "Oleg",
  "last_name": "Petrov",
  "phone_number": "89097651212"
}
```

### `/cars`

| Метод | Путь | Кто | Что |
|-------|------|-----|-----|
| GET | `/cars` | нет | Список, фильтры, кэш 30 сек |
| GET | `/cars/{car_id}` | нет | Одна машина |
| POST | `/cars` | да | Создание. `owner_id` берётся из токена |
| PUT | `/cars/{car_id}` | владелец | Полная замена |
| PATCH | `/cars/{car_id}` | владелец | Частичное обновление |
| DELETE | `/cars/{car_id}` | владелец | Удаление и письмо подписчикам |

Фильтры: `engine_type`, `litres`, `horse_power`, `year`, `color`, `country`.

```json
{
  "vin": "JA3BB51E9JU024751",
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

`engine_type`: `gasoline`, `diesel`, `electric`, `hybrid`.  
`status`: `active`, `sold`, `reserved`.  
VIN — 17 символов, без I, O и Q.

### `/favorites`

| Метод | Путь | Кто | Что |
|-------|------|-----|-----|
| GET | `/favorites` | да | Список |
| POST | `/favorites` | да | Добавить `{ "car_id": 1 }` |
| DELETE | `/favorites/{car_id}` | да | Убрать |

### `/vrc`

| Метод | Путь | Что |
|-------|------|-----|
| POST | `/vrc` | Фото СТС, в ответе VIN |
| POST | `/vrc/autofill` | Пример характеристик по уже известному VIN |

Номер читает английская модель PaddleOCR после вырезки строки. Если VIN не собрался, ответ `422`.

### `/chat`

| Метод | Путь | Кто | Что |
|-------|------|-----|-----|
| POST | `/chat` | да | Найти или создать диалог. Тело: `{ "car_id": 1 }` |
| GET | `/chat/{chat_id}/history` | покупатель или владелец | Сообщения по времени |

Повторный `POST` на ту же машину от того же покупателя возвращает тот же `chat_id`. Владелец не может открыть чат по своей машине: `409`.

### Socket.IO

Подключение только с cookie `access_token`. В сессии сокета хранится `user_id`.

| Событие | От клиента | Что делает сервер |
|---------|------------|-------------------|
| `join_room` | `{ "chat_id": 1 }` | Пускает покупателя или владельца в комнату `chat:1` и записывает её имя в сессию |
| `send_message` | `{ "chat_id": 1, "text": "..." }` | Та же проверка, запись в `message`, событие `new_message` в комнату |
| `disconnect` | — | `leave_room`, если комната была записана |

`new_message`: `message_id`, `text`, `author_id`, `created_at`.

---

## Модели

**users** — `id`, уникальный `email`, хэш пароля (argon2), `first_name`, `last_name`, `phone_number`.

**cars** — `car_id`, `owner_id` → users, `vin`, `engine_type`, `litres`, `horse_power`, `year`, `color`, `country`, `price`, `status`.

**favorites** — составной ключ `(user_id, car_id)`.

**chat** — `chat_id`, `car_id`, `buyer_id`, `created_at`. Пара `(car_id, buyer_id)` уникальна.

**message** — `message_id`, `chat_id`, `author_id`, `text`, `created_at`.

---

## Как устроен запрос

HTTP-ручка берёт сессию через `DBManager` и ходит в репозиторий. Проверка владельца машины — `getting_existing_car`. Письма ставит Celery. `GET /cars` кэшируется в Redis.

Сокет сам открывает `DBManager`: у него нет HTTP-зависимости. Участник чата — это `buyer_id` диалога или `owner_id` машины.

---

## Коды ответов

| Код | Когда |
|-----|--------|
| 200 | Успех |
| 401 | Нет токена, токен просрочен или повреждён |
| 403 | Чужое объявление или чужой чат |
| 404 | Нет пользователя, машины, чата или избранного |
| 409 | Email занят, машина уже в избранном, нельзя писать себе |
| 415 | Плохой или неподдерживаемый файл СТС |
| 422 | Тело не прошло схему или VIN не распознан |
| 500 | Необработанная ошибка |

Неверный логин сейчас тоже отвечает `404` («пользователь не найден»), не `401`.

---

## Тесты

```bash
pytest -q
```

59 тестов. База поднимается из `.env-test`, таблицы пересоздаются на сессию. Кэш в тестах отключён. Фикстура `ac` — HTTP-клиент без сети, cookie живёт на весь прогон.

Покрыто: JWT, регистрация и логин, валидация, CRUD машин и чужие правки, избранное, OCR и разбор VIN, история чата для покупателя, владельца и чужого, повторный `POST /chat`, нет машины, отказ писать себе, вход покупателя в комнату.

---

## Миграции

```bash
alembic revision --autogenerate -m "описание"
alembic upgrade head
alembic downgrade -1
```

---

## Что сознательно не сделано

- Список чатов без ручного `chat_id`
- Отдельные тесты на `send_message` и `disconnect`
- Пагинация каталога
- CI
