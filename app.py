import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def on_scroll(*args):
    start = int(h_scrollbar.get())
    end = start + display_width
    ax.set_xlim(x[start], x[end])
    canvas.draw()

root = tk.Tk()
root.geometry("800x600")

graph_frame = ttk.Frame(root)
graph_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

# Create a figure and a subplot
fig, ax = plt.subplots()

# Create a canvas to display the plot
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, sticky='nsew')

# Sample data for the plot
x = np.linspace(0, 20 * np.pi, 10000)
y = np.sin(x)

# Plot the data
ax.plot(x, y)
ax.set_xlabel('x')
ax.set_ylabel('sin(x)')
ax.set_title('Sine Wave')

# Create a horizontal scrollbar
display_width = 1000  # Number of data points to display at once
h_scrollbar = tk.Scale(root, from_=0, to=len(x) - display_width, orient=tk.HORIZONTAL, command=on_scroll)
h_scrollbar.set(0)
h_scrollbar.grid(row=1, column=0, sticky='ew')

# Make the graph_frame and canvas_widget expandable
graph_frame.grid_rowconfigure(0, weight=1)
graph_frame.grid_columnconfigure(0, weight=1)

root.mainloop()
