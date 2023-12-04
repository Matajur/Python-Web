from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user with that email if it exists. If no such user exists,
    it returns None.

    :param email: str: Specify the type of data that is expected to be passed into the function
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    return db.query(User).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session):
    """
    The create_user function creates a new user in the database.


    :param body: UserModel: Pass the data from the request body to this function
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    g = Gravatar(body.email)
    new_user = User(**body.model_dump(), avatar=g.get_image())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, refresh_token: str, db: Session) -> None:
    """
    The update_token function updates the refresh_token for a user in the database.
        Args:
            user (User): The User object to update.
            refresh_token (str): The new refresh token to store in the database.
            db (Session): A Session object used to interact with the database.

    :param user: User: Identify the user in the database
    :param refresh_token: Update the user's refresh token in the database
    :param db: Session: Access the database
    :return: None
    :doc-author: Trelent
    """
    user.refresh_token = refresh_token  # type: ignore
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function marks a user as confirmed in the database.

    :param email: str: Get the email of the user
    :param db: Session: Access the database
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True  # type: ignore
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    Args:
        email (str): The email address of the user to update.
        url (str): The URL for the new avatar image.
        db (Session, optional): A database session object to use instead of creating one locally. Defaults to None.  # noQA: E501 line too long, pylint: disable=line-too-long  # noQA: E501 line too long, pylint: disable=line-too-long  # noQA: E501 line too long,

    :param email: Get the user from the database
    :param url: str: Pass the url of the avatar to be updated
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url  # type: ignore
    db.commit()
    return user


async def reset_password(email: str, new_password: str, db: Session):
    """
    The reset_password function resets a user's password.

    Args:
        email (str): The user's email address.
        new_password (str): The new password to set for the user.
        db (Session): A database session object, used to commit changes.

    :param email: str: Identify the user whose password is to be reset
    :param new_password: str: Set the new password for the user
    :param db: Session: Pass the database session to the function
    :return: Nothing, but the type hint says it returns a user
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.password = new_password  # type: ignore
    user.password_needs_reset = False  # type: ignore
    db.commit()


async def make_password_needs_reset(email: str, db: Session):
    """
    The make_password_needs_reset function sets the password_needs_reset flag to True for a user with the given email.
        Args:
            email (str): The user's email address.
            db (Session): A database session object.

    :param email: str: Get the user's email address
    :param db: Session: Access the database
    :return: Nothing
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.password_needs_reset = True  # type: ignore
    db.commit()
