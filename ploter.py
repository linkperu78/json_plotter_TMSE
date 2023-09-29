#import numpy as np
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from matplotlib.dates import DateFormatter

# ------------------------------------------------------------------------------------
# Functions for User Interface
# ------------------------------------------------------------------------------------

# Update the dictionary key with
def update_dictionary(new_array_paths):

    for new_file in new_array_paths:
        #print(f"New values in dictionary from = {new_file}")
        listb.insert("end", f"{os.path.basename(new_file)}\n")
        my_temp_dictionary = {
            'test' : 1
        }
        my_temp_dictionary.pop('test')

        with open(new_file, 'r') as file:
            data = json.load(file)
            temp_array_dict = data['registro']

            for attempt_data in temp_array_dict:
                key = attempt_data['I']
                fecha = int(attempt_data['F'])
                valor = attempt_data['P']
                
                if not key in my_temp_dictionary.keys():
                    my_temp_dictionary[key]={
                        'Fecha' :[],
                        'Valor' :[]
                    }
                my_temp_dictionary[key]['Fecha'].append(fecha)
                my_temp_dictionary[key]['Valor'].append(valor)

        for key in my_temp_dictionary.keys():
            
            if not key in my_dictionary.keys():
                my_dictionary[key] = {
                    'Fecha' : [],
                    'Valor' : []
                }
            temp_data = my_temp_dictionary[key]['Valor']
            temp_date = my_temp_dictionary[key]['Fecha']
            my_dictionary[key]['Fecha'].append(temp_date)
            my_dictionary[key]['Valor'].append(temp_data)

    combo['values'] = list(my_dictionary.keys())


# When drag and drop into the list box
def on_drop(event):
    list_data = event.data.split()
    new_data = []

    for attempt_data in list_data:
        if attempt_data not in my_files and attempt_data.endswith(".json"):
            new_data.append(attempt_data)
    print(f"Values in drag and drop:\n{new_data}\n")
    my_files.append(new_data)
    update_dictionary(new_data)


# Cuando se presiona el boton, se abre el buscador de
# archivos, filtrando solo los archivos .json 
def button_event_fileex():
    file_paths = filedialog.askopenfilenames(
        title='Seleccionar archivos JSON',
        filetypes=(("JSON files","*.json"), ("All files","*.*")),
        initialdir="",
        multiple = True
    )
    new_path = []

    for attempt_data in file_paths:
        if attempt_data not in my_files:
            my_files.append(attempt_data)
            new_path.append(attempt_data)

    update_dictionary(new_path)


# Funcion para resetear toda la info y graficas
def button_hard_reset():
    my_dictionary.clear()
    my_files.clear()
    listb.delete(0, tk.END)
    combo['values']=[]
    combo_var.set("")
    ax.clear()
    canvas.draw()


def on_combobox_select(event):
    selected_value = combo_var.get()
    array_array_date      = my_dictionary[selected_value]['Fecha']
    array_array_value     = my_dictionary[selected_value]['Valor']
    print(array_array_value)

    max_fecha = [] 

    iterator = 0
    for array_date in array_array_date:
        max_ = max(array_date)
        max_fecha.append([max_,iterator])
        iterator+=1
    #print(max_fecha)
    ordered_data = [index[1] for index in sorted(max_fecha, key=max)]


    ordered_time_array      = []
    ordered_value_array     = []
    for index in ordered_data:
        new_time_array = array_array_date[index]
        new_data_array = array_array_value[index]
        ordered_time_array.append(new_time_array)
        ordered_value_array.append(new_data_array)

    x_axis = []
    for timestamps in ordered_time_array:
        x_axis.extend([datetime.datetime.fromtimestamp(ts) for ts in timestamps])

    #x_axis = sum( ordered_time_array, [] )
    y_axis = sum( ordered_value_array, [] )

    if True:
        # Clear the previous plot
        ax.clear()
        
        # Plot the new data
        ax.plot(x_axis, y_axis)
        ax.set_xlabel('Tiempo')
        ax.set_ylabel(f"{selected_value}")
        ax.set_title(f'{selected_value}')
        
        ax.xaxis.set_major_formatter(DateFormatter('%d %H:%M:%S'))

        # Rotate x-axis labels for better readability (optional)
        plt.xticks(rotation=15)

        # Update the canvas
        canvas.draw()

# -----------------------------------------------
# -------------- MAIN WINDOW --------------------
root = TkinterDnD.Tk()

# Make the window resizable
root.geometry("1024x800")

root.title("App Layout")
# -----------------------------------------------



# ------------------------------------------------------------------------------------
# Layout for app
# ------------------------------------------------------------------------------------

# Frame that expands over the entire app
outer_frame = ttk.Frame(root, borderwidth=2, relief="solid")
outer_frame.grid(row=0, column=0, sticky='nsew')

# Configure row and column weights for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# ROW 1
file_drop_canvas = tk.Canvas(outer_frame)
file_drop_canvas.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

listb = tk.Listbox(file_drop_canvas, bd=1, relief="solid", bg="#ffe0d6")
listb.pack(fill=tk.BOTH, expand=1)
listb.drop_target_register(DND_FILES)
listb.dnd_bind('<<Drop>>', on_drop)


# ROW 2
button_frame = ttk.Frame(outer_frame)
button_frame.grid(row=1, column=0, pady=10)

# Button 1
btn1 = ttk.Button(button_frame, text="Seleccionar", command=button_event_fileex)
btn1.pack(side="left", padx=20)

# Button 2
btn2 = ttk.Button(button_frame, text="Resetear", command=button_hard_reset)
btn2.pack(side="left", padx=20)

# Combobox
combo_var = tk.StringVar()
combo = ttk.Combobox(
    button_frame
    , values=[]
    , state='readonly'
    , textvariable=combo_var)
combo.pack(padx=20)
combo.bind("<<ComboboxSelected>>", on_combobox_select)

# ROW 3

graph_frame = ttk.Frame(outer_frame)
graph_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

# 2D graph showing a circle
fig, ax = plt.subplots()

# Create a canvas to display the plot
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)


my_dictionary = {'index': 0}
my_files = []
if __name__ == "__main__":
    my_dictionary.pop('index')
    root.mainloop()
