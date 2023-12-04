from sqlalchemy import func, desc, and_, select

from src.db import session
from src.models import Discipline, Grade, Group, Professor, Student


def select_01() -> list:
    """
    Знайти 5 студентів із найбільшим середнім балом зі всіх предметів.
    """
    result = (
        session.query(
            Student.fullname.label("student"),
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return result


def select_02(discipline_id: int) -> list:
    """
    Знайти студента із найвищим середнім балом з певного предмета.
    """
    result = (
        session.query(
            Discipline.name.label("discipline"),
            Student.fullname.label("student"),
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .filter(Discipline.id == discipline_id)
        .group_by(Student.id, Discipline.name)
        .order_by(desc("avg_grade"))
        .limit(1)
        .all()
    )
    return result


def select_03(discipline_id: int) -> list:
    """
    Знайти середній бал в групах з певного предмета.
    """
    result = (
        session.query(
            Discipline.name.label("discipline"),
            Group.name.label("group"),
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Group)
        .filter(Discipline.id == discipline_id)
        .group_by(Group.name, Discipline.name)
        .order_by(desc("avg_grade"))
        .all()
    )
    return result


def select_04() -> list:
    """
    Знайти середній бал на потоці (по всій таблиці оцінок).
    """
    result = (
        session.query(
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .all()
    )
    return result


def select_05(professor_id: int) -> list:
    """
    Знайти, які курси читає певний викладач.
    """
    result = (
        session.query(
            Professor.fullname.label("professor"),
            Discipline.name.label("discipline"),
        )
        .select_from(Discipline)
        .join(Professor)
        .filter(Professor.id == professor_id)
        .order_by(Discipline.name)
        .all()
    )
    return result


def select_06(group_id: int) -> list:
    """
    Знайти список студентів в певній групі.
    """
    result = (
        session.query(
            Group.name.label("group"),
            Student.fullname.label("student"),
        )
        .select_from(Student)
        .join(Group)
        .filter(Group.id == group_id)
        .order_by(Student.fullname)
        .all()
    )
    return result


def select_07(discipline_id: int, group_id: int) -> list:
    """
    Знайти оцінки студентів в окремій групі з певного предмета.
    """
    result = (
        session.query(
            Group.name.label("group"),
            Discipline.name.label("discipline"),
            Student.fullname.label("student"),
            Grade.grade,
            Grade.date_of,
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Group)
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id))
        .group_by("group", "discipline", "student", Grade.grade, Grade.date_of)
        .all()
    )
    return result


def select_08(professor_id: int) -> list:
    """
    Знайти середній бал, який ставить певний викладач зі своїх предметів.
    """
    result = (
        session.query(
            Professor.fullname.label("professor"),
            Discipline.name.label("discipline"),
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Discipline)
        .join(Professor)
        .filter(Professor.id == professor_id)
        .group_by(Professor.fullname, Discipline.name)
        .all()
    )
    return result


def select_09(student_id: int) -> list:
    """
    Знайти список курсів, які відвідує певний студент.
    """
    result = (
        session.query(
            Student.fullname.label("student"),
            Discipline.name.label("discipline"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .filter(Student.id == student_id)
        .group_by(Student.id, Discipline.name)
        .order_by(Discipline.name)
        .all()
    )
    return result


def select_10(student_id: int, professor_id: int) -> list:
    """
    Список курсів, які певному студенту читає певний викладач.
    """
    result = (
        session.query(
            Professor.fullname.label("professor"),
            Student.fullname.label("student"),
            Discipline.name.label("discipline"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Professor)
        .filter(and_(Student.id == student_id, Professor.id == professor_id))
        .group_by(Professor.fullname, Student.id, Discipline.name)
        .all()
    )
    return result


def select_11(professor_id: int, student_id: int) -> list:
    """
    Середній бал, який певний викладач ставить певному студентові.
    """
    result = (
        session.query(
            Professor.fullname.label("professor"),
            Student.fullname.label("student"),
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Professor)
        .filter(and_(Professor.id == professor_id, Student.id == student_id))
        .group_by(Professor.fullname, Student.id)
        .all()
    )
    return result


def select_12(discipline_id: int, group_id: int) -> list:
    """
    Оцінки студентів в певній групі з певного предмета на останньому занятті.
    """
    subquery = (
        select(func.max(Grade.date_of))
        .join(Student)
        .join(Group)
        .filter(and_(Grade.discipline_id == discipline_id, Group.id == group_id))
        .scalar_subquery()
    )
    result = (
        session.query(
            Group.name.label("group"),
            Discipline.name.label("discipline"),
            Grade.date_of.label("last_date"),
            Student.fullname.label("student"),
            Grade.grade,
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Group)
        .filter(
            and_(Discipline.id == discipline_id, Group.id == group_id),
            Grade.date_of == subquery,
        )
        .group_by("group", "discipline", "last_date", "student", Grade.grade)
        .all()
    )
    return result


if __name__ == "__main__":
    print("Selection 01", select_01())
    print("Selection 02", select_02(1))
    print("Selection 03", select_03(1))
    print("Selection 04", select_04())
    print("Selection 05", select_05(1))
    print("Selection 06", select_06(1))
    print("Selection 07", select_07(1, 1))
    print("Selection 08", select_08(1))
    print("Selection 09", select_09(1))
    print("Selection 10", select_10(1, 1))
    print("Selection 11", select_11(1, 1))
    print("Selection 12", select_12(1, 1))
