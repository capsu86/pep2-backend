import pytest
from httpx import AsyncClient
from app.main import app
from app.services.in_memory_user_service import InMemoryUserService
from app.interfaces.user_service_interface import IUserService
from app.routers.user import get_user_service

@pytest.mark.asyncio
async def test_create_and_get_users():
    # override the DI to use in-memory service
    app.dependency_overrides[get_user_service] = lambda: InMemoryUserService()

    async with AsyncClient(app=app, base_url="http://test") as client:
        resp1 = await client.post("/users", json={"id":3,"name":"API","email":"api@example.com"})
        assert resp1.status_code == 200
        resp2 = await client.get("/users")
        data = resp2.json()
        assert any(u["email"] == "api@example.com" for u in data)

    app.dependency_overrides.clear()
