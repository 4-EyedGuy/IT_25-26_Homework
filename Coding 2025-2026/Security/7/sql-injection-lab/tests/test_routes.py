import pytest
from app.main import app

def bearer(token: str | None) -> dict[str, str]:
    if token is None:
        return {}
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_auth_token_injection_attempt(client):
    payloads = [
        {"name": "alice' OR '1'='1", "password": "whatever"},
        {"name": "nonexist", "password": "' OR '1'='1"},
        {"name": "' OR 1=1 --", "password": "' OR 1=1 --"},
    ]

    for body in payloads:
        r = await client.post("/auth/token", json=body)
        assert r.status_code == 401, f"Possible auth SQLi: payload {body} returned {r.status_code} with body: {r.text}"


@pytest.mark.asyncio
async def test_order_id_path_injection_and_validation(client):
    bad_ids = ["1 OR 1=1", "1; DROP TABLE orders;", "1 UNION SELECT 1"]
    headers = {"Authorization": "Bearer secrettokenAlice"}

    for bid in bad_ids:
        r = await client.get(f"/orders/{bid}", headers=headers)
        assert r.status_code in (422, 404, 403)


@pytest.mark.asyncio
async def test_authorization_header_sqli_attempt(client):
    malicious_tokens = ["' OR '1'='1", "abcd' OR '1'='1", "secrettoken123' OR '1'='1"]
    for t in malicious_tokens:
        headers = bearer(t)
        r = await client.get("/orders", headers=headers)
        assert r.status_code == 401, f"Auth bypass possibility with token {t}: status {r.status_code} body: {r.text}"

@pytest.mark.asyncio
async def test_orders_bearer_injection(client):
    headers = bearer("badTokeh' OR '1'='1")
    
    params = {"limit": 1, "offset": "0"}
    r = await client.get("/orders", headers=headers, params=params)
    assert r.status_code in (401, 403), "Injection"

@pytest.mark.asyncio
async def test_example(client):
    response = await client.get("/orders")
    assert response.status_code == 401