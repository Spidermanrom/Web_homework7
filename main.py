import sys
from db import session
from models import Student, Discipline, Teacher, Grade, Group
from sqlalchemy import func, desc


def select_1():
    print("Завдання: Знайти 5 студентів із найбільшим середнім балом з усіх предметів")
    field_names = ['full_name', 'grade']
    data = session.query(Student.full_name,  func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return *field_names, *data


def select_2():
    print(f"Завдання: Знайти студента із найвищим середнім балом з певного предмета.\n{session.query(Discipline.name).all()}")
    subject = input('Введіть назву предмета: ')
    field_names = ['full_name', 'discipline', 'grade']
    data = session.query(Student.full_name,
                        Discipline.name,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                        .select_from(Student).join(Grade, Student.id == Grade.id)\
                        .join(Discipline, Discipline.id == Grade.discipline_id)\
                        .filter(Discipline.name==subject).group_by(Student.full_name, Discipline.name)\
                        .order_by(desc('avg_grade')).limit(1).all()
    return field_names, data

def select_3():
    print(f"Завдання: Знайти середній бал у групах з певного предмета.\n{session.query(Discipline).all()}")
    subject = input('Введіть назву предмета: ')
    field_names = ['name', 'discipline', 'grade']
    data = session.query(Group.group_name,
                        Discipline.name,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                        .select_from(Group).join(Student, Student.group_id == Group.id)\
                        .join(Grade, Student.id == Grade.id)\
                        .join(Discipline, Discipline.id == Grade.discipline_id)\
                        .filter(Discipline.name==subject).group_by(Group.group_name, Discipline.name)\
                        .order_by(desc('avg_grade')).all()
    return field_names, data

def select_4():
    print("Завдання: Знайти середній бал на потоці (по всій таблиці оцінок).")
    field_names = ['group_name', 'grade']
    data = session.query(Group.group_name,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                        .select_from(Group).join(Student, Student.group_id == Group.id)\
                        .join(Grade, Student.id == Grade.discipline_id)\
                        .group_by(Group.group_name)\
                        .order_by(desc('avg_grade')).all()
    return field_names, data

def select_5():
    print("Завдання: Знайти які курси читає певний викладач.")
    print(session.query(Teacher).all())
    teacher_full_name = input('Введіть ім\'я та прізвище викладача: ')
    field_names = ['teacher_name', 'discipline']
    data = session.query(Teacher.full_name, Discipline.name)\
                        .select_from(Discipline).join(Teacher, Discipline.id == Teacher.id)\
                        .filter(Teacher.full_name==teacher_full_name)\
                        .order_by(Teacher.full_name).all()
    return field_names, data

def select_6():
    print(f"Завдання: Знайти список студентів у певній групі.\n{session.query(Group.group_name).all()}")
    group_num = input('Введіть номер групи: ')
    field_names = ['group', 'full_name']
    data = session.query(Group.group_name, Student.full_name)\
                        .select_from(Group).join(Student, Student.group_id == Group.id)\
                        .filter(Group.group_name==group_num)\
                        .order_by(Student.full_name).all()
    return field_names, data

def select_7():
    print(f"Завдання: Знайти оцінки студентів у окремій групі з певного предмета.\n{session.query(Group.group_name).all()}")
    group_num = input('Введіть номер групи: ')
    print(session.query(Discipline).all())
    subject = input('Введіть назву предмета: ')
    field_names = ['group', 'full_name', 'discipline', 'grade', 'date']
    data = session.query(Group.group_name, Student.full_name, Discipline.name, Grade.grade, Grade.date)\
                        .select_from(Grade).join(Student, Student.id == Grade.id)\
                        .join(Discipline, Discipline.id == Grade.id)\
                        .join(Group, Student.group_id == Group.id)\
                        .filter(Group.group_name==group_num, Discipline.name==subject)\
                        .order_by(Student.full_name).all()
    return field_names, data

def select_8():
    print(f"Завдання: Знайти середній бал, який ставить певний викладач зі своїх предметів.\n{session.query(Teacher.full_name).all()}")
    teacher_full_name = input('Введіть ім\'я та прізвище викладача: ')
    field_names = ['full_name', 'discipline', 'grade']
    data = session.query(Teacher.full_name,
                        Discipline.name,
                        func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                        .select_from(Grade).join(Discipline, Discipline.id == Grade.id)\
                        .join(Teacher, Discipline.id == Teacher.id)\
                        .filter(Teacher.full_name == teacher_full_name)\
                        .group_by(Teacher.full_name, Discipline.name).order_by(Discipline.name).all()
    return field_names, data

def select_9():
    print("Завдання: Знайти список курсів, які відвідує студент.")
    student_full_name = input('Введіть ім\'я та прізвище студента: ')
    field_names = ['full_name', 'discipline']
    data = session.query(Student.full_name,
                        Discipline.name)\
                        .select_from(Student).join(Grade, Student.id == Grade.id)\
                        .join(Discipline, Grade.id == Discipline.id)\
                        .filter(Student.full_name==student_full_name)\
                        .group_by(Student.full_name, Discipline.name).order_by(Discipline.name).all()
    return field_names, data

def select_10():
    print("Завдання: Список курсів, які певному студенту читає певний викладач.")
    s_full_name = input('Введіть ім\'я та прізвище студента: ')
    print(session.query(Teacher.full_name).all())
    t_full_name = input('Введіть ім\'я та прізвище викладача: ')
    field_names = [ 'studnet full_name',
                   'teacher full_name',
                   'discipline']
    
    data = session.query(Student.full_name,
                        Teacher.full_name,
                        Discipline.name)\
                        .select_from(Student).join(Grade, Student.id == Grade.id)\
                        .join(Discipline, Grade.id == Discipline.id)\
                        .join(Teacher, Discipline.id== Teacher.id)\
                        .filter(Student.full_name==s_full_name,
                                Teacher.full_name==t_full_name)\
                        .group_by(Student.full_name,
                                    Teacher.full_name,
                                    Discipline.name).all()
    return field_names, data

def exit():
    print('Good bye')
    sys.exit()

selects = {
    '0': exit,
    '1': select_1,
    '2': select_2,
    '3': select_3,
    '4': select_4,
    '5': select_5,
    '6': select_6,
    '7': select_7,
    '8': select_8,
    '9': select_9,
    '10': select_10
}
help = {
    '0': 'Вихід',
    '1': 'Знайти 5 студентів із найбільшим середнім балом з усіх предметів',
    '2': 'Знайти студента із найвищим середнім балом з певного предмета.',
    '3': 'Знайти середній бал у групах з певного предмета.',
    '4': 'Знайти середній бал на потоці (по всій таблиці оцінок).',
    '5': 'Знайти які курси читає певний викладач.',
    '6': 'Знайти список студентів у певній групі.',
    '7': 'Знайти оцінки студентів у окремій групі з певного предмета.',
    '8': 'Знайти середній бал, який ставить певний викладач зі своїх предметів.',
    '9': 'Знайти список курсів, які відвідує студент.',
    '10': 'Список курсів, які певному студенту читає певний викладач.'
}

help_str = ''
for key, value in help.items():
    help_str += '{} -> {}\n'.format(key, value)

def get_handler(user_input):
    return selects.get(user_input)

def main():
    print(help_str)
    while True:
        user_input = input('>>> ')
        handler = get_handler(user_input)
        try:
            result = handler()
            print(result)
        except TypeError:
            print(f'Не знайома команда! Виберіть зі списку команд: \n')
            print(help_str)


if __name__ == '__main__':
    main()