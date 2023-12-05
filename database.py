"""
author:      Leakos Alexis
start date:  14.11.23
description: functions that impact the database or get information from there.
"""

# Imports
import mysql.connector
import tkinter
from tkinter import messagebox

import database


# functions ...
# ...to open the database
def open_dbconnection():
    global db_connection
    db_connection = mysql.connector.connect(host='127.0.0.1', port='3306', user='root',
                                            password='Jenny_4t_the_gate', database='ProjectPYDB',
                                            buffered=True, autocommit=True)


# ...to close the database
def close_dbconnection():
    db_connection.close()


# ...to get a student id by his pseudo
def get_student_id_by_nickname(pseudo):
    query = "SELECT id FROM students WHERE nickname = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (pseudo,))
    result_id = cursor.fetchall()
    cursor.close()
    return result_id


# ...to get a exercises id by his name
def get_exercise_id_by_name(exercise):
    query = "SELECT id FROM exercises WHERE name = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (exercise,))
    result_id = cursor.fetchall()
    cursor.close()
    return result_id


# ...to insert a new student in the students' data
def add_student(pseudo):
    query = "INSERT INTO students (nickname) VALUES (%s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (pseudo,))
    cursor.close()


# ...to insert a new exercise
def add_exercise(exercise):
    query = "INSERT INTO exercises (name) VALUE (%s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (exercise,))
    cursor.close()


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
        if ex_id == []:
            add_exercise(exercise)
            ex_id = get_exercise_id_by_name(exercise)[0][0]
        else:
            ex_id = ex_id[0][0]
        print(ex_id)
        name_id = get_student_id_by_nickname(pseudo)
        if name_id == []:
            add_student(pseudo)
            name_id = get_student_id_by_nickname(pseudo)[0][0]
        else:
            name_id = name_id[0][0]
        print(name_id)
        query = "INSERT INTO students_has_exercises (try, success, chronometer, start_date_and_time, student_id, exercise_id) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor = db_connection.cursor()
        cursor.execute(query, (nbtrials, nbsuccess, duration_s, start_date, name_id,
                               ex_id))  # todo trouver un moyen d'enregister correctement les heures dans "start_date_and_time"
        cursor.close()
        return True


# ... to display all results in results window
def show_database():
    open_dbconnection()
    cursor = db_connection.cursor()
    query = "SELECT students.nickname, students_has_exercises.start_date_and_time, students_has_exercises.chronometer, exercises.name, students_has_exercises.success, students_has_exercises.try FROM students_has_exercises INNER JOIN students ON students_has_exercises.student_id = students.id INNER JOIN exercises ON students_has_exercises.exercise_id = exercises.id"
    cursor.execute(query, )
    data = cursor.fetchall()
    cursor.close()
    close_dbconnection()
    return data


# ... to display specific results defined by user
def select_where(name, exercise):  # TODO
    input_data = []
    if name != "":
        input_data.append(get_student_id_by_nickname(name)[0])
    if exercise != "":
        input_data.append(get_exercise_id_by_name(exercise)[0])
    cursor = db_connection.cursor()

    query = "SELECT students.nickname, students_has_exercises.start_date_and_time, students_has_exercises.chronometer, exercises.name, students_has_exercises.success, students_has_exercises.try FROM students_has_exercises INNER JOIN students ON students_has_exercises.student_id = students.id INNER JOIN exercises ON students_has_exercises.exercise_id = exercises.id "
    if name != "" and exercise != "" or name != "" and exercise != "Any" :
        query += "WHERE students.nickname %s AND exercises.name = %s"
    elif name != "":
        query += "WHERE students.nickname %s"
    elif exercise != "" or exercise != "Any":
        query += "WHERE exercises.name = %s"

    cursor.execute(query, input_data)
    results = cursor.fetchall()
    cursor.close()
    return results