import argparse
from sqlalchemy.orm import sessionmaker
from db import engine
from models import Student, Teacher, Group, Subject, Grade

# --- Ініціалізація сесії ---
Session = sessionmaker(bind=engine)
session = Session()

# --- CRUD-функції ---
def create_record(model, **kwargs):
    fields = {c.name for c in model.__table__.columns}
    valid_kwargs = {k: v for k, v in kwargs.items() if k in fields and v is not None}
    obj = model(**valid_kwargs)
    session.add(obj)
    session.commit()
    print(f"{model.__name__} створено з ID={obj.id}")

def list_records(model):
    records = session.query(model).all()
    if not records:
        print("Таблиця порожня")
        return
    for r in records:
        if hasattr(r, "fullname"):
            print(f"{r.id}. {r.fullname}")
        elif hasattr(r, "name"):
            print(f"{r.id}. {r.name}")
        else:
            print(f"{r.id}. (без назви)")

def update_record(model, id, **kwargs):
    obj = session.get(model, id)
    if obj:
        fields = {c.name for c in model.__table__.columns}
        for key, value in kwargs.items():
            if key in fields and value is not None:
                setattr(obj, key, value)
        session.commit()
        print(f"{model.__name__} ID={id} оновлено")
    else:
        print("Запис не знайдено")

def remove_record(model, id):
    obj = session.get(model, id)
    if obj:
        session.delete(obj)
        session.commit()
        print(f"🗑️  {model.__name__} ID={id} видалено")
    else:
        print("Запис не знайдено")

# --- Маппінг моделей ---
MODELS = {
    "Student": Student,
    "Teacher": Teacher,
    "Group": Group,
    "Subject": Subject,
    "Grade": Grade,
}

# --- CLI логіка ---
def main():
    parser = argparse.ArgumentParser(description="University database CLI")
    parser.add_argument("-a", "--action", required=True, help="Дія: create, list, update, remove")
    parser.add_argument("-m", "--model", required=True, help="Модель: Student, Teacher, Group, Subject, Grade")
    parser.add_argument("--id", type=int, help="ID запису (для update/remove)")
    parser.add_argument("-n", "--name", help="Назва або повне ім’я (для create/update)")
    args = parser.parse_args()

    model = MODELS.get(args.model)
    if not model:
        print("Невідома модель")
        return

    if args.action == "create":
        create_record(model, fullname=args.name, name=args.name)
    elif args.action == "list":
        list_records(model)
    elif args.action == "update":
        update_record(model, args.id, fullname=args.name, name=args.name)
    elif args.action == "remove":
        remove_record(model, args.id)
    else:
        print("Невідома дія")

if __name__ == "__main__":
    main()
