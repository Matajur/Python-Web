from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    Security,
    status,
)
from fastapi_limiter.depends import RateLimiter
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from src.conf import messages
from src.database.db import get_db
from src.repository import users as rep_users
from src.schemas import RequestEmail, UserModel, UserResponse, TokenModel
from src.services.auth import auth_service
from src.services.email import send_verification_email, send_reset_password_email

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

# dependencies=[Depends(RateLimiter(times=1, seconds=10))],


@router.post(
    "/signup",
    response_model=UserResponse,  # type: ignore
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    body: UserModel,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    The signup function creates a new user in the database.
    It also sends an email to the user with a link to verify their account.


    :param body: UserModel: Get the data from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background queue
    :param request: Request: Get the base url of the application
    :param db: Session: Get the database session
    :param : Get the email address of the user who is signing up
    :return: A usermodel object
    :doc-author: Trelent
    """
    exist_user = await rep_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=messages.ACCOUNT_EXISTS
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await rep_users.create_user(body, db)  # type: ignore
    print(new_user)
    print(type(new_user.email))
    print(type(new_user.username))
    background_tasks.add_task(send_verification_email, new_user.email, new_user.username, str(request.base_url))  # type: ignore
    return new_user


# dependencies=[Depends(RateLimiter(times=1, seconds=10))],


@router.post(
    "/login",
    response_model=TokenModel,
)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    The login function is used to authenticate a user.
    It takes the username and password from the request body, verifies them against
    the database, and returns an access token if successful. The access token can be
    used in subsequent requests to verify that the user has been authenticated.

    :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: Session: Get the database session
    :return: A dictionary with the access_token, refresh_token and token type
    :doc-author: Trelent
    """
    user = await rep_users.get_user_by_email(body.username, db)
    # email is username for OAuth2PasswordRequestForm
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_EMAIL
        )
    if user.confirmed is False:  # if not user.confirmed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.EMAIL_NOT_VERIFIED
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_PASSWORD
        )
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await rep_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh_token", response_model=TokenModel)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    """
    The refresh_token function is used to refresh the access token.
        The function takes in a refresh token and returns an access_token,
        a new refresh_token, and the type of token (bearer).

    :param credentials: HTTPAuthorizationCredentials: Get the token from the request header
    :param db: Session: Create a connection to the database
    :param : Get the current user's email from the database
    :return: A dictionary with the following keys:
    :doc-author: Trelent
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await rep_users.get_user_by_email(email, db)
    if user.refresh_token != token:  # type: ignore
        await rep_users.update_token(user, None, db)  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_TOKEN_R
        )
    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await rep_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get(
    "/confirmed_email/{token}",
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    The confirmed_email function is used to confirm a user's email address.
        The function takes the token from the URL and uses it to get the user's email address.
        It then checks if that email exists in our database, and if so, confirms their account.

    :param token: str: Get the token from the url
    :param db: Session: Access the database
    :return: A dictionary with a message key and a value of email confirmed
    :doc-author: Trelent
    """
    email = auth_service.get_email_from_token(token)
    user = await rep_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=messages.VERIFICATION_ERROR
        )
    if user.confirmed is True:  # if user.confirmed
        return {"message": messages.EMAIL_CONFIRMED_ALREADY}
    await rep_users.confirmed_email(email, db)
    return {"message": messages.EMAIL_CONFIRMED}


@router.post(
    "/request_email",
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    The request_email function is used to send an email to the user with a link that will confirm their account.
        The function takes in the body of the request, which contains only one field: email. It then uses this email
        address to find a user in our database and check if they have already confirmed their account or not. If they
        have, we return a message saying so; otherwise, we add another task (send_verification_email) to our background tasks queue
        and return another message.

    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base_url of the request
    :param db: Session: Pass the database session to the repository layer
    :param : Send the email to the user
    :return: The following:
    :doc-author: Trelent
    """
    user = await rep_users.get_user_by_email(body.email, db)
    if user:
        if user.confirmed is True:  # if user.confirmed
            return {"message": messages.EMAIL_CONFIRMED_ALREADY}
        background_tasks.add_task(send_verification_email, user.email, user.username, str(request.base_url))  # type: ignore
    return {"message": messages.CHECK_EMAIL}


@router.post(
    "/reset_password", dependencies=[Depends(RateLimiter(times=1, seconds=10))]
)
async def request_password_reset(
    body: RequestEmail, request: Request, db: Session = Depends(get_db)
):
    """
    The request_password_reset function is used to send a password reset email to the user.
        The function takes in an email address and sends a password reset link to that address.
        If the user does not exist, or if they have not confirmed their account, no action is taken.

    :param body: RequestEmail: Get the email from the request body
    :param request: Request: Get the base url of the server
    :param db: Session: Pass the database session to the function
    :return: A dictionary with a message key
    :doc-author: Trelent
    """
    user = await rep_users.get_user_by_email(body.email, db)
    if user:
        if user.confirmed is True:  # if user.confirmed
            await send_reset_password_email(
                user.email, user.username, str(request.base_url)  # type: ignore
            )
    return {"message": messages.CHECK_EMAIL}


@router.get(
    "/reset_password/{reset_token}",
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def confirm_password_reset(reset_token: str, db: Session = Depends(get_db)):
    """
    The confirm_password_reset function is used to confirm that a user has requested a password reset.
    It takes the reset token as an argument and returns a message indicating that the user can now set their new password.

    :param reset_token: str: Get the email from the token
    :param db: Session: Get the database session
    :return: A dict with a message
    :doc-author: Trelent
    """
    email = auth_service.get_email_from_token(reset_token)
    user = await rep_users.get_user_by_email(email, db)
    print(user.username)  # type: ignore
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=messages.VERIFICATION_ERROR
        )
    await rep_users.make_password_needs_reset(email, db)
    return {"message": messages.NEW_PASSWORD}


@router.put(
    "/reset_password/{reset_token}",
    dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def reset_password(
    reset_token: str, new_password: str, db: Session = Depends(get_db)
):
    """
    The reset_password function is used to reset a user's password.
        It takes in the reset_token, which is sent to the user via email, and a new_password.
        The function then checks if the token has expired or not by checking if it matches with an existing email address in our database.
        If it does match, we check that this particular user's password needs to be reset (this field will be set when they request for their password to be changed).
        If both of these conditions are met, we hash their new_password and update our database with this information.

    :param reset_token: str: Get the email from the token
    :param new_password: str: Get the new password from the user
    :param db: Session: Get the database session from the dependency injection
    :return: A dictionary with a message key and the value is password_reset
    :doc-author: Trelent
    """
    email = auth_service.get_email_from_token(reset_token)
    user = await rep_users.get_user_by_email(email, db)
    if user.password_needs_reset == True:  # type: ignore
        new_password = auth_service.get_password_hash(new_password)
        await rep_users.reset_password(email, new_password, db)
        return {"message": messages.PASSWORD_RESET}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=messages.VERIFICATION_ERROR
    )
