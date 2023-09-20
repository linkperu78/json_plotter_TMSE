import numpy as np
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

# ------------------------------------------------------------------------------------
# Functions for User Interface
# ------------------------------------------------------------------------------------

# Update the dictionary key with
def update_dictionary(array_paths):

    for new_file in array_paths:
        print(f"New values in dictionary from = {new_file}")
        listb.insert("end", f"{os.path.basename(new_file)}\n")

        with open(new_file, 'r') as file:
            data = json.load(file)
            temp_array_dict = data['registro']

            for attempt_data in temp_array_dict:
                key = attempt_data['I']
                fecha = attempt_data['F']
                valor = attempt_data['P']
                

                if not key in my_dictionary.keys():
                    temp_dict = {
                        'Fecha' : [fecha],
                        'Valor' : [valor]
                    }
                    my_dictionary[key] = temp_dict
                else:
                    my_dictionary[key]['Fecha'].append(fecha)
                    my_dictionary[key]['Valor'].append(valor)
                    #my_dictionary[key].extend(data)

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
    for path in file_paths:
        print(f" - {path}\n")
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
    print(f"Selected value: {selected_value} and {event}")
    my_date_array = []
    array_date = my_dictionary[selected_value]['Fecha']
    for date in array_date:
        date_int = int(date)
        my_date_array.append(date_int)
    max_fecha = max(my_date_array)
    min_fecha = min(my_date_array)

    date_obj = datetime.datetime.fromtimestamp(max_fecha)
    max_date = date_obj.strftime("%H:%M:%S %d/%m/%Y")
    date_obj = datetime.datetime.fromtimestamp(min_fecha)
    min_date = date_obj.strftime("%H:%M:%S %d/%m/%Y")

    my_value_array = my_dictionary[selected_value]['Valor']
    
    print(f"{min_date}  -  {max_date}")
    if True:
        # Clear the previous plot
        ax.clear()
        
        # Plot the new data
        ax.plot(my_date_array, my_value_array)
        ax.set_xlabel('Tiempo')
        ax.set_ylabel(f"{selected_value}")
        ax.set_title(f'{selected_value}')
        
        # Update the canvas
        canvas.draw()

# -----------------------------------------------
# -------------- MAIN WINDOW --------------------
root = TkinterDnD.Tk()
root.geometry("800x600")
root.title("App Layout")
# -----------------------------------------------



# ------------------------------------------------------------------------------------
# Layout for app
# ------------------------------------------------------------------------------------

# Frame that expands over the entire app

outer_frame = ttk.Frame(root, borderwidth=2, relief="solid")
outer_frame.grid(row=0, column=0, sticky='nsew')
#outer_frame.grid_rowconfigure(0, weight=1)
#outer_frame.grid_columnconfigure(0, weight=1)


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
canvas_widget.pack(fill=tk.BOTH, expand=1)


my_dictionary = {'test':'hola'}
my_files = []
if __name__ == "__main__":
    my_dictionary.pop('test')
    root.mainloop()
