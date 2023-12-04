from datetime import datetime

from .db import session
from .models import Discipline, Grade, Group, Professor, Student


def discipline_handler(args):
    action = args.get("action").lower()
    match action:
        case "create":
            item = Discipline(
                name=args.get("name"), professor_id=args.get("professor_id")
            )
            session.add(item)
        case "list":
            items = session.query(Discipline).all()
            for i in items:
                print(i.id, i.name)
        case "update":
            item = session.query(Discipline).filter(Discipline.id == args.get("id"))
            item.update({"name": args.get("name")})
        case "remove":
            session.query(Discipline).filter(Discipline.id == args.get("id")).delete()
    session.commit()
    session.close()


def grade_handler(args):
    action = args.get("action").lower()
    match action:
        case "create":
            item = Grade(
                grade=args.get("name"),
                date_of=datetime.strptime(args.get("date"), "%Y-%m-%d").date(),
                student_id=args.get("student_id"),
                discipline_id=args.get("discipline_id"),
            )
            session.add(item)
        case "list":
            items = session.query(Grade).all()
            for i in items:
                print(i.id, i.grade, i.date_of, i.student_id, i.discipline_id)
        case "update":
            item = session.query(Grade).filter(Grade.id == args.get("id"))
            item.update(
                {
                    "grade": args.get("name"),
                    "date_of": datetime.strptime(args.get("date"), "%Y-%m-%d").date(),
                    "student_id": args.get("student_id"),
                    "discipline_id": args.get("discipline_id"),
                }
            )
        case "remove":
            session.query(Grade).filter(Grade.id == args.get("id")).delete()
    session.commit()
    session.close()


def group_handler(args):
    action = args.get("action").lower()
    match action:
        case "create":
            item = Group(name=args.get("name"))
            session.add(item)
        case "list":
            items = session.query(Group).all()
            for i in items:
                print(i.id, i.name)
        case "update":
            item = session.query(Group).filter(Group.id == args.get("id"))
            item.update({"name": args.get("name")})
        case "remove":
            session.query(Group).filter(Group.id == args.get("id")).delete()
    session.commit()
    session.close()


def professor_handler(args):
    action = args.get("action").lower()
    match action:
        case "create":
            item = Professor(fullname=args.get("name"))
            session.add(item)
        case "list":
            items = session.query(Professor).all()
            for i in items:
                print(i.id, i.fullname)
        case "update":
            item = session.query(Professor).filter(Professor.id == args.get("id"))
            item.update({"fullname": args.get("name")})
        case "remove":
            session.query(Professor).filter(Professor.id == args.get("id")).delete()
    session.commit()
    session.close()


def student_handler(args):
    action = args.get("action").lower()
    match action:
        case "create":
            item = Student(fullname=args.get("name"), group_id=args.get("group_id"))
            session.add(item)
        case "list":
            items = session.query(Student).all()
            for i in items:
                print(i.id, i.fullname, i.group_id)
        case "update":
            item = session.query(Student).filter(Student.id == args.get("id"))
            item.update(
                {"fullname": args.get("name"), "group_id": args.get("group_id")}
            )
        case "remove":
            session.query(Student).filter(Student.id == args.get("id")).delete()
    session.commit()
    session.close()
