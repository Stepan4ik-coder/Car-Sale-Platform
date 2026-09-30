from src.tasks.tasks_for_celery import send_notifications


def check_car_price(old_car, new_car, car_id: int):

    if old_car.price != new_car.price:
        send_notifications.delay(car_id, new_car.status, new_car.price)


def check_car_status(old_car, new_car, car_id: int):

    if old_car.status != new_car.status:
        send_notifications.delay(car_id, new_car.status, new_car.price)
