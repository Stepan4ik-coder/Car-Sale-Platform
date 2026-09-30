import asyncio

from src.database import async_session_maker
from src.repos.favorites import FavoritesRepository
from src.services.notifications.send_emails import send_email
from src.tasks.celery_app import celery_app


async def get_subscribers(car_id):
    async with async_session_maker() as session:
        repo = FavoritesRepository(session)
        return await repo.get_users_by_car_id(car_id=car_id)


@celery_app.task
def send_notifications(car_id: int, status: str, price: int):

    subscribers = asyncio.run(get_subscribers(car_id))
    if not subscribers:
        return

    subject = f"Обновление автомобиля #{car_id}"
    body = f"Машина #{car_id}. Цена: {price}. Статус: {status}."
    for user in subscribers:
        send_email(user.email, subject, body)
