from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from .db import Base, engine


class Discipline(Base):
    __tablename__ = "disciplines"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    professor_id = Column(
        ForeignKey("professors.id", ondelete="CASCADE"), nullable=False
    )
    professor = relationship("Professor", backref="disciplines")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column(Date, nullable=False)
    student_id = Column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    discipline_id = Column(
        ForeignKey("disciplines.id", ondelete="CASCADE"), nullable=False
    )
    student = relationship("Student", backref="grades")
    discipline = relationship("Discipline", backref="grades")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)


class Professor(Base):
    __tablename__ = "professors"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False, unique=True)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False)
    group_id = Column(ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    group = relationship("Group", backref="students")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
