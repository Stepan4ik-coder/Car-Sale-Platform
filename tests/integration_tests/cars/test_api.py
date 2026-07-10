async def test_get_cars(ac):
    response = await ac.get("/cars")

    assert response.status_code == 200