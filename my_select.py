from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from db import engine
from models import Student, Group, Teacher, Subject, Grade

Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    return (
        session.query(Student.fullname, func.round(func.avg(Grade.grade), 2))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )

def select_2(subject_name):
    return (
        session.query(Student.fullname, func.round(func.avg(Grade.grade), 2))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(1)
        .all()
    )

def select_3(subject_name: str):
    return (
        session.query(
            Group.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Group)
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .all()
    )

def select_4():
    return session.query(func.round(func.avg(Grade.grade), 2)).scalar()

def select_5(teacher_name):
    return (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.fullname == teacher_name)
        .all()
    )

def select_6(group_name):
    return (
        session.query(Student.fullname)
        .join(Group)
        .filter(Group.name == group_name)
        .all()
    )

def select_7(group_name, subject_name):
    return (
        session.query(Student.fullname, Grade.grade)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )

def select_8(teacher_name):
    return (
        session.query(func.round(func.avg(Grade.grade), 2))
        .join(Subject, Subject.id == Grade.subject_id)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Teacher.fullname == teacher_name)
        .scalar()
    )

def select_9(student_name):
    return (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.fullname == student_name)
        .distinct()
        .all()
    )

def select_10(student_name, teacher_name):
    return (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Teacher, Teacher.id == Subject.teacher_id)
        .filter(Student.fullname == student_name, Teacher.fullname == teacher_name)
        .distinct()
        .all()
    )

# --- Дополнительные запросы ---
def select_11():
    return (
        session.query(Teacher.fullname, func.round(func.avg(Grade.grade), 2))
        .join(Subject, Subject.teacher_id == Teacher.id)
        .join(Grade, Grade.subject_id == Subject.id)
        .group_by(Teacher.fullname)
        .order_by(func.avg(Grade.grade).desc())
        .all()
    )

def select_12():
    return (
        session.query(Subject.name, func.count(Grade.id))
        .join(Grade, Grade.subject_id == Subject.id)
        .group_by(Subject.name)
        .order_by(func.count(Grade.id).desc())
        .limit(1)
        .first()
    )

def select_13():
    subquery = (
        session.query(Grade.student_id)
        .group_by(Grade.student_id)
        .having(func.min(Grade.grade) > 70)
        .subquery()
    )
    return (
        session.query(Student.fullname)
        .join(subquery, Student.id == subquery.c.student_id)
        .all()
    )

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

    print("11. Середній бал кожного викладача:", select_11())
    print("12. Найпопулярніший предмет:", select_12())
    print("13. Студенти, які мають лише оцінки вище 70:", select_13())

    session.close()

