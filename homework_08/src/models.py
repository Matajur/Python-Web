from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import (
    EmbeddedDocumentField,
    ListField,
    ReferenceField,
    StringField,
    BooleanField,
)


class Tag(EmbeddedDocument):
    name = StringField(max_length=20, required=True)


class Author(Document):
    fullname = StringField(max_length=120, required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Author, reverse_delete_rule=2)
    quote = StringField()
    meta = {"allow_inheritance": True}


class Contact(Document):
    fullname = StringField(max_length=120, required=True)
    email = StringField()
    phone = StringField()
    status = BooleanField(default=False)
