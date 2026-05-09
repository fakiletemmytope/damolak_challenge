import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert data["role"] == "user"

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    # First registration
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    
    # Duplicate registration
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    # Register first
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    
    # Login
    response = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user_details"]["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    # Register first
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    
    # Login with wrong password
    response = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_logout(client: AsyncClient):
    # Register and Login
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    login_res = await client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    token = login_res.json()["token"]
    
    # Logout (requires auth token)
    response = await client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Logout"
