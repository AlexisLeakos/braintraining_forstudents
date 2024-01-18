"""
author:      Leakos Alexis
project start date:  14.11.23
description: functions that impact the database or get information from there.
file last modification date: 18.01.2024
"""

# Imports
import mysql.connector, datetime, tkinter, bcrypt
from tkinter import messagebox


# functions ...
# ...to open the database
def open_dbconnection():
    global db_connection
    db_connection = mysql.connector.connect(host='127.0.0.1', port='3306', user='userProjDBPY',
                                            password='Pa$$w0rd', database='ProjectPYDB',
                                            buffered=True, autocommit=True)


# ...to close the database
def close_dbconnection():
    db_connection.close()


# ...to know if he is the first user of the program


def first_user_connection():
    query = "SELECT COUNT(id) FROM students"
    cursor = db_connection.cursor()
    cursor.execute(query)
    nb_result = cursor.fetchone()[0]
    print(nb_result)
    return nb_result

"""
We suppose that a teacher will be first to register into the database and to the game.
We also suppose that the students are honest and won't lie to the question.
"""


# ...to get a student id by his pseudo
def get_student_id_by_nickname(pseudo):
    query = "SELECT id FROM students WHERE nickname = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (pseudo,))
    result_id = cursor.fetchone()
    cursor.close()
    return result_id


def get_student_nickname_by_id(id):
    query = "SELECT nickname FROM students WHERE id = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (id,))
    result_name = cursor.fetchone()
    cursor.close()
    return result_name


# ...to get a exercises id by his name
def get_exercise_id_by_name(exercise):
    query = "SELECT id FROM exercises WHERE name = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (exercise,))
    result_id = cursor.fetchone()
    cursor.close()
    return result_id


def get_exercise_name_by_id(id):
    query = "SELECT name FROM exercises WHERE id = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (id,))
    result_name = cursor.fetchone()
    cursor.close()
    return result_name


# ...to insert a new exercise
def add_exercise(exercise):
    query = "INSERT INTO exercises (name) VALUE (%s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (exercise,))
    cursor.close()


# ... to delete the selected data in the database
def delete_result(id):
    open_dbconnection()
    query = "DELETE FROM students_has_exercises WHERE id=%s"
    cursor = db_connection.cursor()
    cursor.execute(query, (id,))
    close_dbconnection()


# ...to insert the datas given.
def insert_game_results(pseudo, exercise, nbtrials, nbsuccess, duration_s, start_date, window):
    if nbtrials == 0:
        tkinter.messagebox.showerror(parent=window, title="petit fainéant...",
                                     message="il fait au moins tenter une fois pour rentrer un résultat")
        return False
    elif pseudo == "" or pseudo is None:
        tkinter.messagebox.showinfo(parent=window, title="Pseudo manquant",
                                    message="Veuillez introduire un pseudo")
        return False
    else:
        ex_id = get_exercise_id_by_name(exercise)
        if ex_id == None:
            add_exercise(exercise)
            ex_id = get_exercise_id_by_name(exercise)[0]
        else:
            ex_id = ex_id[0]
        # print(ex_id)
        name_id = get_student_id_by_nickname(pseudo)
        # print(name_id)
        query = "INSERT INTO students_has_exercises (try, success, chronometer, start_date_and_time, student_id, exercise_id) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor = db_connection.cursor()
        cursor.execute(query, (nbtrials, nbsuccess, duration_s, start_date, name_id,
                               ex_id))  # todo trouver un moyen d'enregister correctement les heures dans "start_date_and_time"

        cursor.close()
        return True


