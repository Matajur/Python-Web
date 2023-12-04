from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import users as rep_users
from src.services.auth import auth_service
from src.services.cloud_image import CloudImage
from src.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function returns the current user's information.
        ---
        get:
          tags: [users] # This is a tag that can be used to group operations by resources or any other qualifier.
          summary: Returns the current user's information.
          description: Returns the current user's information based on their JWT token in their request header.
          responses: # The possible responses this operation can return, along with descriptions and examples of each response type (if applicable).
            &quot;200&quot;:  # HTTP status code 200 indicates success! In this case, it means we successfully returned a User

    :param current_user: User: Get the current user
    :return: The current user
    :doc-author: Trelent
    """
    return current_user


@router.patch("/avatar", response_model=UserResponse)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The new avatar image to be uploaded.
            current_user (User): The user whose avatar is being updated.
            db (Session): A database session for interacting with the database.

    :param file: UploadFile: Get the file from the request body
    :param current_user: User: Get the current user
    :param db: Session: Pass the database session to the repository layer
    :param : Get the current user
    :return: An object of the user type
    :doc-author: Trelent
    """
    public_id = CloudImage.generate_avatar_name(current_user.email)  # type: ignore
    r = CloudImage.upload(public_id, file.file)
    src_url = CloudImage.get_ulr_4_avatar(public_id, r)
    user = await rep_users.update_avatar(current_user.email, src_url, db)  # type: ignore
    return user
