import json
from bson.objectid import ObjectId

from utils.connection_mongo import db


def authors2mongodb():
    with open("utils/authors.json", "r", encoding="utf-8") as fd:
        authors = json.load(fd)

    for author in authors:
        db.authors.insert_one(
            {
                "fullname": author["fullname"],
                "born_date": author["born_date"],
                "born_location": author["born_location"],
                "description": author["description"],
            }
        )


def quotes2mongodb():
    with open("utils/quotes.json", "r", encoding="utf-8") as fd:
        quotes = json.load(fd)

    for quote in quotes:
        author = db.authors.find_one({"fullname": quote["author"]})
        if author:
            db.quotes.insert_one(
                {
                    "quote": quote["quote"],
                    "tags": quote["tags"],
                    "author": ObjectId(author["_id"]),
                }
            )


if __name__ == "__main__":
    authors2mongodb()
    quotes2mongodb()
