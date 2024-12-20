from app.users.dao import UsersDAO
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("id,email,is_present", [
    (1, "test@test.com", True),
    (2, "artem@example.com", True),
    (3, "email", False),
])
async def test_find_user_by_id(id, email, is_present):
    user = await UsersDAO.find_by_id(id)

    if is_present:
        assert user
        assert user.id == id
        assert user.email == email
    else:
        assert not user