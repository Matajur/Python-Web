from bson.objectid import ObjectId

from django import template

from utils.connection_mongo import db

register = template.Library()


def get_author(id_):
    author = db.authors.find_one({"_id": ObjectId(id_)})
    if author is not None:
        return author["fullname"]


register.filter("author", get_author)
