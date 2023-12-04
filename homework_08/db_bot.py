from src.cacher import cache
from src.connection import session
from src.models import Author, Quote


def matcher(command, arg):
    match command:
        case "name":
            name_search(arg)
        case "tag":
            tag_search(arg)
        case "tags":
            tags_search(arg)
        case _:
            print(f"Unknown command '{command}")


@cache
def name_search(arg):
    ids = {}
    authors = Author.objects(fullname__icontains=arg)
    for author in authors:
        ids.update({author.fullname: author.id})
    if len(ids) == 0:
        print(f"No quotes for author '{arg}'")
    else:
        for key, val in ids.items():
            print(f"Printing quotes of '{key}':")
            quotes = Quote.objects(author=val)
            for quote in quotes:
                print(quote.quote)


@cache
def tag_search(arg):
    quotes = Quote.objects(tags__name__icontains=arg)
    if quotes:
        for quote in quotes:
            tgs = []
            for tag in quote.tags:
                tgs.append(tag.name)
            print(f"Tags list for request '{arg}': {tgs}")
            print(quote.quote)
    else:
        print(f"No quotes for tag '{arg}'")


@cache
def tags_search(arg):
    args = arg.strip().split(",")
    quotes = Quote.objects(tags__name__in=args)
    if quotes:
        for quote in quotes:
            tgs = []
            for tag in quote.tags:
                tgs.append(tag.name)
            print(f"Tags list for request '{arg}': {tgs}")
            print(quote.quote)
    else:
        print(f"No quotes for tags '{arg}'")


if __name__ == "__main__":
    while True:
        try:
            inp = input("Insert command ('name', 'tag', 'tags', 'exit') [exit]: ")
            if inp == "exit" or inp == "":
                break
            else:
                command, arg = inp.split(":")
                if arg == "":
                    print(f"Missing argument after the command '{inp}'")
                else:
                    matcher(command.strip(), arg.strip())
        except ValueError as err:
            print(f"Wrong input '{inp}', should be 'command: argument' or type 'exit'")
