import argparse
from sqlalchemy.orm import sessionmaker
from db import engine
from models import Teacher, Group, Student, Subject, Grade

Session = sessionmaker(bind=engine)
session = Session()

def create_teacher(name):
    teacher = Teacher(fullname=name)
    session.add(teacher)
    session.commit()
    print(f"✅ Викладача '{name}' створено (id={teacher.id})")

def list_teachers():
    teachers = session.query(Teacher).all()
    for t in teachers:
        print(f"{t.id}. {t.fullname}")

def update_teacher(id, name):
    teacher = session.get(Teacher, id)
    if teacher:
        teacher.fullname = name
        session.commit()
        print(f"Викладача id={id} оновлено на '{name}'")
    else:
        print("Викладача не знайдено")

def remove_teacher(id):
    teacher = session.get(Teacher, id)
    if teacher:
        session.delete(teacher)
        session.commit()
        print(f"Викладача id={id} видалено")
    else:
        print("Викладача не знайдено")

def main():
    parser = argparse.ArgumentParser(description="University CLI")
    parser.add_argument("-a", "--action", required=True, help="CRUD action: create, list, update, remove")
    parser.add_argument("-m", "--model", required=True, help="Model name: Teacher, Group, Student, Subject, Grade")
    parser.add_argument("--id", type=int, help="Object ID (for update/remove)")
    parser.add_argument("-n", "--name", help="Name or full name")

    args = parser.parse_args()

    if args.model == "Teacher":
        if args.action == "create":
            create_teacher(args.name)
        elif args.action == "list":
            list_teachers()
        elif args.action == "update":
            update_teacher(args.id, args.name)
        elif args.action == "remove":
            remove_teacher(args.id)
        else:
            print("Невідома дія")

if __name__ == "__main__":
    main()
