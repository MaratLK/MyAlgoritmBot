import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf

# Пример создания данных для графика
# В реальности данные можно загружать с помощью API биржи, например, используя Binance API или другой источник

dates = pd.date_range('2023-10-01', periods=100)
prices = pd.DataFrame(index=dates)
prices['Open'] = np.random.uniform(low=100, high=200, size=100)
prices['High'] = prices['Open'] + np.random.uniform(low=1, high=10, size=100)
prices['Low'] = prices['Open'] - np.random.uniform(low=1, high=10, size=100)
prices['Close'] = np.random.uniform(low=100, high=200, size=100)
prices['Volume'] = np.random.randint(low=1000, high=10000, size=100)

# Используем mplfinance для создания удобного и стильного графика, похожего на TradingView
# Основной акцент будет на кастомизации вида графика и его красоте

mpf.plot(
    prices,
    type='candle',
    style='yahoo',  # Можно выбрать стиль или создать свой собственный, например, white, nightclouds, yahoo
    title='Trading Chart',
    ylabel='Price',
    volume=True,    # Отображение объема, как на TradingView
    ylabel_lower='Volume',
    figratio=(16, 9),  # Соотношение сторон графика для удобства
    figscale=1.2,   # Масштаб для улучшенной читаемости
)

# Если нужно, можно создать дополнительные индикаторы, например, среднюю скользящую
prices['SMA_20'] = prices['Close'].rolling(window=20).mean()
prices['SMA_50'] = prices['Close'].rolling(window=50).mean()

# Добавляем на график индикаторы
mpf.plot(
    prices,
    type='candle',
    style='yahoo',
    title='Trading Chart with Moving Averages',
    ylabel='Price',
    volume=True,
    ylabel_lower='Volume',
    figratio=(16, 9),
    figscale=1.2,
    addplot=[
        mpf.make_addplot(prices['SMA_20'], color='blue', linestyle='--'),
        mpf.make_addplot(prices['SMA_50'], color='red', linestyle='-')
    ]
)

plt.show()
