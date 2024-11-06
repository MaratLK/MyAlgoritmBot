import ccxt
import pandas as pd
import matplotlib.pyplot as plt

# Инициализация Bybit через CCXT
exchange = ccxt.bybit({
    'enableRateLimit': True,
})

# Функция для получения свечных данных с Bybit
def fetch_candlestick_data(symbol='BTC/USDT', timeframe='1h', limit=10):
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    # Преобразуем данные в DataFrame
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Преобразуем время в читаемый формат
    return df

# Функция для построения графика свечей
def plot_candlestick(df):
    fig, ax = plt.subplots()
    
    for i in range(len(df)):
        # Цвет свечи
        color = 'green' if df['close'][i] >= df['open'][i] else 'red'
        
        # Рисуем тень
        ax.plot([i, i], [df['low'][i], df['high'][i]], color='black', linewidth=0.8)
        
        # Рисуем тело свечи
        ax.plot([i, i], [df['open'][i], df['close'][i]], color=color, linewidth=5)
    
    # Настройки графика
    ax.set_title(f'Candlestick Chart for {symbol}')
    ax.set_xlabel('Candle Number')
    ax.set_ylabel('Price')
    plt.show()

# Запрос данных и построение графика
symbol = 'BTC/USDT'
df = fetch_candlestick_data(symbol=symbol, timeframe='1h', limit=10)
plot_candlestick(df)
