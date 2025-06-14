import pytest
from app.models.user import User

@pytest.mark.asyncio
async def test_service_creates_and_lists(user_service):
    user = User(id=2, name="Svc", email="svc@example.com")
    await user_service.create_user(user)
    users = await user_service.list_users()
    assert any(u.email == "svc@example.com" for u in users)
