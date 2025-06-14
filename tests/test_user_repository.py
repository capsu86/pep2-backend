import pytest
from app.models.user import User

@pytest.mark.asyncio
async def test_add_and_get_all_users(user_repository):
    user = User(id=1, name="Test", email="test@example.com")
    await user_repository.add_user(user)
    users = await user_repository.get_all_users()
    assert len(users) == 1
    assert users[0].email == "test@example.com"
