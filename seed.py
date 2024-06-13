import random
from datetime import datetime

import sqlalchemy
from faker import Faker

from db import session
from models import Group, Student, Teacher, Discipline, Grade, Base

fake = Faker()

disciplines = [
    "History",
    "Geometry",
    "Algebra",
    "English",
    "Physics",
    "Chemistry",
    "Biology"
]

groups = [
    "G11",
    "G12",
    "G13"
]

def clear_tables(session):
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
        sequence_name = f"{table.name}_id_seq"
        stmt = sqlalchemy.text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1")
        session.execute(stmt)
    session.commit()
    session.close()

def create_fake_data(session):
    # Teachers
    for _ in range(5):
        name = f"{fake.first_name()} {fake.last_name()}"
        teacher = Teacher(full_name = name)
        session.add(teacher)
        
    # Groups
    for i in groups:
        session.add(Group(group_name=i))

    t_id_list = []
    for t in session.query(Teacher).all():
        t_id_list.append(t.id)

    # Disceplines
    for i in disciplines:
        discipline = Discipline(name=i, teachers_id=random.choice(t_id_list))
        session.add(discipline)

    # Students
    for _ in range(50):
        student = Student(full_name = f"{fake.first_name()} {fake.last_name()}",
                            group_id=random.choice([i.id for i in session.query(Group).all()]))
        session.add(student)

    # Grades
    get_students = session.query(Student).all()
    get_disciplines = session.query(Discipline).all()

    for _ in get_students:
        for _ in range(random.randint(1,20)):
            random_discipline = random.choice(get_disciplines)
            grade = Grade(grade=random.randint(1, 5),
                        date=fake.date_between_dates(date_start=datetime(2024,1,1),
                                                    date_end=datetime(2024,5,1)),
                        student_id=random.choice(get_students).id,
                        discipline_id=random_discipline.id)
                        
            session.add(grade)

    session.commit()
    session.close()

if __name__=="__main__":
    clear_tables(session)
    create_fake_data(session)
