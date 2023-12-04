from psycopg2 import DatabaseError

from db_connection import connection

create_table_disciplines = """
-- Table: disciplines
DROP TABLE IF EXISTS disciplines CASCADE;
CREATE TABLE disciplines (
  id SERIAL PRIMARY KEY,
  name VARCHAR(30),
  professor_id INTEGER REFERENCES professors (id)
);
"""

create_table_grades = """
-- Table: grades
DROP TABLE IF EXISTS grades CASCADE;
CREATE TABLE grades (
  id SERIAL PRIMARY KEY,
  student_id INTEGER REFERENCES students (id),
  discipline_id INTEGER REFERENCES disciplines (id),
  date_of DATE NOT NULL,
  grade INTEGER NOT NULL
);
"""

create_table_groups = """
-- Table: groups
DROP TABLE IF EXISTS groups CASCADE;
CREATE TABLE groups (
  id SERIAL PRIMARY KEY,
  name VARCHAR(10) UNIQUE NOT NULL
);
"""

create_table_professors = """
-- Table: professors
DROP TABLE IF EXISTS professors CASCADE;
CREATE TABLE professors (
  id SERIAL PRIMARY KEY,
  fullname VARCHAR(30),
  email VARCHAR(30) UNIQUE NOT NULL
);
"""

create_table_students = """
-- Table: students
DROP TABLE IF EXISTS students CASCADE;
CREATE TABLE students (
  id SERIAL PRIMARY KEY,
  fullname VARCHAR(30),
  email VARCHAR(30) UNIQUE NOT NULL,
  age NUMERIC CHECK (age > 16 AND age < 51),
  group_id INTEGER REFERENCES groups (id)
);
"""


def create_table(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
        c.close()
    except DatabaseError as err:
        print(err)


if __name__ == "__main__":
    with connection() as conn:
        if conn is not None:
            create_table(conn, create_table_groups)
            create_table(conn, create_table_students)
            create_table(conn, create_table_professors)
            create_table(conn, create_table_disciplines)
            create_table(conn, create_table_grades)
