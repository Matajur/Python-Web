import argparse

from src.crud import (
    discipline_handler,
    grade_handler,
    group_handler,
    professor_handler,
    student_handler,
)

SUPPORTED_COMMANDS = ("create", "list", "update", "remove")

"""
python cli.py -a create -m Student -n 'John Snow' -gr 3
"""

parser = argparse.ArgumentParser(description="University database handling application")
parser.add_argument("-a", "--action", help="Comand: create, list, update, remove")
parser.add_argument(
    "-m", "--model", help="Model: Discipline, Grade, Group, Professor, Student"
)
parser.add_argument(
    "-n",
    "--name",
    help="'Name' for Discipline or Group, 'Fullname' for Professor or Student, 'Value' for Grade",
)
parser.add_argument("-id", "--id", help="ID of item to be changed or deleted")
parser.add_argument("-c", "--column", help="Name of a column to be modified")
parser.add_argument("-dis", "--discipline_id", help="Discipline ID as a foreign key")
parser.add_argument("-gr", "--group_id", help="Group ID as a foreign key")
parser.add_argument("-pr", "--professor_id", help="Professor ID as a foreign key")
parser.add_argument("-st", "--student_id", help="Student ID as a foreign key")
parser.add_argument("-d", "--date", help="Date of the grade in format 'YYYY-MM-DD'")

args = vars(parser.parse_args())

action = args.get("action").lower()


def main(model):
    match model:
        case "discipline":
            discipline_handler(args)
        case "grade":
            grade_handler(args)
        case "group":
            group_handler(args)
        case "professor":
            professor_handler(args)
        case "student":
            student_handler(args)
        case _:
            print("Unknown model, try help to see supported models")


if __name__ == "__main__":
    if action in SUPPORTED_COMMANDS:
        if args.get("model"):
            main(model=args.get("model").lower())
        else:
            print("Missing model name, try help to see supported models")
    else:
        print("Unknown command, try help to see supported commands")
