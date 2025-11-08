import argparse

# --- Налаштування CLI-парсера ---
def parse_args():
    parser = argparse.ArgumentParser(description="Університетська база даних (CLI через argparse)")

    # Аргумент для дії: create, list, update, remove
    parser.add_argument(
        "-a", "--action",
        required=True,
        help="Дія: create, list, update, remove"
    )

    # Аргумент для моделі: Student, Teacher, Group, Subject, Grade
    parser.add_argument(
        "-m", "--model",
        required=True,
        help="Модель: Student, Teacher, Group, Subject, Grade"
    )

    # Необов’язкові аргументи для додаткових параметрів
    parser.add_argument("--id", type=int, help="ID запису (для update/remove)")
    parser.add_argument("-n", "--name", help="Назва або ім'я (для create/update)")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print("Отримані аргументи:", args)
