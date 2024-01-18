#############################
# Training (Menu)
# JCY oct 23
# PRO DB PY
#############################
"""
DATE MODIFICATION : 18.01.2024
AUTEUR : Leakos Alexis
DESCRIPTION : fichier contenant la page d'accueil
avec les multiples choix de direction
ainsi que la page d'affichage des résultats
"""
import tkinter as tk
from tkinter import ttk, messagebox
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
def exercise(event, exer, window,username):
    dict_games[exer](window, username)


class destroy_button():
    def __init__(self, frame, student_id, rowD, data):
        self.button_delete = tk.Button(frame, text="supprimer", command=lambda: destroy_result(student_id, data, frame))
        self.button_delete.grid(row=rowD, column=8)


class ModifyButton:
    def __init__(self, parameter_frame, frame, student_id, data, rowD):
        self.modify_button = tk.Button(parameter_frame, text="Modifier",
                                            command=lambda: modification_window(frame, data, id=student_id))
        self.modify_button.grid(row=rowD, column=7)


def modify(student_id, data, frame):
    database.modify_results(data, student_id)
    show_results(frame, data[0], data[1])


# window to modify the datas
def modification_window(parent_frame, data, id=None, table_type="modify", ):
    updated_results_window = tk.Toplevel(parent_frame)
    updated_results_window.title("modification des résultats")
    updated_results_window.geometry("1080x255")

    update_frame = tk.Frame(updated_results_window, padx=15)
    update_frame.pack()
    # items to modify
    updating_datas = ["temps", "nb OK", "nb Total"]
    for updating_data in range(len(updating_datas)):
        info_item = tk.Label(update_frame, text=updating_datas[updating_data])
        info_item.grid(row=0, column=0 + updating_data)
    name_entry = tk.Entry(update_frame)
    dateTime_entry = tk.Entry(update_frame)
    time_entry = tk.Entry(update_frame)
    exercise_entry = tk.Entry(update_frame)
    OK_entry = tk.Entry(update_frame)
    total_entry = tk.Entry(update_frame)

    entries = [time_entry, OK_entry, total_entry]
    for inserted_entry in range(len(entries)):
        entries[inserted_entry].grid(row=1, column=inserted_entry)
    if OK_entry.get() <= total_entry.get():
        button_finish = tk.Button(update_frame, text="Valider", command=lambda:modify(id, data=[time_entry.get(), OK_entry.get(), total_entry.get()], frame=parent_frame))
        button_finish.grid(row=2, column=4)
    else:
        tk.messagebox.showerror(parent=updated_results_window, title="Rhoooo le tricheur...", message="On va dire que tu t'es trompé entre les deux.")
        return entries

def destroy_result(student_id, data, frame):
    database.delete_result(student_id)
    show_results(frame, data[0], data[1])


# call display_results
def display_result(event):
    # create new window and organise it
    global progress_bar, window_results
    window_results = tk.Toplevel()
    window_results.title("Résultats")
    window_results.geometry("1400x1100")

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
    parameters_entries = {}

    exercise_value = tk.StringVar(parameters_frame)
    cbo_entry_exercice_create = ttk.Combobox(parameters_frame, textvariable=exercise_value, font=("Arial", 10),
                                             width=15)
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
        parameters_entries[label_text] = entry
        print(parameters_entries["Pseudo:"].get())

    # Middle part with parameters
    parameters_frame = tk.Frame(window_results)
    parameters_frame.pack(pady=20)

    # Results
    main_results_frame = tk.Frame(window_results)
    main_results_frame.pack()
    results_frame = tk.Frame(main_results_frame)
    results_frame.grid(row=0, column=0, pady=20)

    # Button to view results
    view_results_button = tk.Button(parameters_frame, text="Voir résultats",
                                    command=lambda: show_results(results_frame, parameters_entries["Pseudo:"].get(),
                                                                 cbo_entry_exercice_create.get()),
                                    font=("Helvetica", 12))
    view_results_button.grid(row=0, columnspan=len(parameters_labels) + 1, pady=10)

    # Labels for each column
    columns = ["Elève", "Date heure", "Temps", "Exercice", "nb OK", "nb Total", "% réussi", "Modify", "Delete"]

    for col in columns:
        label = tk.Label(results_frame, text=col, relief=tk.RIDGE, width=15, font=("Helvetica", 12))
        label.grid(row=0, column=columns.index(col))

    # Total box
    total_box = tk.Frame(window_results)
    total_box.pack(pady=20)

    total_label = tk.Label(total_box, text="Total", font=("Helvetica", 16))
    total_label.pack()

    # Last part for summarized showed
    summer_frame = tk.Frame(window_results)
    summer_frame.pack(pady=20)

    summerised_columns = ["Nbessais", "Temps total", "Nb Total", "% Total", "% Visual"]

    for col in summerised_columns:
        label = tk.Label(summer_frame, text=col, relief=tk.RIDGE, width=15, font=("Helvetica", 12))
        label.grid(row=0, column=summerised_columns.index(col))

    # Add sample data for the last part (replace this with your actual data)
    last_part_data = database.show_summerized_results()

    for j, value in enumerate(last_part_data):
        label = tk.Label(summer_frame, text=value, relief=tk.RIDGE, width=15, font=("Helvetica", 12))
        label.grid(row=1, column=j)
    print("display_result")

    try:
        accuracy = round(float(last_part_data[2]) / float(last_part_data[3]) * 100, 2)
    except:
        accuracy = 0

    # Add a progress bar in the last column
    progress_bar = ttk.Progressbar(summer_frame, orient="horizontal", mode="determinate",
                                   length=100, value=accuracy)
    progress_bar.grid(row=1, column=4, padx=5)


