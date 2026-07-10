import pytest


@pytest.mark.parametrize("email,password,status_code", [
    ("lays@pring.com", "123456789", 409),
    ("voron@spring.com", "123456789s", 200),

])
async def test_auth_flow(email: str, password: str, status_code: int, ac):

    # /register
    resp_reg = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": "Oleg",
            "last_name": "Petrov",
            "phone_number": "89097651212"

        }
    )
    assert resp_reg.status_code == status_code
    if status_code != 200:
        return

    # /login
    resp_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert ac.cookies["access_token"]
    assert "access_token" in resp_login.json()
    assert resp_login.status_code == status_code

    # /me
    resp_me = await ac.get("/auth/get_me")
    user = resp_me.json()
    assert user["email"] == email
    assert "password" not in user
    assert "hashed_password" not in user
    assert resp_me.status_code == status_code

    # /logout
    resp_logout = await ac.post("/auth/logout")
    assert resp_logout.status_code == status_code
    assert "access_token" not in ac.cookies

