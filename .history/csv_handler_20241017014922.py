import csv


def save_symbols_to_csv(symbols):
    with open('bybit_symbols.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['symbol'])
        for symbol in symbols:
            writer.writerow([symbol])

# Функция для загрузки символов из CSV
def load_symbols_from_csv(file_path='bybit_symbols.csv'):
    symbols = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbols.append(row['symbol'])
    except FileNotFoundError:
        print(f'Файл {file_path} не найден. Убедитесь, что файл существует.')
    return symbols

# Функция для поиска символа
def search_symbol_in_csv(symbol, file_path='bybit_symbols.csv'):
    symbols = load_symbols_from_csv(file_path)
    if symbol in symbols:
        print(f'Пара {symbol} найдена.')
        return True
    else:
        print(f'Пара {symbol} не найдена.')
        return False 

# Функция для интерактивного поиска и анализа
def interactive_search_and_analysis(file_path='bybit_symbols.csv'):
    symbol = input("Введите пару для анализа (например, BTCUSDT): ")

    # Проверяем, существует ли символ
    if search_symbol_in_csv(symbol, file_path):
        print(f'Теперь можно продолжить анализ для {symbol}.')
    else:
        print(f'Пара {symbol} не найдена. Попробуйте ввести другую.')
