import unittest
from datetime import date
from pydantic_extra_types.phone_numbers import PhoneNumber
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact_by_id,
    get_contact_by_name,
    get_contacts_by_name,
    contact_create,
    contact_remove,
    contact_update,
)


class TestRepositoryContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(__spec__=Session)
        self.contact_1 = Contact(
            id=1,
            name="Ivan",
            thurname="Ivanchenko",
            email="test_1@meta.ua",
            phone=PhoneNumber("+380991234567"),
            birthday=date(2000, 1, 30),
            notes="hello world!",
        )
        self.contact_2 = Contact(
            id=2,
            name="Ivan",
            thurname="Petrenko",
            email="test_2@meta.ua",
            phone=PhoneNumber("+380992345678"),
            birthday=date(2000, 10, 14),
            notes="oh my god!",
        )

    # get_contacts

    async def test_get_contacts(self):
        contacts = [self.contact_1, self.contact_2]
        self.session.query(Contact).limit().offset().all.return_value = contacts
        result = await get_contacts(db=self.session, limit=10, offset=0)  # type: ignore
        self.assertEqual(result, contacts)

    # contact_create

    async def test_contact_create(self):
        body = ContactModel(
            name="Ivan",
            thurname="Ivanchenko",
            email="test@meta.ua",
            phone=PhoneNumber("+380991234567"),
            birthday=date(2000, 1, 30),
            notes="hello world!",
        )
        result = await contact_create(db=self.session, body=body)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.thurname, body.thurname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.notes, body.notes)
        self.assertTrue(hasattr(result, "id"))  # if result has attribute ID

    # get_contact_update

    async def test_contact_update_found(self):
        body = ContactModel(
            name="Petro",
            thurname="Ivanchenko",
            email="test@meta.ua",
            phone=PhoneNumber("+380991234567"),
            birthday=date(2000, 1, 30),
            notes="hello world!",
        )
        self.session.query(Contact).filter_by().first.return_value = self.contact_1
        self.session.commit.return_value = None
        result = await contact_update(db=self.session, cont_id=self.contact_1.id, body=body)  # type: ignore
        self.assertEqual(result.name, body.name)  # type: ignore

    async def test_contact_update_not_found(self):
        body = ContactModel(
            name="Petro",
            thurname="Ivanchenko",
            email="test@meta.ua",
            phone=PhoneNumber("+380991234567"),
            birthday=date(2000, 1, 30),
            notes="hello world!",
        )
        self.session.query(Contact).filter_by().first.return_value = None
        self.session.commit.return_value = None
        result = await contact_update(db=self.session, cont_id=self.contact_1.id, body=body)  # type: ignore
        self.assertIsNone(result)

    # get_contact_remove

    async def test_contact_remove_found(self):
        self.session.query(Contact).filter_by().first.return_value = self.contact_1
        result = await contact_remove(db=self.session, cont_id=self.contact_1.id)  # type: ignore
        self.assertEqual(result, self.contact_1)

    async def test_contact_remove_not_found(self):
        self.session.query(Contact).filter_by().first.return_value = None
        result = await contact_remove(db=self.session, cont_id=self.contact_1.id)  # type: ignore
        self.assertIsNone(result)

    # get_contact_by_id

    async def test_get_contact_by_id_found(self):
        self.session.query(Contact).filter_by().first.return_value = self.contact_1
        result = await get_contact_by_id(db=self.session, cont_id=self.contact_1.id)  # type: ignore
        self.assertEqual(result, self.contact_1)

    async def test_get_contact_by_id_not_found(self):
        self.session.query(Contact).filter_by().first.return_value = None
        result = await get_contact_by_id(db=self.session, cont_id=self.contact_1.id)  # type: ignore
        self.assertIsNone(result)

    # get_contact_by_name

    async def test_get_contact_by_name_found(self):
        self.session.query(Contact).filter_by().first.return_value = self.contact_1
        result = await get_contact_by_name(db=self.session, cont_name=self.contact_1.name)  # type: ignore
        self.assertEqual(result, self.contact_1)

    async def test_get_contact_by_name_not_found(self):
        self.session.query(Contact).filter_by().first.return_value = None
        result = await get_contact_by_name(db=self.session, cont_name=self.contact_1.name)  # type: ignore
        self.assertIsNone(result)

    # get_contacts_by_name

    async def test_get_contacts_by_name_found(self):
        contacts = [self.contact_1, self.contact_2]
        self.session.query(
            Contact
        ).filter_by().limit().offset().all.return_value = contacts
        result = await get_contacts_by_name(db=self.session, cont_name=self.contact_1.name, limit=10, offset=0)  # type: ignore
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_name_not_found(self):
        self.session.query(Contact).filter_by().limit().offset().all.return_value = None
        result = await get_contacts_by_name(db=self.session, cont_name=self.contact_1.name, limit=10, offset=0)  # type: ignore
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
