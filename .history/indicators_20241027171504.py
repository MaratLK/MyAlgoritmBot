def calculate_aroon(data, period=14):
    # Находим индекс максимума и минимума за заданный период
    high_period = data['high'].rolling(window=period, min_periods=1).apply(lambda x: x.argmax(), raw=True)  #7
    low_period = data['low'].rolling(window=period, min_periods=1).apply(lambda x: x.argmin(), raw=True)  #8
    
    # Переводим индексы в числовой формат
    days_since_high = period - (period - high_period).astype(int)  #9
    days_since_low = period - (period - low_period).astype(int)  #10
    
    # Рассчитываем Aroon Up и Aroon Down
    aroon_up = ((period - days_since_high) / period) * 100  #11 Расчет силы восходящего тренда
    aroon_down = ((period - days_since_low) / period) * 100  #12 Расчет силы нисходящего тренда
    
    return aroon_up, aroon_down