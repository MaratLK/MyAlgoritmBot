from bybit_api import get_all_bybit_symbols
from csv_handler import interactive_search_and_analysis

# Получаем все пары с Bybit и сохраняем их в CSV
symbols = get_all_bybit_symbols()
save_symbols_to_csv(symbols)

# Запускаем программу с интерактивным вводом
interactive_search_and_analysis()