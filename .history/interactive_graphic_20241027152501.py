import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Пример создания данных для графика
# В реальности данные можно загружать с помощью API биржи, например, используя Binance API или другой источник

# Генерация случайных данных для демонстрации
dates = pd.date_range('2023-10-01', periods=100)
prices = pd.DataFrame(index=dates)
prices['Открытие'] = np.random.uniform(low=100, high=200, size=100)
prices['Максимум'] = prices['Открытие'] + np.random.uniform(low=1, high=10, size=100)
prices['Минимум'] = prices['Открытие'] - np.random.uniform(low=1, high=10, size=100)
prices['Закрытие'] = np.random.uniform(low=100, high=200, size=100)
prices['Объем'] = np.random.randint(low=1000, high=10000, size=100)

# Создаем график с использованием Plotly для более интерактивного опыта, включая перетаскивание и масштабирование
fig = go.Figure()

# Добавляем свечи на график
fig.add_trace(go.Candlestick(
    x=prices.index,
    open=prices['Открытие'],
    high=prices['Максимум'],
    low=prices['Минимум'],
    close=prices['Закрытие'],
    name='Свечи'
))

# Добавляем скользящие средние
prices['Скользящая_средняя_20'] = prices['Закрытие'].rolling(window=20).mean()
prices['Скользящая_средняя_50'] = prices['Закрытие'].rolling(window=50).mean()

fig.add_trace(go.Scatter(
    x=prices.index,
    y=prices['Скользящая_средняя_20'],
    mode='lines',
    line=dict(color='blue', dash='dash'),
    name='Скользящая средняя 20'
))

fig.add_trace(go.Scatter(
    x=prices.index,
    y=prices['Скользящая_средняя_50'],
    mode='lines',
    line=dict(color='red'),
    name='Скользящая средняя 50'
))

# Настраиваем внешний вид графика
fig.update_layout(
    title='Интерактивный торговый график',
    xaxis_title='Дата',
    yaxis_title='Цена',
    template='plotly_dark',  # Стиль графика, можно выбрать другой (например, 'plotly', 'ggplot2', 'seaborn')
    xaxis_rangeslider_visible=False,  # Отключение нижнего слайдера
    figratio=(16, 9),
    figscale=1.2
)

# Отображение графика
fig.show()
