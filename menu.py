#############################
# Training (Menu)
# JCY oct 23
# PRO DB PY
#############################

import tkinter as tk
from tkinter import ttk
import geo01
import info02
import info05
import database

# exercises array
a_exercise = ["geo01", "info02", "info05"]
albl_image = [None, None, None]  # label (with images) array
a_image = [None, None, None]  # images array
a_title = [None, None, None]  # array of title (ex: GEO01)

dict_games = {"geo01": geo01.open_window_geo_01, "info02": info02.open_window_info_02,
              "info05": info05.open_window_info_05}

# values
progress_bar = 0


# call other windows (exercices)
def exercise(event, exer):
    dict_games[exer](window)


# get the results from user parameters
def view_specific_results():
    print("test")  # TODO si bar de progression inactif |-> suite des lignes ne s'affichent pas. TO PATCH
    database.select_where()


# call display_results
def display_result(event):  # TODO
    # create new window and organise it
    global progress_bar
    window_results = tk.Toplevel(window)
    window_results.title("Résultats")
    window_results.geometry("1100x900")

    # Upper part
    upper_frame = tk.Frame(window_results)
    upper_frame.pack(pady=20)

    title_label = tk.Label(upper_frame, text="Training: Affichage", font=("Helvetica", 16))
    title_label.pack()

    # Parameters entry form
    parameters_frame = tk.Frame(window_results)
    parameters_frame.pack(pady=20)

    # Labels and Entry widgets for parameters
    parameters_labels = ["Pseudo:"]
    parameters_entries = []

    exercise_value = tk.StringVar(parameters_frame)
    cbo_entry_exercice_create = ttk.Combobox(parameters_frame, textvariable=exercise_value, font=("Arial", 10), width=15)
    cbo_entry_exercice_create.grid(row=0, column=0)
    cbo_entry_exercice_create['values'] = ('ANY', 'GEO01', 'INFO02', 'INFO05')
    '''
    note: upgrade idea -> entries are picked up directly from the database. TODO if time left
    '''
    cbo_entry_exercice_create['state'] = 'readonly'

    for i, label_text in enumerate(parameters_labels):
        label = tk.Label(parameters_frame, text=label_text, font=("Helvetica", 12))
        label.grid(row=0, column=i + 1, padx=5, pady=5, sticky="e")

        entry = tk.Entry(parameters_frame, font=("Helvetica", 12))
        entry.grid(row=0, column=i + 2, padx=5, pady=5, sticky="w")
        parameters_entries.append(entry)

    # Button to view results
    view_results_button = tk.Button(parameters_frame, text="Voir résultats", command=view_specific_results(name,exercise),
                                    font=("Helvetica", 12))
    view_results_button.grid(row=1, columnspan=len(parameters_labels) + 1, pady=10)

    # Middle part with parameters
    parameters_frame = tk.Frame(window_results)
    parameters_frame.pack(pady=20)

    # Labels for each column
    columns = ["Elève", "Date heure", "Temps", "Exercice", "nb OK", "nb Total", "% réussi"]

    for col in columns:
        label = tk.Label(parameters_frame, text=col, relief=tk.RIDGE, width=15, font=("Helvetica", 12))
        label.grid(row=0, column=columns.index(col))

    # Add sample data (replace this with your actual data)
    sample_data = database.show_database()

    for data in range(len(sample_data)):
        for info in range(len(sample_data[data])):
            print(sample_data[data][info])
            label = tk.Label(parameters_frame, text=sample_data[data][info], relief=tk.RIDGE, width=15,
                             font=("Helvetica", 10))
            label.grid(row=data + 1, column=info)

        # Add a progress bar in the last column
        progress_bar = ttk.Progressbar(parameters_frame, orient="horizontal", mode="determinate",
                                       length=100, value=round(float(sample_data[data][4]) / float(sample_data[data][5]) * 100, 2))
        progress_bar.grid(row=data + 1, column=6, padx=5)

    # Total box
    total_box = tk.Frame(window_results)
    total_box.pack(pady=20)

    total_label = tk.Label(total_box, text="Total", font=("Helvetica", 16))
    total_label.pack()

    # Last part with 5 columns
    last_part_frame = tk.Frame(window_results)
    last_part_frame.pack(pady=20)

    last_part_columns = ["NbLignes", "Temps total", "Nb Total", "% Total"]

    for col in last_part_columns:
        label = tk.Label(last_part_frame, text=col, relief=tk.RIDGE, width=15, font=("Helvetica", 12))
        label.grid(row=0, column=last_part_columns.index(col))

    # Add sample data for the last part (replace this with your actual data)
    last_part_data = ["100", "5 hours", "500", "75%"]

    for j, value in enumerate(last_part_data):
        label = tk.Label(last_part_frame, text=value, relief=tk.RIDGE, width=15, font=("Helvetica", 12))
        label.grid(row=1, column=j)
    print("display_result")


# Main window
window = tk.Tk()
window.title("Training, entrainement cérébral")
window.geometry("1100x900")

# color définition
rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color  # translation in hexa
window.configure(bg=hex_color)
window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

# Title création
lbl_title = tk.Label(window, text="TRAINING MENU", font=("Arial", 15))
lbl_title.grid(row=0, column=1, ipady=5, padx=40, pady=40)

# labels creation and positioning
for ex in range(len(a_exercise)):
    a_title[ex] = tk.Label(window, text=a_exercise[ex], font=("Arial", 15))
    a_title[ex].grid(row=1 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)  # 3 label per row

    a_image[ex] = tk.PhotoImage(file="img/" + a_exercise[ex] + ".gif")  # image name
    albl_image[ex] = tk.Label(window, image=a_image[ex])  # put image on label
    albl_image[ex].grid(row=2 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)  # 3 label per row
    albl_image[ex].bind("<Button-1>",
                        lambda event, ex=ex: exercise(event=None, exer=a_exercise[ex]))  # link to others .py
    print(a_exercise[ex])

# Buttons, display results & quit
btn_display = tk.Button(window, text="Display results", font=("Arial", 15))
btn_display.grid(row=1 + 2 * len(a_exercise) // 3, column=1)
btn_display.bind("<Button-1>", lambda e: display_result(e))

btn_finish = tk.Button(window, text="Quitter", font=("Arial", 15))
btn_finish.grid(row=2 + 2 * len(a_exercise) // 3, column=1)
btn_finish.bind("<Button-1>", quit)

# main loop
window.mainloop()
