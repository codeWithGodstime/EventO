
def test_create_user(client):

    response = client.post(
        "/auth/register",
        json={"email": "e@gmail.com","username": "timetokill","password": "timetokill"}
    )

    assert response.status_code == 201
    assert "uid" in response.json()
    assert "username" in response.json()
    assert "email" in response.json()
    assert "phone_number" in response.json()
    assert response.json()['is_organizer'] is True
    assert response.json()['is_active'] is False #TODO: change later


def test_login(client, user):
    response = client.post("/auth/token", json={"email": user.email, "password": "timetokill"})
    print(response, response.status_code, response.json())
    assert response.status_code == 200
    assert "data" in response.json()
    assert "access" in response.json()
    assert "refresh" in response.json()

def test_unauthenticated_user_cannot_access_profile(client, user):
    response = client.get("/auth/me")
    assert response.status_code == 401
    print(response.json())