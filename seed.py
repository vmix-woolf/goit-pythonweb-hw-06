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
session.query(Subject).delete()
session.query(Teacher).delete()
session.query(Group).delete()
session.commit()

# Групи
groups = [Group(name=f"Група {i}") for i in range(1, 4)]
session.add_all(groups)
session.commit()

# Викладачі
teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

# Предмети
subject_names = ["Математика", "Фізика", "Хімія", "Історія", "Інформатика", "Економіка"]
subjects = []
for i, name in enumerate(subject_names):
    subject = Subject(name=name, teacher_id=teachers[i % len(teachers)].id)
    subjects.append(subject)
session.add_all(subjects)
session.commit()

# Студенти
students = []
for _ in range(30):
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
    # Для кожного студента додаємо по 10 оцінок
    chosen_subjects = random.sample(subjects, k=min(5, len(subjects)))
    for _ in range(10):
        subject = random.choice(chosen_subjects)
        g = Grade(
            student_id=student.id,
            subject_id=subject.id,
            grade=random.randint(60, 100)
        )
        grades.append(g)

session.add_all(grades)
session.commit()

session.close()
print("✅ Базу даних успішно наповнено: 30 студентів, 10 оцінок на кожного!")
