import csv
from backtesting_module import get_symbol_price

# Функция для сохранения символов и их цен в CSV
def save_symbols_to_csv(symbols):
    with open('bybit_symbols.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['symbol', 'price'])  # Добавляем заголовки: символ и цена

        for symbol in symbols:
            price_data = get_symbol_price(symbol)  # Получаем цену для каждого символа
            if price_data:
                price = price_data['price']
                writer.writerow([symbol, price])  # Сохраняем символ и его цену
            else:
                writer.writerow([symbol, 'N/A'])  # Если цену не удалось получить, записываем 'N/A'

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
    for asset in symbols:
        if asset['symbol'] == symbol:
            print(f'Пара {symbol} найдена. Цена: {asset["price"]}')
            return True
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
