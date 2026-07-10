import pytest

VALID_REGISTER = {
    "email": "kot@pes.ru",
    "password": "32112343",
    "first_name": "Sam",
    "last_name": "Olegov",
    "phone_number": "89097771232",

}

@pytest.mark.parametrize(
    "field, bad_value",
    [
        ("email", "bad"),
        ("password", "321"),
        ("first_name", "D"),
        ("last_name", "s"),
        ("phone_number", "3")
    ]
)
async def test_check_invalid_register(ac, field, bad_value):
    payload = {**VALID_REGISTER, field: bad_value}
    response = await ac.post("/auth/register", json=payload)

    assert response.status_code == 422