import unittest
from unittest.mock import patch, MagicMock
from fastapi_mail import FastMail, MessageSchema, MessageType

from src.services import email as serv_email
from src.services.auth import auth_service


class TestServiceSEmail(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.username = "test_user"
        self.email = "test@example.com"
        self.host = "test_host"
        self.token = "qwertyuiop1234567890"

    @patch.object(serv_email, "FastMail", return_value=MagicMock(spec=FastMail))
    async def test_send_verification_email(self, MockedFastMail):
        fm = MockedFastMail.return_value
        auth_service.create_email_token = MagicMock(return_value=self.token)
        await serv_email.send_verification_email(
            email=self.email, username=self.username, host=self.host
        )  # type: ignore

        fm.send_message.assert_called_once()

        expected_message = MessageSchema(
            subject="Confirm your email",
            recipients=[self.email],  # type: ignore
            template_body={
                "host": self.host,
                "username": self.username,
                "token": self.token,
            },
            subtype=MessageType.html,
        )
        fm.send_message.assert_called_with(
            expected_message, template_name=serv_email.VERIFICATION_TEMPLATE
        )


"""
    @patch.object(email_service, "FastMail", return_value=MagicMock(spec=FastMail))
    async def test_send_reset_password_email(self, MockedFastMail):
        fm_instance = MockedFastMail.return_value

        await email_service.send_reset_password_email("test@example.com", "test_token")

        # Перевірка, що send_message було викликано
        fm_instance.send_message.assert_called_once()

        # Перевірка аргументів
        expected_message = MessageSchema(
            subtype="plain",
            subject="Reset Password",
            recipients=["test@example.com"],
            body="Your token: test_token",
        )
        fm_instance.send_message.assert_called_with(expected_message)
"""


if __name__ == "__main__":
    unittest.main()
