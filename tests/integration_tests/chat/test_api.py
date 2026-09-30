from datetime import datetime

from src.schemas.cars import CarCreate
from src.schemas.messages import MessageCreate


async def register_and_login(ac, email, first_name, phone):
    await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": "password",
            "first_name": first_name,
            "last_name": "Petrov",
            "phone_number": phone,
        },
    )
    await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": "password",
        },
    )
    me = await ac.get("/auth/get_me")
    return me.json()["id"]


async def car_create(ac):
    car_data = CarCreate(
        vin="JA3BB51E9JU024751",
        engine_type="gasoline",
        litres=3,
        horse_power=255,
        year=1986,
        color="white",
        country="Japan",
        price=1000000,
        status="active",
    )
    new_car = await ac.post("/cars", json=car_data.model_dump())
    return new_car.json()["car_id"]


async def test_get_chat_history_for_buyer_and_stranger(ac, db):
    car_id = await car_create(ac)
    buyer_id = await register_and_login(ac, "my_own@example.com", "Vova", "89097771122")

    response = await ac.post("/chat", json={"car_id": car_id})
    chat_id = response.json()["chat_id"]

    await db.messages.add(
        MessageCreate(
            chat_id=chat_id,
            text="Привет",
            author_id=buyer_id,
            created_at=datetime.now(),
        )
    )
    await db.commit()

    buyer_history = await ac.get(f"/chat/{chat_id}/history")
    await register_and_login(ac, "my_another@example.com", "Dima", "89087771122")
    stranger_history = await ac.get(f"/chat/{chat_id}/history")

    assert buyer_history.status_code == 200
    assert buyer_history.json()[0]["text"] == "Привет"
    assert stranger_history.status_code == 403


async def test_get_chat_history_for_owner(ac):
    await register_and_login(ac, "owner@example.com", "Pavel", "89147771122")
    car_id = await car_create(ac)

    await register_and_login(ac, "another_user@example.com", "Ignat", "89137771122")
    response = await ac.post("/chat", json={"car_id": car_id})
    chat_id = response.json()["chat_id"]

    await ac.post(
        "/auth/login", json={"email": "owner@example.com", "password": "password"}
    )

    owner_history = await ac.get(f"/chat/{chat_id}/history")

    assert owner_history.status_code == 200


async def test_not_existing_chat(ac):
    response = await ac.get("/chat/999/history")

    assert response.status_code == 404


async def test_add_chat(ac):
    await register_and_login(ac, "own@example.com", "Petr", "89197771122")
    car_id = await car_create(ac)
    await register_and_login(ac, "wow_wow@example.com", "Sam", "89297771122")

    response = await ac.post("/chat", json={"car_id": car_id})
    second_response = await ac.post("/chat", json={"car_id": car_id})

    assert response.status_code == 200
    assert response.json()["chat_id"] == second_response.json()["chat_id"]


async def test_add_chat_with_not_existing_car(ac):
    await register_and_login(ac, "privacy@example.com", "Sergey", "89397771122")
    response = await ac.post("/chat", json={"car_id": 222})

    assert response.status_code == 404


async def test_not_allowed_to_message_with_yourself(ac):
    await register_and_login(ac, "swag@example.com", "Stepan", "89397771132")
    car_id = await car_create(ac)
    first_response = await ac.post("/chat", json={"car_id": car_id})

    assert first_response.status_code == 409
