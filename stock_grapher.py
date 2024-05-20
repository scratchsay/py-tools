import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf

def get_stock_data():
    company_name = entry.get()
    try:
        stock_data = yf.download(company_name, start='2023-01-01', end='2024-01-01')
        plot_stock_data(stock_data)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch stock data for {company_name}. Error: {e}")

def plot_stock_data(stock_data):
    global canvas  # Ensure canvas is accessible outside this function
    if 'canvas' in globals():
        canvas.get_tk_widget().destroy()  # Destroy existing canvas widget
    fig, ax = plt.subplots(figsize=(8, 6))
    stock_data['Close'].plot(ax=ax)
    ax.set_title('Stock Prices')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

window = tk.Tk()
window.title("Stock Price Graph")
window.geometry("800x600")

label = tk.Label(window, text="Enter company name:")
label.pack()

entry = tk.Entry(window)
entry.pack()

button = tk.Button(window, text="Get Stock Data", command=get_stock_data)
button.pack()

window.mainloop()
