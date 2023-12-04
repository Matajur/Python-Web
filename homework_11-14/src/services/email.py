from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr, BaseModel

from src.conf.config import settings
from src.services.auth import auth_service

VERIFICATION_TEMPLATE = "email_verification_template.html"
RESET_PASSWORD_TEMPLATE = "email_reset_password_template.html"


class EmailSchema(BaseModel):
    email: EmailStr


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Contacts App",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)


async def send_verification_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to confirm their email address.
        The function takes in three arguments:
            -email: the user's email address, which is used as a unique identifier for them.
            -username: the username of the user, which is displayed in the message body of
                confirmation emails sent out by this function. This helps users identify that they are
                receiving an authentic confirmation request from our service and not some phishing attempt.

    :param email: EmailStr: Specify the email address of the recipient
    :param username: str: Pass the username of the user to be used in the email template
    :param host: str: Pass in the host url of the application
    :return: A coroutine
    :doc-author: Trelent
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name=VERIFICATION_TEMPLATE)
    except ConnectionErrors as err:
        print(err)


async def send_reset_password_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to reset the password.
        The function takes in three arguments:
            -email: the user's email address, which is used as a unique identifier for them.
            -username: the username of the user, which is displayed in the message body of
                confirmation emails sent out by this function. This helps users identify that they are
                receiving an authentic confirmation request from our service and not some phishing attempt.

    :param email: EmailStr: Specify the email address of the recipient
    :param username: str: Pass the username of the user to be used in the email template
    :param host: str: Pass in the host url of the application
    :return: A coroutine
    :doc-author: Trelent
    """
    try:
        token_reset = auth_service.create_reset_token({"sub": email})
        message = MessageSchema(
            subject="Reset password",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_reset,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name=RESET_PASSWORD_TEMPLATE)
    except ConnectionErrors as err:
        print(err)
