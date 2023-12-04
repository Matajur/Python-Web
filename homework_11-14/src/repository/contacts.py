from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(db: Session, limit: int, offset: int):
    """
    The get_contacts function returns a list of contacts from the database.


    :param db: Session: Pass the database session to the function
    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip before starting to return rows
    :return: A list of contact objects
    :doc-author: Trelent
    """
    contacts = db.query(Contact).limit(limit).offset(offset).all()  # pagination
    return contacts


async def get_contact_by_id(db: Session, cont_id: int):
    """
    The get_contact_by_id function returns a contact object from the database based on its id.


    :param db: Session: Pass the database connection to the function
    :param cont_id: int: Filter the query by id
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(id=cont_id).first()
    return contact


async def get_contact_by_name(db: Session, cont_name: str):
    """
    The get_contact_by_name function returns a contact object from the database based on the name of that contact.
        Args:
            db (Session): The database session to use for querying.
            cont_name (str): The name of the contact to retrieve from the database.
        Returns:
            Contact: A single Contact object matching cont_name, or None if no such Contact exists in our DB.

    :param db: Session: Connect to the database
    :param cont_name: str: Filter the database by name
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(email=cont_name).first()
    return contact


async def get_contacts_by_name(db: Session, cont_name: str, limit: int, offset: int):
    """
    The get_contacts_by_name function returns a list of contacts with the given name.


    :param db: Session: Connect to the database
    :param cont_name: str: Filter the query by name
    :param limit: int: Limit the number of results returned
    :param offset: int: Specify the number of records to skip before starting to return rows
    :return: A list of contacts
    :doc-author: Trelent
    """
    contact = (
        db.query(Contact).filter_by(email=cont_name).limit(limit).offset(offset).all()
    )
    return contact


async def get_contact_by_thurname(db: Session, cont_thurname: str):
    """
    The get_contact_by_thurname function returns a contact object from the database based on the thurname of that contact.
        Args:
            db (Session): The SQLAlchemy session to use for querying.
            cont_thurname (str): The thurname of the desired contact.
        Returns:
            Contact: A single Contact object matching the given thurname, or None if no such user exists.

    :param db: Session: Pass in the database session
    :param cont_thurname: str: Filter the query by thurname
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(email=cont_thurname).first()
    return contact


async def get_contacts_by_thurname(
    db: Session, cont_thurname: str, limit: int, offset: int
):
    """
    The get_contacts_by_thurname function returns a list of contacts with the given thurname.
        Args:
            db (Session): The database session to use for querying.
            cont_thurname (str): The thurname to search for in the database.
            limit (int): Limit on how many results are returned from the query. Defaults to 100 if not specified by user, or is set higher than 100 by user input.

    :param db: Session: Create a database session
    :param cont_thurname: str: Filter the results by thurname
    :param limit: int: Limit the number of results returned by the query
    :param offset: int: Skip the first offset number of rows
    :return: A list of contact objects
    :doc-author: Trelent
    """
    contact = (
        db.query(Contact)
        .filter_by(email=cont_thurname)
        .limit(limit)
        .offset(offset)
        .all()
    )
    return contact


async def get_contact_by_email(db: Session, cont_email: str):
    """
    The get_contact_by_email function returns a contact object from the database based on the email address provided.
        Args:
            db (Session): The SQLAlchemy session object.
            cont_email (str): The email address of the contact to be retrieved from the database.
        Returns:
            Contact: A single Contact object matching cont_email, or None if no match is found.

    :param db: Session: Pass the database session to the function
    :param cont_email: str: Filter the database by email
    :return: A single contact by email
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(email=cont_email).first()
    return contact


async def get_contact_by_phone(db: Session, cont_phone: str):
    """
    The get_contact_by_phone function returns a contact object from the database based on the phone number provided.
        Args:
            db (Session): The SQLAlchemy session to use for querying.
            cont_phone (str): The phone number of the contact to retrieve from the database.
        Returns:
            Contact: A single Contact object matching cont_phone, or None if no match is found.

    :param db: Session: Pass the database session to the function
    :param cont_phone: str: Filter the database query by phone number
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(email=cont_phone).first()
    return contact


async def contact_create(db: Session, body: ContactModel):
    """
    The contact_create function creates a new contact in the database.


    :param db: Session: Pass the database session to the function
    :param body: ContactModel: Create a new contact
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def contact_remove(db: Session, cont_id: int):
    """
    The contact_remove function removes a contact from the database.


    :param db: Session: Pass the database session to the function
    :param cont_id: int: Identify the contact that is to be removed from the database
    :return: The contact that was deleted
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(db, cont_id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def contact_update(db: Session, cont_id: int, body: ContactModel):
    """
    The contact_update function updates a contact in the database.
        Args:
            db (Session): The database session to use for this function.
            cont_id (int): The id of the contact to update.
            body (ContactModel): A ContactModel object containing all of the information needed to update a contact.

    :param db: Session: Pass the database session to the function
    :param cont_id: int: Identify the contact that is being updated
    :param body: ContactModel: Pass the data from the request body to this function
    :return: A contactmodel
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(db, cont_id)  # type: ignore
    if contact:
        contact.name = body.name  # type: ignore
        contact.thurname = body.thurname  # type: ignore
        contact.email = body.email  # type: ignore
        contact.phone = body.phone  # type: ignore
        contact.notes = body.notes  # type: ignore
        db.commit()
    return contact
