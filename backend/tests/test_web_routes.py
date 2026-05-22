from uuid import uuid4

from fastapi.testclient import TestClient


PASSWORD = "StrongPass123!"


def register_and_login(client: TestClient, role: str) -> dict:
    unique = uuid4().hex[:10]
    digits = str(uuid4().int)[-8:]
    email = f"{role.lower()}_{unique}@test.com"
    register = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": f"{role} User",
            "email": email,
            "phone_number": f"+2547{digits}",
            "password": PASSWORD,
            "role": role,
        },
    )
    assert register.status_code == 200, register.text

    login = client.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD})
    assert login.status_code == 200, login.text
    return login.json()["data"]


def set_auth_cookie(client: TestClient, token: str) -> None:
    client.cookies.set("mavuno_access_token", token)


def clear_auth_cookie(client: TestClient) -> None:
    client.cookies.clear()


def test_public_web_pages_load(real_db_client: TestClient):
    assert real_db_client.get("/").status_code == 200
    assert real_db_client.get("/login").status_code == 200
    assert real_db_client.get("/register").status_code == 200
    assert real_db_client.get("/forgot-password").status_code == 200
    assert real_db_client.get("/reset-password").status_code == 200
    assert real_db_client.get("/about").status_code == 200
    assert real_db_client.get("/contact").status_code == 200
    assert real_db_client.get("/403").status_code == 403
    assert real_db_client.get("/404").status_code == 404
    assert real_db_client.get("/500").status_code == 500


def test_protected_pages_redirect_unauthenticated_users(real_db_client: TestClient):
    protected = [
        "/dashboard",
        "/profile",
        "/settings",
        "/notifications",
        "/farmer/dashboard",
        "/buyer/dashboard",
        "/transporter/dashboard",
        "/cold-hub/dashboard",
        "/cooperative/dashboard",
        "/admin/dashboard",
    ]
    for path in protected:
        response = real_db_client.get(path, follow_redirects=False)
        assert response.status_code == 302, f"{path} should redirect"
        assert response.headers.get("location") == "/login"


def test_role_dashboard_redirect_from_shared_dashboard(real_db_client: TestClient):
    role_to_dashboard = {
        "FARMER": "/farmer/dashboard",
        "BUYER": "/buyer/dashboard",
        "TRANSPORTER": "/transporter/dashboard",
        "COLD_HUB_OPERATOR": "/cold-hub/dashboard",
        "COOPERATIVE_ADMIN": "/cooperative/dashboard",
        "OPS_ADMIN": "/admin/dashboard",
        "SUPER_ADMIN": "/admin/dashboard",
    }

    for role, expected in role_to_dashboard.items():
        tokens = register_and_login(real_db_client, role)
        set_auth_cookie(real_db_client, tokens["access_token"])

        response = real_db_client.get("/dashboard", follow_redirects=False)
        assert response.status_code == 302
        assert response.headers.get("location") == expected
        clear_auth_cookie(real_db_client)


def test_role_isolation_farmer_cannot_access_other_role_dashboards(real_db_client: TestClient):
    tokens = register_and_login(real_db_client, "FARMER")
    set_auth_cookie(real_db_client, tokens["access_token"])

    assert real_db_client.get("/farmer/dashboard").status_code == 200
    assert real_db_client.get("/buyer/dashboard", follow_redirects=False).status_code == 403
    assert real_db_client.get("/transporter/dashboard", follow_redirects=False).status_code == 403
    assert real_db_client.get("/admin/dashboard", follow_redirects=False).status_code == 403
    clear_auth_cookie(real_db_client)


def test_role_isolation_admin_can_access_admin_routes(real_db_client: TestClient):
    tokens = register_and_login(real_db_client, "OPS_ADMIN")
    set_auth_cookie(real_db_client, tokens["access_token"])

    assert real_db_client.get("/admin/dashboard").status_code == 200
    assert real_db_client.get("/admin/users").status_code == 200
    assert real_db_client.get("/notifications").status_code == 200
    clear_auth_cookie(real_db_client)


def test_role_route_groups_load(real_db_client: TestClient):
    role_routes = {
        "FARMER": [
            "/farmer/dashboard",
            "/farmer/harvests",
            "/farmer/harvests/create",
            "/farmer/offers",
            "/farmer/pickups",
            "/farmer/payments",
            "/farmer/reports",
        ],
        "BUYER": [
            "/buyer/dashboard",
            "/buyer/demands",
            "/buyer/demands/create",
            "/buyer/matches",
            "/buyer/orders",
            "/buyer/payments",
            "/buyer/deliveries",
        ],
        "TRANSPORTER": [
            "/transporter/dashboard",
            "/transporter/vehicles",
            "/transporter/vehicles/create",
            "/transporter/jobs",
            "/transporter/routes",
            "/transporter/earnings",
        ],
        "COLD_HUB_OPERATOR": [
            "/cold-hub/dashboard",
            "/cold-hub/capacity",
            "/cold-hub/check-in",
            "/cold-hub/check-out",
            "/cold-hub/temperature-logs",
            "/cold-hub/breaches",
        ],
        "COOPERATIVE_ADMIN": [
            "/cooperative/dashboard",
            "/cooperative/farmers",
            "/cooperative/farmers/create",
            "/cooperative/harvests",
            "/cooperative/aggregate-harvests",
            "/cooperative/reports",
        ],
        "OPS_ADMIN": [
            "/admin/dashboard",
            "/admin/users",
            "/admin/farmers",
            "/admin/buyers",
            "/admin/transporters",
            "/admin/vehicles",
            "/admin/harvests",
            "/admin/demands",
            "/admin/routes",
            "/admin/transport-jobs",
            "/admin/cold-hubs",
            "/admin/payments",
            "/admin/reports",
            "/admin/audit-logs",
            "/admin/integration-logs",
            "/admin/system-health",
            "/admin/settings",
        ],
    }

    for role, routes in role_routes.items():
        tokens = register_and_login(real_db_client, role)
        set_auth_cookie(real_db_client, tokens["access_token"])
        for path in routes:
            response = real_db_client.get(path)
            assert response.status_code == 200, f"{role} failed at {path} with {response.status_code}"
        clear_auth_cookie(real_db_client)
