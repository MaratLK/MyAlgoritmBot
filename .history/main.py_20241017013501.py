from bybit_api import get_all_bybit_symbols
from csv_handler import save_symbols_to_csv, search_symbol_in_csv

# Получаем все пары и сохраняем их в CSV
symbols = get_all_bybit_symbols()
save_symbols_to_csv(symbols)

# Пример поиска символа
search_symbol_in_csv('BTCUSDT')
