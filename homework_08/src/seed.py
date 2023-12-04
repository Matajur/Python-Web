import json

from connection import session
from models import Tag, Author, Quote

file_authors = "src/authors.json"
file_quotes = "src/quotes.json"


def seed_authors(file):
    refs = {}
    with open(file, "r") as fh:
        authors = json.load(fh)
    for atr in authors:
        obj = Author(
            fullname=atr.get("fullname"),
            born_date=atr.get("born_date"),
            born_location=atr.get("born_location"),
            description=atr.get("description"),
        ).save()
        refs.update({obj.fullname: obj})
    return refs


def seed_quotes(file, refs):
    with open(file, "r") as fh:
        quots = json.load(fh)
    for qt in quots:
        tgs = qt.get("tags")
        tags = []
        for tg in tgs:
            tag = Tag(name=tg)
            tags.append(tag)
        atr = qt.get("author")
        author = refs.get(atr)
        Quote(tags=tags, author=author, quote=qt.get("quote")).save()


if __name__ == "__main__":
    refs = seed_authors(file_authors)
    seed_quotes(file_quotes, refs)
