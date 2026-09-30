from src.sockets import chat_handlers
from src.sockets.chat_handlers import handle_join_room


async def test_handle_join_room(monkeypatch):
    called = dict()

    class TestCar:
        owner_id = 2

    class TestChat:
        buyer_id = 1

    async def fake_sio_get_session(sid):
        return {"user_id": 1}

    async def fake_getting_car_and_chat(chat_id):
        fake_car = TestCar()
        fake_chat = TestChat()

        return fake_car, fake_chat

    async def fake_enter_room(sid, room):
        called["sid"] = sid
        called["room"] = room

    async def fake_save_session(sid, data: dict):
        return True

    monkeypatch.setattr(chat_handlers.sio, "get_session", fake_sio_get_session)
    monkeypatch.setattr(
        chat_handlers, "getting_car_and_chat", fake_getting_car_and_chat
    )
    monkeypatch.setattr(chat_handlers.sio, "enter_room", fake_enter_room)
    monkeypatch.setattr(chat_handlers.sio, "save_session", fake_save_session)

    await handle_join_room("fake_sid", {"chat_id": 5})

    assert called["sid"] == "fake_sid"
    assert called["room"] == "chat:5"
