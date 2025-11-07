from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from db import engine
from models import Student, Group, Teacher, Subject, Grade

Session = sessionmaker(bind=engine)
session = Session()


# 1. Топ-5 студентів за середнім балом
def select_1():
    result = (
        session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return result


# 2. Найкращий студент з певного предмета
def select_2(subject_name):
    result = (
        session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
        .all()
    )
    return result


# 3. Середній бал у кожній групі з певного предмета
def select_3(subject_name):
    result = (
        session.query(Group.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Student)
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .all()
    )
    return result


# 4. Середній бал по всіх оцінках
def select_4():
    result = session.query(func.round(func.avg(Grade.grade), 2)).scalar()
    return result


# 5. Курси, які веде певний викладач
def select_5(teacher_name):
    result = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.fullname == teacher_name)
        .all()
    )
    return result


# 6. Список студентів у певній групі
def select_6(group_name):
    result = (
        session.query(Student.fullname)
        .join(Group)
        .filter(Group.name == group_name)
        .all()
    )
    return result


# 7. Оцінки студентів певної групи з певного предмета
def select_7(group_name, subject_name):
    result = (
        session.query(Student.fullname, Grade.grade)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return result


# 8. Середній бал, який ставить певний викладач
def select_8(teacher_name):
    result = (
        session.query(Teacher.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Subject)
        .join(Grade)
        .filter(Teacher.fullname == teacher_name)
        .group_by(Teacher.fullname)
        .first()
    )
    return result


# 9. Курси, які відвідує певний студент
def select_9(student_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.fullname == student_name)
        .distinct()
        .all()
    )
    return result


# 10. Курси, які певний студент слухає у певного викладача
def select_10(student_name, teacher_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.fullname == student_name, Teacher.fullname == teacher_name)
        .distinct()
        .all()
    )
    return result


if __name__ == "__main__":
    print("1. Топ-5 студентів:", select_1())
    print("2. Найкращий студент з предмета 'Хімія':", select_2("Хімія"))
    print("3. Середній бал у групах з предмета 'Хімія':", select_3("Хімія"))
    print("4. Середній бал по потоку:", select_4())

    first_teacher = session.query(Teacher.fullname).first()[0]
    first_student = session.query(Student.fullname).first()[0]

    print(f"5. Курси викладача '{first_teacher}':", select_5(first_teacher))
    print("6. Студенти групи 'Група 1':", select_6("Група 1"))
    print("7. Оцінки студентів групи 'Група 1' з предмета 'Хімія':", select_7("Група 1", "Хімія"))
    print(f"8. Середній бал викладача '{first_teacher}':", select_8(first_teacher))
    print(f"9. Курси, які відвідує студент '{first_student}':", select_9(first_student))
    print(f"10. Курси, які студент '{first_student}' слухає у викладача '{first_teacher}':",
          select_10(first_student, first_teacher))

session.close()
