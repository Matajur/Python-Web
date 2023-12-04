import pickle
from datetime import datetime, timedelta
from typing import Optional

import redis
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer  # Bearer token
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.conf import messages
from src.conf.config import settings
from src.database.db import get_db
from src.repository import users as rep_users


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    rds = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def verify_password(
        self, plain_password, hashed_password
    ):  # not async def, because no overations with db
        """
        The verify_password function takes a plain-text password and a hashed password,
        and returns True if the passwords match, False otherwise.


        :param self: Represent the instance of the class
        :param plain_password: Verify the password that is entered by the user
        :param hashed_password: Store the hashed password in the database
        :return: A boolean value
        :doc-author: Trelent
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        The get_password_hash function takes a password as input and returns the hash of that password.
            The function uses the pwd_context object to generate a hash from the given password.

        :param self: Represent the instance of the class
        :param password: str: Pass the password to be hashed
        :return: A hash of the password
        :doc-author: Trelent
        """
        return self.pwd_context.hash(password)

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        The create_access_token function creates a new access token.
            Args:
                data (dict): The data to be encoded in the JWT.
                expires_delta (Optional[float]): A timedelta object representing how long the token should last for. Defaults to 60 minutes if not specified.

        :param self: Represent the instance of the class
        :param data: dict: Pass the data to be encoded
        :param expires_delta: Optional[float]: Set the expiration time of the token
        :return: An encoded access token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_access_token

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        The create_refresh_token function creates a refresh token for the user.
            Args:
                data (dict): The data to be encoded in the JWT. This should include at least a username and an email address, but can also include other information such as roles or permissions.
                expires_delta (Optional[float]): The number of seconds until this token expires, defaults to 7 days if not specified.

        :param self: Represent the instance of the class
        :param data: dict: Pass the data that will be encoded in the token
        :param expires_delta: Optional[float]: Specify the time of expiration
        :return: An encoded refresh token
        :doc-author: Trelent
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"}
        )
        encoded_refresh_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        The decode_refresh_token function is used to decode the refresh token.
            The function will raise an HTTPException if the token is invalid or has expired.
            If the token is valid, it will return a string with the email address of
            user who owns that refresh_token.

        :param self: Represent the instance of a class
        :param refresh_token: str: Pass the refresh token to the function
        :return: The email of the user who has a valid refresh token
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=messages.INVALID_SCOPE_TOKEN,
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=messages.INVALID_CREDENTIALS,
            )

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        """
        The get_current_user function is a dependency that will be used in the
            protected endpoints. It takes a token as an argument and returns the user
            if it's valid, otherwise raises an HTTPException with status code 401.

        :param self: Represent the instance of the class
        :param token: str: Get the token from the authorization header
        :param db: Session: Get the database session
        :return: An object of type user
        :doc-author: Trelent
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.INVALID_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == "access_token":
                email = payload.get("sub")
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        # user = await rep_users.get_user_by_email(email, db)
        user = self.rds.get(f"user:{email}")
        if user is None:
            user = await rep_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.rds.set(f"user:{email}", pickle.dumps(user))
            self.rds.expire(f"user:{email}", 900)  # 900 sec - remains in cash
        else:
            user = pickle.loads(user)  # type: ignore

        if user is None:
            raise credentials_exception
        return user

    def create_email_token(self, data: dict):
        """
        The create_email_token function creates a token that is used to verify the user's email address.
            The token contains the following data:
                - iat (issued at): The time when the token was created.
                - exp (expiration): When this token will expire and no longer be valid. This is set to 7 days from creation time.
                - scope: What this JWT can be used for, in this case it's an email_token which means it can only be used for verifying emails.

        :param self: Represent the instance of the class
        :param data: dict: Pass in the data that will be encoded into the token
        :return: A token that is used to verify the user's email address
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"}
        )
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    def create_reset_token(self, data: dict):
        """
        The create_reset_token function creates a token that is used to reset user's password.
            The token contains the following data:
                - iat (issued at): The time when the token was created.
                - exp (expiration): When this token will expire and no longer be valid. This is set to 7 days from creation time.
                - scope: What this JWT can be used for, in this case it's an email_token which means it can only be used for verifying emails.

        :param self: Represent the instance of the class
        :param data: dict: Pass in the data that will be encoded into the token
        :return: A token that is used to verify the user's email address
        :doc-author: Trelent
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "reset_token"}
        )
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    def get_email_from_token(self, token: str):
        """
        The get_email_from_token function takes a token as an argument and returns the email associated with that token.
        If the scope of the token is not &quot;email_token&quot;, then it raises an HTTPException. If there is a JWTError, then it also raises an HTTPException.

        :param self: Represent the instance of the class
        :param token: str: Pass in the token that we want to decode
        :return: The email from a token
        :doc-author: Trelent
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "email_token":
                email = payload["sub"]
                return email
            elif payload["scope"] == "reset_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=messages.INVALID_SCOPE_TOKEN,
            )
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=messages.INVALID_TOKEN,
            )


auth_service = Auth()
