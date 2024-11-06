import tkinter as tk
from tkinter import ttk
import ccxt
import pandas as pd
from tkinter import messagebox

# Инициализация приложения и выбор биржи
exchange_options = ['binance', 'bybit', 'okx']  # Список бирж для выбора

# Создаем главное окно
root = tk.Tk()
root.title("Trading Bot Interface")
root.geometry("600x400")

# Функция для загрузки данных о валютных парах
def load_pairs():
    selected_exchange = exchange_var.get()
    if not selected_exchange:
        messagebox.showwarning("Выбор биржи", "Пожалуйста, выберите биржу.")
        return
    
    # Инициализация выбранной биржи
    exchange = getattr(ccxt, selected_exchange)()
    try:
        markets = exchange.load_markets()
        pairs = list(markets.keys())
        
        # Обновляем таблицу
        update_table(pairs)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

# Функция для обновления таблицы
def update_table(pairs):
    for row in table.get_children():
        table.delete(row)
    
    for pair in pairs:
        table.insert("", "end", values=(pair,))

# Функция для фильтрации валютных пар по поиску
def search_pairs():
    search_query = search_var.get().lower()
    filtered_pairs = [pair for pair in table.get_children() if search_query in table.item(pair)['values'][0].lower()]
    
    update_table(filtered_pairs)

# Выпадающий список для выбора биржи
exchange_var = tk.StringVar()
exchange_menu = ttk.Combobox(root, textvariable=exchange_var, values=exchange_options, state="readonly")
exchange_menu.set("Выберите биржу")
exchange_menu.pack(pady=10)

# Кнопка загрузки валютных пар
load_button = tk.Button(root, text="Загрузить валютные пары", command=load_pairs)
load_button.pack(pady=10)

# Поле для поиска
search_var = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack(pady=5)
search_entry.bind("<KeyRelease>", lambda event: search_pairs())

# Создание таблицы для отображения валютных пар
columns = ("Валютная пара",)
table = ttk.Treeview(root, columns=columns, show="headings")
table.heading("Валютная пара", text="Валютная пара")
table.pack(fill=tk.BOTH, expand=True)

# Запуск приложения
root.mainloop()