def reset_table(frame):
    for widget in frame.winfo_children():
        if widget.grid_info()['row'] != 0:
            widget.destroy()


def show_results(results_frame, name="", exercise=""):
    reset_table(results_frame)
    # Add sample data (replace this with your actual data)
    sample_data = database.show_database(name, exercise)
    if sample_data != False:
        for data in range(len(sample_data)):
            for info in range(len(sample_data[data])):
                # print(sample_data[data][info])
                label = tk.Label(results_frame, text=sample_data[data][info], relief=tk.RIDGE, width=15,
                                 font=("Helvetica", 10))
                label.grid(row=data + 1, column=info)

            accuracy = round(float(sample_data[data][4]) / float(sample_data[data][5]) * 100, 2)

            # Add a progress bar in the last column
            progress_bar = ttk.Progressbar(results_frame, orient="horizontal", mode="determinate",
                                           length=100, value=accuracy)
            progress_bar.grid(row=data + 1, column=6, padx=5)

            # button to modify the data
            destroy_button_name = f"destroy_button_{data}"
            modify_button_name = f"modify_button_{data}"
            #exec(
            #    "%s = destroy_button(res_frame, student[j][6], [res_frame, variables, tot_frame, window_results], %d, %d)"
            #    % (destroy_button_name, j + 1, i + 7))
            exec(
                "%s = ModifyButton(results_frame, window_results, sample_data[data][6], [results_frame, (name, exercise), window_results], %d)"
                % (modify_button_name, data + 1))
            # Button to delete the data
            button_delete_name = f"button_delete_{data}"
            exec("%s = destroy_button(results_frame, %d, %d, data=%s)" % (
            button_delete_name, sample_data[data][6], data + 1, [name, exercise]))

def open_window(username, privilege):
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
                            lambda event, ex=ex: exercise(event=None, exer=a_exercise[ex], window=window, username=username))  # link to others .py
        print(a_exercise[ex])

    # Buttons, display results & quit
    btn_display = tk.Button(window, text="Display results", font=("Arial", 15))
    btn_display.grid(row=1 + 2 * len(a_exercise) // 3, column=1)
    btn_display.bind("<Button-1>", lambda e: display_result(e))

    btn_logout = tk.Button(window, text="Déloguer", font=("Arial", 15))
    btn_logout.grid(row=2 + 2 * len(a_exercise) // 3, column=1)
    btn_logout.bind("<Button-1>", lambda e: logout(window))

    btn_finish = tk.Button(window, text="Quitter", font=("Arial", 15))
    btn_finish.grid(row=3 + 2 * len(a_exercise) // 3, column=1)
    btn_finish.bind("<Button-1>", quit)

    # main loop
    window.mainloop()


# logout from the game
def logout(window):
    from register_login import window_login
    window.destroy()
    window_login()


if __name__ == "__main__":
    from register_login import window_login
    window_login()