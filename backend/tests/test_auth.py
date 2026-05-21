from app.services.auth_service import AuthService


def test_register_route(client, monkeypatch):
    def fake_register(self, payload):
        return {"user_id": "u1", "email": payload.email, "role": payload.role}

    monkeypatch.setattr(AuthService, "register", fake_register)
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Farmer One",
            "email": "farmer@example.com",
            "phone_number": "+254700000001",
            "password": "StrongPass123",
            "role": "FARMER",
        },
    )
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_login_route(client, monkeypatch):
    def fake_login(self, payload):
        return {
            "access_token": "access",
            "refresh_token": "refresh",
            "token_type": "bearer",
            "expires_at": "2026-05-21T10:00:00Z",
            "role": "FARMER",
        }

    monkeypatch.setattr(AuthService, "login", fake_login)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "farmer@example.com", "password": "StrongPass123"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["token_type"] == "bearer"
