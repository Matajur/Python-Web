import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User, Role
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestRepositoryUsers(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(__spec__=Session)
        self.role = Role("admin")
        self.user = User(
            id=1,
            username="superuser",
            email="test@mate.ua",
            password="top_sectet",
            avatar="http://gravatar",
            refresh_token="qwertyuiop1234567890",
            role=self.role,
            confirmed=False,
        )

    # get_user_by_email

    async def test_get_user_by_email_found(self):
        self.session.query(User).filter_by().first.return_value = self.user
        result = await get_user_by_email(email=self.user.email, db=self.session)  # type: ignore
        self.assertEqual(result, self.user)

    async def test_get_user_by_email_not_found(self):
        self.session.query(User).filter_by().first.return_value = None
        result = await get_user_by_email(email=self.user.email, db=self.session)  # type: ignore
        self.assertIsNone(result)

    # create_user

    async def test_create_user(self):
        body = UserModel(
            username="superuser",
            email="test@meta.ua",
            password="top_secret",
        )
        result = await create_user(body=body, db=self.session)  # type: ignore
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))  # if result has attribute ID
        self.assertTrue(hasattr(result, "avatar"))
        self.assertTrue(hasattr(result, "refresh_token"))
        self.assertTrue(hasattr(result, "role"))
        self.assertTrue(hasattr(result, "confirmed"))

    # update_token

    async def test_update_token(self):
        refresh_token = "1234567890qwertyuiop"
        await update_token(user=self.user, refresh_token=refresh_token, db=self.session)
        self.assertEqual(self.user.refresh_token, refresh_token)

    # confirmed_email

    async def test_confirmed_email(self):
        self.session.query(User).filter_by().first.return_value = self.user
        await confirmed_email(email=self.user.email, db=self.session)  # type: ignore
        self.assertTrue(self.user.confirmed)

    # update_avatar

    async def test_update_avatar(self):
        url = "http://cloudinary"
        self.session.query(User).filter_by().first.return_value = self.user
        result = await update_avatar(email=self.user.email, url=url, db=self.session)  # type: ignore
        self.assertEqual(result.avatar, url)
