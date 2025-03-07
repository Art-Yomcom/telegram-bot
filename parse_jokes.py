import requests
import pandas as pd

def parse_jokes(url):
    response = requests.get(url)
    jokes = response.text.split("\n\n")  # Разделение анекдотов по пустой строке
    jokes = [joke.strip() for joke in jokes if joke.strip()]  # Убираем лишние пробелы
    return jokes

def add_jokes_to_csv(category, jokes, filename="anekdoty.csv"):
    try:
        df = pd.read_csv(filename)  # Читаем существующий CSV
    except FileNotFoundError:
        df = pd.DataFrame(columns=["category", "text"])  # Если файла нет, создаём новый

    new_jokes = [{"category": category, "text": joke} for joke in jokes]

    df = pd.concat([df, pd.DataFrame(new_jokes)], ignore_index=True)  # Добавляем новые анекдоты
    df.to_csv(filename, index=False)  # Записываем обратно в CSV

# Парсим анекдоты Вовочки
url_vovochka = "https://lib.ru/ANEKDOTY/wowochka.txt"
vovochka_jokes = parse_jokes(url_vovochka)
add_jokes_to_csv("Вовочка", vovochka_jokes)

# Парсим анекдоты Штирлица
url_shtirlic = "https://lib.ru/ANEKDOTY/vonstir.txt"
shtirlic_jokes = parse_jokes(url_shtirlic)
add_jokes_to_csv("Штирлиц", shtirlic_jokes)

# Парсим анекдоты Чукчи
url_chukcha = "https://lib.ru/ANEKDOTY/chukcha.txt"
chukcha_jokes = parse_jokes(url_chukcha)
add_jokes_to_csv("Чукча", chukcha_jokes)
