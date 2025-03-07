import csv
import random

def get_joke(category, csv_file="anekdoty.csv"):
    try:
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")  # Указываем разделитель
            jokes = [row["Анекдот"] for row in reader if row["Категория"] == category]  # Собираем все анекдоты категории
            if jokes:
                return random.choice(jokes)  # Возвращаем случайный анекдот
            else:
                return None  # Если анекдотов в категории нет
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None