# ... to modify the results already saved.
def modify_results(dataset, id):
    open_dbconnection()
    try:
        exercise_id = get_exercise_name_by_id(dataset[3])[0]
        date_data = dataset[1].split(" ")
        date_date_data = date_data[0].split("-")
        date_time_data = date_data[1].split(":")
        final_date = datetime.datetime(int(date_date_data[0]), int(date_date_data[1]), int(date_date_data[2]),
                                       int(date_time_data[0]), int(date_time_data[1]), int(date_time_data[2]))
        final_time = dataset[2]
        okay_tries = int(dataset[4])
        total_tries = int(dataset[5])
    except:
        return
    query = "UPDATE results SET pseudo = %s, date_et_heure = %s, temp = %s, nb_trials = %s, nb_ok = %s, minigame_id = %s WHERE id=%s"
    cursor = db_connection.cursor()
    cursor.execute(query, (dataset[0], final_date, final_time, total_tries, okay_tries, exercise_id, id))

    # todo function "create"


# ... to display all results in results window
def show_database(name, exercise):
    open_dbconnection()
    if exercise != "" and exercise != "ANY":
        try:
            exercise_id = get_exercise_id_by_name(exercise)
        except:
            return False
    if name != "":
        try:
            st_id = get_student_id_by_nickname(name)
        except:
            return False
    cursor = db_connection.cursor()
    query = "SELECT student_id, start_date_and_time, chronometer, exercise_id, success, try, id FROM students_has_exercises"
    if name != "" and exercise != "" and exercise != "ANY":
        query += f" WHERE student_id = %s AND exercise_id = %s"
        cursor.execute(query, (st_id, exercise_id))
    elif name != "":
        st_id = get_student_id_by_nickname(name)
        query += f" WHERE student_id = %s"
        cursor.execute(query, st_id)
    elif exercise != "" and exercise != "ANY":

        query += f" WHERE exercise_id = %s"
        cursor.execute(query, exercise_id)
    else:
        cursor.execute(query)
    results_unnamed = cursor.fetchall()
    results = []
    for result_set in results_unnamed:
        results.append((get_student_nickname_by_id(result_set[0]), result_set[1], result_set[2],
                        get_exercise_name_by_id(result_set[3]),
                        result_set[4], result_set[5], result_set[6]))
    cursor.close()
    close_dbconnection()
    return results


# make the average of the entire results or the displayed results
def show_summerized_results(name="", exercise=""):
    open_dbconnection()
    cursor = db_connection.cursor()
    get_student_id_by_nickname(name)
    query = "SELECT count(student_id), sum(chronometer), sum(success), sum(try) FROM students_has_exercises where student_id = %s"
    if name != "" and exercise != "" and exercise != "Any":
        st_id = get_student_id_by_nickname(name)[0]
        exercise_id = get_exercise_id_by_name(exercise)[0]
        query += f" WHERE student_id = %s AND exercise_id = %s"
        cursor.execute(query, (st_id, exercise_id))
    elif name != "":
        st_id = get_student_id_by_nickname(name)
        query += f" WHERE student_id = %s"
        cursor.execute(query, st_id)
    elif exercise != "" and exercise != "Any":
        exercise_id = get_exercise_id_by_name(exercise)
        query += f" WHERE exercise_id = %s"
        cursor.execute(query, exercise_id)
    else:
        cursor.execute(query)
    results = cursor.fetchall()[0]
    cursor.close()
    close_dbconnection()
    return results


# Insert a new student into the database
def insert_new_student(data, level):
    input_data = [data[0], data[1], level]
    password = input_data[1].encode('utf-8')
    input_data[1] = bcrypt.hashpw(password, bcrypt.gensalt())
    query = "INSERT INTO students (nickname, password, security_level) VALUES (%s, %s, %s)"
    cursor = db_connection.cursor()
    print(input_data)
    cursor.execute(query, input_data)
    cursor.close()


# login user
def check_login(username, password, window):
    from register_login import redirect_to_register, wrong_login_password
    open_dbconnection()
    if username == "" or password == "":
        tkinter.messagebox.showerror(parent=window, title="informations manquantes",
                                     message="Veuillez completer toutes les informations")
    else:
        cursor = db_connection.cursor()
        query = "SELECT password FROM students WHERE nickname = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result != None:
            result = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), result.encode('utf-8')):
                window.destroy()
                return True
            else:
                wrong_login_password()
        else:
            redirect_to_register()
            window.destroy()
            return False
