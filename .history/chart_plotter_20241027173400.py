import plotly.graph_objects as go
from indicators import calculate_aroon

def plot_chart(self):
        exchange_name = self.exchange_combo.currentText()  #61 Получение имени выбранной биржи
        symbol = self.pair_combo.currentText()  #62 Получение выбранной валютной пары
        timeframe = self.timeframe_combo.currentText()  #63 Получение выбранного таймфрейма
        chart_type = self.chart_type_combo.currentText()  #64 Получение типа графика

        # Получение данных и построение графика
        data = self.data_fetcher.fetch_data(exchange_name, symbol, timeframe)  #65 Получение данных для построения графика
        if data is not None:
            fig = go.Figure()  #66 Создание новой фигуры для графика

            if chart_type == "Candlestick":  #67 Если выбран тип "свечной график"
                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    name=symbol
                ))  #68 Добавление данных свечей в график
            elif chart_type == "Line":  #69 Если выбран линейный график
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['close'],
                    mode='lines',
                    name=symbol
                ))  #70 Добавление данных линии в график

            # Добавляем индикатор Арун, если включен
            if self.aroon_enabled:  #71 Проверка флага включения индикатора Арун
                aroon_up, aroon_down = calculate_aroon(data)  #72 Расчет значений Aroon Up и Aroon Down
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=aroon_up,
                    mode='lines',
                    name='Aroon Up',
                    line=dict(color='green', dash='dash')
                ))  #73 Добавление линии Aroon Up
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=aroon_down,
                    mode='lines',
                    name='Aroon Down',
                    line=dict(color='red', dash='dash')
                ))  #74 Добавление линии Aroon Down

            # Добавление объемов с различными цветами баров
            colors = ['green' if data['close'][i] > data['open'][i] else 'red' for i in range(len(data))]
            fig.add_trace(go.Bar(
                x=data.index,
                y=data['volume'],
                name='Volume',
                marker=dict(color=colors, opacity=0.5),
                yaxis='y2'
            ))  # Добавляем объемы в график с различной окраской баров

            # Настройки графика с наложением объемов
            fig.update_layout(
                title=f"{symbol} {timeframe} {chart_type}",  #75 Название графика
                xaxis_title="Дата",  #76 Название оси X
                yaxis_title="Цена",  #77 Название оси Y
                template="plotly_dark",  #78 Тема оформления графика
                xaxis_rangeslider_visible=False,  #79 Отключение стандартного слайдера диапазона на оси X
                hovermode='x unified',  #80 Единое перекрестие для всех точек по оси X
                dragmode='pan',  #81 Устанавливаем панорамирование по умолчанию
                yaxis=dict(title='Цена'),
                yaxis2=dict(title='Объем', overlaying='y', side='right', showgrid=False)  # Создаем вторую ось Y для объемов
            )

            # Отображаем график в QWebEngineView
            self.chart_view.setHtml(fig.to_html(include_plotlyjs='cdn'))  #82 Конвертация графика в HTML и отображение в интерфейсе
