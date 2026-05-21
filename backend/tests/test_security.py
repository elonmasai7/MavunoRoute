from types import SimpleNamespace
from uuid import uuid4

from app.dependencies import get_current_user


def test_unauthorized_without_token(client):
    app = client.app
    app.dependency_overrides.pop(get_current_user, None)
    response = client.get("/api/v1/users")
    assert response.status_code == 401


def test_forbidden_for_insufficient_role(client):
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=uuid4(), role="FARMER", is_active=True)
    response = client.get("/api/v1/users")
    assert response.status_code == 403
