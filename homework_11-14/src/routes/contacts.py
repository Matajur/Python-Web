from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.repository import contacts as rep_contacts
from src.schemas import ContactModel, ContactResponse
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix="/contacts", tags=["contacts"])


allowed_oper_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_oper_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_oper_update = RoleAccess([Role.admin, Role.moderator])
allowed_oper_remove = RoleAccess([Role.admin])


@router.get(
    "/",
    response_model=List[ContactResponse],
    name="Get contacts",
    dependencies=[Depends(allowed_oper_get), Depends(RateLimiter(times=2, seconds=5))],
)
async def get_contacts(
    limit: int = Query(default=10, le=500, ge=5),  # type: ignore
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_contacts function returns a list of contacts.
        The limit and offset parameters are used to paginate the results.


    :param limit: int: Limit the number of contacts returned
    :param le: Limit the number of contacts returned to 500
    :param ge: Set a minimum value for the limit parameter
    :param offset: int: Set the offset of the query
    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :param : Limit the number of contacts returned
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await rep_contacts.get_contacts(db, limit, offset)
    return contacts


@router.get(
    "/advanced_search",
    response_model=List[ContactResponse],
    name="Get contacts: advanced search",
    dependencies=[Depends(allowed_oper_get), Depends(RateLimiter(times=2, seconds=5))],
)
async def get_contacts_advanced(
    limit: int = Query(default=10, le=500, ge=5),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
    cont_name: str | None = None,
    cont_thurname: str | None = None,
    cont_email: str | None = None,
):
    """
    The get_contacts_advanced function is a more advanced version of the get_contacts function.
    It allows you to search for contacts by name, thurname or email.
    If no parameters are given it will return all contacts in the database.

    :param limit: int: Limit the number of contacts returned
    :param le: Limit the maximum value of a parameter
    :param ge: Specify the minimum value for a parameter
    :param offset: int: Skip the first n contacts
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :param cont_name: str | None: Filter the contacts by name
    :param cont_thurname: str | None: Filter the contacts by thurname
    :param cont_email: str | None: Get a contact by email
    :param : Limit the number of contacts returned by the query
    :return: A list of contacts
    :doc-author: Trelent
    """
    if cont_name is not None:
        contacts = await rep_contacts.get_contacts_by_name(db, cont_name, limit, offset)
    elif cont_thurname is not None:
        contacts = await rep_contacts.get_contacts_by_thurname(
            db, cont_thurname, limit, offset
        )
    elif cont_email is not None:
        contacts = await rep_contacts.get_contact_by_email(db, cont_email)  # type: ignore
    else:
        contacts = await rep_contacts.get_contacts(db, limit, offset)
    return contacts


@router.get(
    "/next_birthdays",
    response_model=List[ContactResponse],
    name="Get next birthdays",
    dependencies=[Depends(allowed_oper_get), Depends(RateLimiter(times=2, seconds=5))],
)
async def get_next_birthdays(
    limit: int = Query(default=10, le=500, ge=5),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_next_birthdays function returns a list of contacts whose birthdays are within the next 7 days.
    The function takes in an optional limit and offset parameter, which can be used to paginate through the results.


    :param limit: int: Limit the number of contacts returned
    :param le: Limit the number of results returned
    :param ge: Set a minimum value for the limit parameter
    :param offset: int: Skip the first n records
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :param : Limit the number of results returned by the function
    :return: A list of contacts that have a birthday within the next 7 days
    :doc-author: Trelent
    """
    today = datetime.today().date()
    contacts = await rep_contacts.get_contacts(db, limit, offset)
    result = []
    for contact in contacts:
        if contact.birthday is not None:
            date_of_birth = contact.birthday
            date_this_year = date_of_birth.replace(year=today.year)
            if date_this_year < today:
                date_this_year = date_this_year.replace(year=today.year + 1)
            days_to_birthday = (date_this_year - today).days
            if days_to_birthday <= 7:
                result.append(contact)
    return result


@router.get(
    "/{cont_id}",
    response_model=ContactResponse,
    name="Get Contact by ID",
    dependencies=[Depends(allowed_oper_get), Depends(RateLimiter(times=2, seconds=5))],
)
async def get_contact(
    cont_id: int = Path(description="The ID of the contact to get", ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_contact function returns a contact by ID.

    :param cont_id: int: Get the id of the contact to be returned
    :param ge: Ensure that the contact id is greater than or equal to 1
    :param db: Session: Pass in the database session that is created by the get_db function
    :param current_user: User: Check if the user is logged in
    :param : Get the contact id from the url
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await rep_contacts.get_contact_by_id(db, cont_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact Not Found"
        )
    return contact


@router.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(allowed_oper_create),
        Depends(RateLimiter(times=1, seconds=10)),
    ],
)
async def create_contact(
    body: ContactModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_contact function creates a new contact in the database.
        The function takes an email, phone number and name as input parameters.
        If the contact already exists, it will return a 409 error code with an appropriate message.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :param : Pass the body of the request to the function
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact_by_email = await rep_contacts.get_contact_by_email(db, body.email)
    contact_by_phone = await rep_contacts.get_contact_by_phone(db, body.phone)
    if contact_by_email or contact_by_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact with this email or phone number already exists",
        )
    contact = await rep_contacts.contact_create(db, body)
    return contact


@router.delete(
    "/{cont_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(allowed_oper_remove),
        Depends(RateLimiter(times=1, seconds=5)),
    ],
    description="Only admin",
)
async def remove_contact(
    cont_id: int = Path(description="The ID of the contact to delete", ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The remove_contact function deletes a contact from the database.

    :param cont_id: int: Pass the contact id to the function
    :param ge: Ensure that the contact id is greater than or equal to 1
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :param : Get the id of the contact to delete
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await rep_contacts.contact_remove(db, cont_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.put(
    "/{cont_id}",
    response_model=ContactResponse,
    dependencies=[
        Depends(allowed_oper_update),
        Depends(RateLimiter(times=1, seconds=10)),
    ],
    description="Only moderator and admin",
)
async def update_contact(
    body: ContactModel,
    cont_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_contact function updates a contact in the database.
        The function takes an id and a body as input, and returns the updated contact.
        If no such contact exists, it raises an HTTPException with status code 404.

    :param body: ContactModel: Pass the json payload to the function
    :param cont_id: int: Get the id of the contact to be updated
    :param db: Session: Pass the database connection to the repository function
    :param current_user: User: Get the current user from the database
    :param : Get the contact id from the url
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await rep_contacts.contact_update(db, cont_id, body)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
