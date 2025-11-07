from faker import Faker
import random
from sqlalchemy.orm import sessionmaker
from db import engine
from models import Base, Group, Student, Teacher, Subject, Grade

fake = Faker("uk_UA")
Session = sessionmaker(bind=engine)
session = Session()

# Очищення таблиць
session.query(Grade).delete()
session.query(Student).delete()
session.query(Group).delete()
session.query(Subject).delete()
session.query(Teacher).delete()
session.commit()

# Групи
groups = [Group(name=f"Група {i}") for i in range(1, 4)]
session.add_all(groups)
session.commit()

# Викладачі
teachers = [Teacher(fullname=fake.name()) for _ in range(random.randint(3, 5))]
session.add_all(teachers)
session.commit()

# Предмети
subject_names = ["Математика", "Фізика", "Історія", "Інформатика", "Біологія", "Хімія", "Література", "Економіка"]
subjects = [
    Subject(
        name=random.choice(subject_names),
        teacher_id=random.choice(teachers).id
    )
    for _ in range(random.randint(5, 8))
]
session.add_all(subjects)
session.commit()

# Студенти
students = []
for _ in range(random.randint(30, 50)):
    s = Student(
        fullname=fake.name(),
        group_id=random.choice(groups).id
    )
    students.append(s)
session.add_all(students)
session.commit()

# Оцінки
grades = []
for student in students:
    for _ in range(random.randint(10, 20)):
        g = Grade(
            student_id=student.id,
            subject_id=random.choice(subjects).id,
            grade=random.randint(60, 100)
        )
        grades.append(g)
session.add(g)
session.commit()

session.close()

print("✅ Базу даних успішно наповнено тестовими даними!")
