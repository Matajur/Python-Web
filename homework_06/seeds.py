from random import randint, sample

from db_connection import connection
from faker import Faker
from psycopg2 import DatabaseError

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


def seed_disciplines(cur):
    sql = """
    INSERT INTO disciplines(name, professor_id) VALUES(%s, %s);
    """
    for i in range(NUMBER_DISCIPLINES):
        cur.execute(sql, (DISCIPLINES[i], randint(1, NUMBER_PROFESSORS)))


def seed_grades(cur):
    sql = """
    INSERT INTO grades(student_id, discipline_id, date_of, grade) VALUES(%s, %s, %s, %s);
    """
    for i in range(NUMBER_STUDENTS * NUMBER_DISCIPLINES * 15):
        cur.execute(
            sql,
            (
                randint(1, NUMBER_STUDENTS),
                randint(1, NUMBER_DISCIPLINES),
                fake.date_between(start_date="-1y", end_date="now"),
                randint(1, 10),
            ),
        )


def seed_groups(cur):
    sql = """
    INSERT INTO groups(name) VALUES(%s);
    """
    for i in range(NUMBER_GROUPS):
        cur.execute(sql, (f"group {i+1}",))


def seed_professors(cur):
    sql = """
    INSERT INTO professors(fullname, email) VALUES(%s, %s);
    """
    for i in range(NUMBER_PROFESSORS):
        cur.execute(sql, (fake.name(), fake.email()))


def seed_students(cur):
    sql = """
    INSERT INTO students(fullname, email, age, group_id) VALUES(%s, %s, %s, %s);
    """
    for i in range(NUMBER_STUDENTS):
        cur.execute(
            sql, (fake.name(), fake.email(), randint(17, 50), randint(1, NUMBER_GROUPS))
        )


if __name__ == "__main__":
    with connection() as conn:
        try:
            if conn is not None:
                cur = conn.cursor()
                seed_groups(cur)
                seed_students(cur)
                seed_professors(cur)
                seed_disciplines(cur)
                seed_grades(cur)
                cur.close()
        except DatabaseError as err:
            print(err)
