import csv

def save_symbols_to_csv(symbols):
    with open('bybit_symbols.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['symbol'])
        for symbol in symbols:
            writer.writerow([symbol])

def load_symbols_from_csv():
    symbols = []
    with open('bybit_symbols.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            symbols.append(row['symbol'])
    return symbols

def search_symbol_in_csv(symbol):
    symbols = load_symbols_from_csv()
    if symbol in symbols:
        print(f'Пара {symbol} найдена.')
    else:
        print(f'Пара {symbol} не найдена.')
