from datetime import date
from random import randint, sample

from faker import Faker

from models import Discipline, Grade, Group, Professor, Student
from db import session

NUMBER_STUDENTS = randint(30, 50)
NUMBER_GROUPS = 3
NUMBER_DISCIPLINES = randint(5, 8)
NUMBER_PROFESSORS = randint(3, 5)
NUMBER_GRADES = 20
OPTIONS = (
    "accounting",
    "alchemy",
    "astronomy",
    "herbology",
    "homepathy",
    "potions",
    "transfiguration",
    "set teory",
)
DISCIPLINES = sample(OPTIONS, k=NUMBER_DISCIPLINES)

fake = Faker()


def seed_disciplines():
    for disc in DISCIPLINES:
        discipline = Discipline(name=disc, professor_id=randint(1, NUMBER_PROFESSORS))
        session.add(discipline)
    session.commit()


def seed_grades():
    for i in range(NUMBER_STUDENTS * NUMBER_DISCIPLINES * 15):
        grade = Grade(
            grade=randint(1, 10),
            date_of=fake.date_between(
                start_date=date(2022, 9, 1), end_date=date(2023, 5, 30)
            ),
            student_id=randint(1, NUMBER_STUDENTS),
            discipline_id=randint(1, NUMBER_DISCIPLINES),
        )
        session.add(grade)
    session.commit()


def seed_groups():
    for i in range(NUMBER_GROUPS):
        group = Group(name=f"group-{i+1}")
        session.add(group)
    session.commit()


def seed_professors():
    for i in range(NUMBER_PROFESSORS):
        professor = Professor(fullname=fake.name())
        session.add(professor)
    session.commit()


def seed_students():
    for i in range(NUMBER_STUDENTS):
        student = Student(
            fullname=fake.name(),
            group_id=randint(1, NUMBER_GROUPS),
        )
        session.add(student)
    session.commit()


if __name__ == "__main__":
    seed_groups()
    seed_students()
    seed_professors()
    seed_disciplines()
    seed_grades()
