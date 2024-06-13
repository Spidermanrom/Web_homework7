from sqlalchemy import String, Integer, ForeignKey, DATE
from sqlalchemy.orm import ( 
    Mapped, 
    mapped_column, 
    relationship
    )

from db import Base

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_name: Mapped[str] = mapped_column(String(20))

class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50))

    def __repr__(self) -> str:
        return self.full_name

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50))
    group_id: Mapped[int] = mapped_column(ForeignKey(
        "groups.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    group_name: Mapped['Group'] = relationship('Group')

    def __repr__(self) -> str:
        return f"{self.id}, {self.full_name}"
    
class Discipline(Base):
    __tablename__ = "disciplines"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    teachers_id: Mapped[int] = mapped_column(ForeignKey(
        "teachers.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    # teacher: Mapped['Teacher'] = relationship(
    #     "Teacher", back_populates='disciplines')
    grade: Mapped['Grade'] = relationship(
        "Grade", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.id}, {self.name}"
    

class Grade(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grade: Mapped[int] = mapped_column()
    date: Mapped[str] = mapped_column(DATE)
    student_id: Mapped[int] = mapped_column(ForeignKey(
        'students.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    student: Mapped['Student'] = relationship("Student")
    discipline_id: Mapped[int] = mapped_column(ForeignKey(
        'disciplines.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    discipline: Mapped['Discipline'] = relationship(
        "Discipline", cascade="all, delete", overlaps="raitings") 

    def __repr__(self) -> str:
        return f"{self.id}, {self.grade}"
