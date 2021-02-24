import sqlite3 as sql
import tkinter as tk
import datetime as dt
import random as r
import os, shutil
from sqlite3 import Error
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from zipfile import ZipFile as zf
from pathlib import Path
from tkinter import *

### FINAL THING TO BUG FIX, USE TRIPLE QUOTATIONS ON PROMPTS TO AVOID QUOTATION ERRORS

root = tk.Tk();
app_width = 795
app_height = 475
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
screen_x = int((screen_width / 2) - (app_width / 2))
screen_y = int((screen_height / 2) - (app_height / 1.75))

APP_TITLE = "QuizHub Ver.1.0 Alpha"
DATABASE_NAME = "quizhub.db"
HEADING_COLOR = "#284B63"
BODY_COLOR = "#f7f7f2"
FOOTER_COLOR = "#153243"

query_result = []
iterator_index = 0
is_searching = False
empty = "NULL"

try:
    conn = sql.connect(DATABASE_NAME)
    file = os.popen(f"attrib +h {DATABASE_NAME}")
    file.close()
    c = conn.cursor()
except Error as e:
    mb.showerror("Error", "Error while creating database connection:\n" + e)


def create_database():
    c.execute("""CREATE TABLE IF NOT EXISTS Exams (
                    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question VARCHAR(255),
                    correctAnswer VARCHAR(255),
                    wrongAnswer1 VARCHAR(255),
                    wrongAnswer2 VARCHAR(255),
                    wrongAnswer3 VARCHAR(255)
                );""")
    initial_check = get_record_by_question(check_entry(f"Welcome to {APP_TITLE}"))
    if initial_check is None and len(record_count()[0]) == 0:
        initial_record()


def initial_record():
    create_record = f"""INSERT INTO Exams VALUES(
                        1000, 
                        {check_entry(f"Welcome to {APP_TITLE}")}, 
                        {check_entry(f"Please add new entries to begin.")}, 
                        {empty}, {empty}, {empty});"""
    c.execute(create_record)
    conn.commit()


def reenter_initial_record():
    create_record = f"""INSERT INTO Exams (question, correctAnswer, wrongAnswer1, wrongAnswer2, wrongAnswer3)
                VALUES({check_entry(f"Welcome to {APP_TITLE}")}, 
                        {check_entry(f"Please add new entries to begin.")}, 
                        {empty}, {empty}, {empty});"""
    c.execute(create_record)
    conn.commit()


#============================DATABASE COMMANDS===========================================
def record_count():
    retrieve_all = "SELECT * FROM Exams;"
    retrieve_ansd = "SELECT * FROM Exams WHERE correctAnswer IS NOT NULL;"
    result = c.execute(retrieve_all).fetchall()
    result2 = c.execute(retrieve_ansd).fetchall()
    return [result, result2]


def get_records_by_keyword(question):
    retrieve_records = f"SELECT * FROM Exams WHERE question LIKE \"%{question}%\";"
    record = c.execute(retrieve_records).fetchall()
    return record


def get_record_by_id(qid):
    retrieve_record = f"SELECT * FROM Exams WHERE question_id={qid}"
    record = c.execute(retrieve_record).fetchone()
    return record


def get_record_by_question(question):
    retrieve_entry = f"SELECT question_id FROM Exams WHERE question={question}"
    record = c.execute(retrieve_entry).fetchone()
    return record


def update_current_database(imported_database_name):
    new_records_count = 0
    try:
        if ".zip" not in imported_database_name:
            database_string_name = imported_database_name + ".zip"
        else:
            database_string_name = imported_database_name

        if Path(database_string_name).is_file():
            with zf(database_string_name, "r") as zip:
                zip.extractall()

            new_conn = sql.connect(database_string_name.replace(".zip", ".db"))
            new_cursor = new_conn.cursor()

            all_records_command = f"SELECT * FROM Exams"
            all_records = new_cursor.execute(all_records_command).fetchall()

            added_records = 0
            for record in all_records:
                result = get_record_by_question(check_entry(record[1]))
                if result is None:
                    create_record = f"""INSERT INTO Exams (question, correctAnswer, wrongAnswer1, wrongAnswer2, wrongAnswer3)
                                 VALUES({check_entry(record[1])}, 
                                        {check_entry(record[2])},
                                        {check_entry(record[3])},
                                        {check_entry(record[4])},
                                        {check_entry(record[5])} 
                            );"""
                    c.execute(create_record)
                    conn.commit()
                    added_records += 1
            mb.showinfo(APP_TITLE + ": SUCCESS", f"Database updated, {added_records} new entries has been added.")
            new_cursor.close()
            new_conn.close()
            os.remove(database_string_name.replace(".zip", ".db"))
            count = record_count()
            if len(count[0]) > 1:
                check = get_record_by_question(check_entry(f"Welcome to {APP_TITLE}"))
                if check is not None:
                    remove_record(check[0])
            update_entry_count()
        else:
            mb.showwarning(APP_TITLE, "Database not found. Please check the name and enter again.")
    except Error:
            mb.showwarning(APP_TITLE, "Database name error. Please check the name and enter again.")
    

def new_record(record, toplevel, components):
    result = get_record_by_question(record[0])
    if record[0] == "Null":
        mb.showwarning(APP_TITLE, "Please enter the question.", parent=toplevel)
    elif result is not None:
        mb.showwarning(APP_TITLE, "Question already exists.", parent=toplevel)
    else:
        create_record = f"""INSERT INTO Exams (question, correctAnswer, wrongAnswer1, wrongAnswer2, wrongAnswer3)
                    VALUES({record[0]}, {record[1]}, {record[2]}, {record[3]}, {record[4]} 
                );"""
        c.execute(create_record)
        conn.commit()
        mb.showinfo(APP_TITLE, "Successfully inserted new record.", parent=toplevel)
        count = record_count()
        if len(count[0]) > 1:
            check = get_record_by_question(check_entry(f"Welcome to {APP_TITLE}"))
            if check is not None:
                remove_record(check[0])
        update_entry_count()
    
        for comp in components:
            comp.set("")


def modify_record(qid, column, value):
    update_record = f"""UPDATE Exams 
                        SET {column} = {value}
                        WHERE question_id = {qid};"""
    c.execute(update_record)
    conn.commit()


def remove_record(qid):
    delete_record = f"DELETE FROM Exams WHERE question_id={qid};"
    c.execute(delete_record)
    conn.commit()

    count = record_count()
    if len(count[0]) == 0:
        reenter_initial_record()
    
#===========================END OF DATABASE COMMANDS====================================

#===========================UTILITY COMMANDS============================================
def check_entry(string):
    if (string == "" or string == None):
        return "Null"
    formatted_string = " ".join(string.strip().split())
    return f"\"{formatted_string}\""


def check_query(data):
    return data if data is not None else " "


def search_database(event):
    global query_result, iterator_index, is_searching
    search_label['text'] = "Search Question:"
    question_query = search_entry.get()
    if question_query == "" or question_query == "Please enter question here":
        search_entry.set("Please enter question here")
    else:
        query_result = get_records_by_keyword(question_query)
        if len(query_result) == 0:
            mb.showinfo("Query Result", "No results found.")
        else:
            if len(query_result) > 1:
                next_button['state'] = NORMAL
            search_label['text'] = f"Result: {1}/{len(query_result)}"
            is_searching = True
            iterator_index = 0
            update_display_values(0)


def paste_and_search(event):
    search_entry.set(root.clipboard_get())
    search_database(0)


def update_display_values(trav):
    global query_result, iterator_index, is_searching
    if query_result == [] or (previous_button['state'] == DISABLED and next_button['state'] == DISABLED):
        pass
    elif not is_searching:
        next_button['state'] = DISABLED
        if trav == 0:
            iterator_index = 0
        else:
            iterator_index += trav
            if iterator_index >= len(query_result) - 1:
                iterator_index =  len(query_result) - 1
            elif iterator_index <= 0:
                iterator_index = 0
    else:
        if trav == 0:
            iterator_index = 0
        else:
            iterator_index += trav
            if iterator_index >= len(query_result) - 1:
                iterator_index =  len(query_result) - 1
                next_button['state'] = DISABLED
                previous_button['state'] = NORMAL
            elif iterator_index <= 0:
                iterator_index = 0
                previous_button['state'] = DISABLED
                next_button['state'] = NORMAL
            else:
                next_button['state'] = NORMAL
                previous_button['state'] = NORMAL
            search_label['text'] = f"Result: {iterator_index + 1}/{len(query_result)}"
    question_id['text'] = f"Question ID: {check_query(query_result[iterator_index][0])}"
    question_name['text'] = check_query(query_result[iterator_index][1])
    correct_answer['text'] = check_query(query_result[iterator_index][2])
    wrong_answer_1['text'] = f"• {check_query(query_result[iterator_index][3])}"
    wrong_answer_2['text'] = f"• {check_query(query_result[iterator_index][4])}"
    wrong_answer_3['text'] = f"• {check_query(query_result[iterator_index][5])}"


def update_entry_count():
    records = record_count()
    total_entries['text'] = f"TOTAL QUESTIONS ENTERED: {len(records[0]):,}"
    total_answered['text'] = f"TOTAL CORRECT ANSWERS: {len(records[1]):,}"


def refresh_entries(event):
    global query_result, iterator_index, is_searching
    query_result = record_count()[0]
    search_label['text'] = "Search Question:"
    if len(query_result) == 0:
        mb.showinfo("Query Result", "No results found.")
    else:
        previous_button['state'] = DISABLED
        next_button['state'] = DISABLED
        is_searching = False
        if len(query_result) > 1:
            next_button['state'] = NORMAL
            random_trav = r.randint(-len(query_result) + 1, len(query_result) - 1)
            update_display_values(random_trav)
        else:
            update_display_values(0)


def update_database(event):
    database_name = sd.askstring(
        APP_TITLE, 
        "Please enter the name of the database: \n(Ex. quizhub_export_184511_02232021.zip)"
    )
    if database_name == "":
        mb.showwarning(APP_TITLE, "Please enter value on the field.")
    elif database_name != None:
        update_current_database(database_name)


def export_database(event):
    confirmation = mb.askyesno(APP_TITLE + ": Please confirm", "Are you sure you want to\nexport the database?")
    if confirmation:
        timestamp = dt.datetime.now().strftime("_export_%H%M%S_%m%d%Y.db")
        export_file_name = DATABASE_NAME.replace(".db", timestamp)
        cwd = os.getcwd()
        file = DATABASE_NAME
        new = export_file_name
        shutil.copy(cwd+"\\"+file, cwd+"\\"+new)
        with zf(new.replace(".db", ".zip"), "w") as zip:
            zip.write(new)
        os.remove(new)
        mb.showinfo(APP_TITLE+": SUCCESS", 
f"Database has been exported successfully!\nPlease check the current folder for the file named:\n\"{export_file_name}\"")

#===========================END OF UTILITY COMMANDS=====================================

#===========================TKINTER COMMANDS============================================
def show_update(field):
    user_input = sd.askstring("Change Field", f"Enter {field}:")
    if user_input != None:
        if field == "Question":
            verify_update("question", user_input, question_name['text'])
        elif field == "Correct Answer":
            verify_update("correctAnswer", user_input, correct_answer['text'])
        elif field == "Wrong Answer 1":
            verify_update("wrongAnswer1", user_input, wrong_answer_1['text'].replace("• ", ""))
        elif field == "Wrong Answer 2":
            verify_update("wrongAnswer2", user_input, wrong_answer_2['text'].replace("• ", ""))
        elif field == "Wrong Answer 3":
            verify_update("wrongAnswer3", user_input, wrong_answer_3['text'].replace("• ", ""))


def verify_update(column_to_update, user_input, current):
    result = mb.askokcancel(APP_TITLE, f"Current: {current}\nNew: {user_input}\nAre your sure?") # True / False
    if result:
        modify_record(int(question_id['text'].replace("Question ID: ", "")), column_to_update, check_entry(user_input))
        mb.showinfo(APP_TITLE, "SUCCESS: Please search again to refresh results.")


def show_add_new_entry(event):
    window_width = 350
    window_height = 340
    
    window_x = int((screen_width / 2) - (window_width / 2))
    window_y = int((screen_height / 2) - (window_height / 1.75))

    entry_root = Toplevel(root)
    entry_root.title(APP_TITLE)
    entry_root.geometry(f"{str(window_width)}x{str(window_height)}+{str(window_x)}+{str(window_y)}")
    entry_root.configure(background=FOOTER_COLOR)
    entry_root.resizable(False, False)

    title_label = Label(entry_root, bg=HEADING_COLOR, fg="white",
                        text="NEW ENTRY",
                        font="Arial 16 bold").pack(
                            fill="both"
                        )
    question_label = Label(entry_root, bg=BODY_COLOR,
                        text=" Question:",
                        font="Arial 12 bold",
                        anchor=W).pack(
                            fill="both"
                        )
    question_entry = StringVar(entry_root)
    question_text = Entry(entry_root, bg=BODY_COLOR,
                        textvariable=question_entry).pack(
                            fill="both"
                        )
    correct_answer_label = Label(entry_root, bg=BODY_COLOR,
                        text=" Correct Answer:",
                        font="Arial 12 bold",
                        anchor=W).pack(
                            fill="both"
                        )
    correct_answer_entry = StringVar(entry_root)
    correct_answer_text = Entry(entry_root, bg=BODY_COLOR,
                        textvariable=correct_answer_entry).pack(
                            fill="both"
                        )
    wrong_answer1_label = Label(entry_root, bg=BODY_COLOR,
                        text=" Wrong Answer 1:",
                        font="Arial 12 bold",
                        anchor=W).pack(
                            fill="both"
                        )
    wrong_answer1_entry = StringVar(entry_root)
    wrong_answer1_text = Entry(entry_root, bg=BODY_COLOR,
                        textvariable=wrong_answer1_entry).pack(
                            fill="both"
                        )
    wrong_answer2_label = Label(entry_root, bg=BODY_COLOR,
                        text=" Wrong Answer 2:",
                        font="Arial 12 bold",
                        anchor=W).pack(
                            fill="both"
                        )
    wrong_answer2_entry = StringVar(entry_root)
    wrong_answer2_text = Entry(entry_root, bg=BODY_COLOR,
                        textvariable=wrong_answer2_entry).pack(
                            fill="both"
                        )
    wrong_answer3_label = Label(entry_root, bg=BODY_COLOR,
                        text=" Wrong Answer 3:",
                        font="Arial 12 bold",
                        anchor=W).pack(
                            fill="both"
                        )
    wrong_answer3_entry = StringVar(entry_root)
    wrong_answer3_text = Entry(entry_root, bg=BODY_COLOR,
                        textvariable=wrong_answer3_entry).pack(
                            fill="both"
                        )
    filler_label = Label(entry_root, bg=FOOTER_COLOR,
                        text=" ").pack()
    create_button = Button(entry_root,
                        text="Create New",
                        font="Arial 10 bold",
                        command=lambda: new_record(
                            [
                                check_entry(question_entry.get()),
                                check_entry(correct_answer_entry.get()),
                                check_entry(wrong_answer1_entry.get()),
                                check_entry(wrong_answer2_entry.get()),
                                check_entry(wrong_answer3_entry.get())
                            ], entry_root, [
                            question_entry,
                            correct_answer_entry,
                            wrong_answer1_entry,
                            wrong_answer2_entry,
                            wrong_answer3_entry
                        ])).pack(
                            fill="both"
                        )
    cancel_button = Button(entry_root,
                        text="Cancel",
                        font="Arial 10 bold",
                        command=entry_root.destroy).pack(
                            fill="both"
                        )

    entry_root.bind("<KeyPress-Return>", lambda event: new_record(
                            [
                                check_entry(question_entry.get()),
                                check_entry(correct_answer_entry.get()),
                                check_entry(wrong_answer1_entry.get()),
                                check_entry(wrong_answer2_entry.get()),
                                check_entry(wrong_answer3_entry.get())
                            ], entry_root, [
                            question_entry,
                            correct_answer_entry,
                            wrong_answer1_entry,
                            wrong_answer2_entry,
                            wrong_answer3_entry
                            ]))
    entry_root.bind("<Escape>", lambda event: entry_root.destroy())


def remove_entry_by_id(event):
    flagged_id = sd.askinteger("DELETE ENTRY", "Enter the Question ID:")

    if flagged_id != None:
        record = get_record_by_id(flagged_id)
        if record == None:
            mb.showwarning(APP_TITLE, "No results found, please check the id and enter again.")
        else:
            answer = mb.askyesno(
                APP_TITLE + ": CAUTION", 
                f"""
Are you sure you want to remove the record?
Question: {record[1]}
Correct Answer: {record[2]}
Wrong Answer #1: {record[3]}
Wrong Answer #2: {record[4]}
Wrong Answer #3: {record[5]}
Press YES to continue.
                """
            )
            if answer:
                remove_record(flagged_id)
                mb.showinfo(APP_TITLE, "Successfully deleted.")
                update_entry_count()

#===========================END OF TKINTER COMMANDS=====================================
if __name__ == "__main__":
    create_database()
    root.title(APP_TITLE)
    root.geometry(f"{str(app_width)}x{str(app_height)}+{str(screen_x)}+{str(screen_y)}")
    root.configure(background=FOOTER_COLOR)
    root.resizable(False, False)

    records = record_count()
    if len(records[0]) == 1:
        random_query = records[0][0]
    else:
        random_query = records[0][r.randint(0, len(records[0]) - 1)]

    #====================TKINTER COMPONENTS=====================
    top_frame = Frame(root, bg=HEADING_COLOR, bd=10)
    center_frame = Frame(root, bg=BODY_COLOR, bd=10)
    bottom_frame = Frame(root, bg=FOOTER_COLOR)


    question_id = Label(top_frame, bg=HEADING_COLOR, fg="white",
                        text=f"Question ID: {random_query[0]}",
                        font="Arial 14 bold")
    question_id.grid(row=0, column=0,
                        rowspan=2,
                        padx=5)
    top_filler = Label(top_frame, bg=HEADING_COLOR, fg="white", #3c887e
                        text="  " * 53).grid(
                            row=0,
                            column=1,
                            rowspan=2
                        )
    total_entries = Label(top_frame, bg=HEADING_COLOR, fg="white",
                        text=f"TOTAL QUESTIONS ENTERED: {len(records[0]):,}", 
                        font="Arial 12 bold")
    total_entries.grid(row=0, column=2,
                        sticky="e",
                        padx=5)
    total_answered = Label(top_frame, bg=HEADING_COLOR, fg="white",
                        text=f"TOTAL CORRECT ANSWERS: {len(records[1]):,}",
                        font="Arial 12 bold")
    total_answered.grid(row=1, column=2,
                        sticky="e",
                        padx=5)

    question_label = Label(center_frame, bg=BODY_COLOR,
                        text=f"Question:",
                        font="Arial 12 bold").grid(
                            row=0,
                            column=0,
                            padx=5,
                            sticky="w",
                        )
    question_name = Label(center_frame, bg=BODY_COLOR,
                        text=random_query[1],
                        font="Arial 10 normal",
                        wraplength=520)
    question_name.grid(row=1, column=0,
                        columnspan=2,
                        padx=5,
                        sticky="w")
    question_button = Button(center_frame, bg=BODY_COLOR,
                        text="Modify Question", 
                        width=32, 
                        command=lambda: show_update("Question")).grid(
                            row=1,
                            column=2,
                            sticky="e",
                            padx=5,
                        )
    center_filler = Label(center_frame, bg=BODY_COLOR,
                            text="  " * 85).grid(
                            row=2,
                            column=0,
                            columnspan=2
                        )
    correct_answer_label = Label(center_frame, bg=BODY_COLOR,
                        text=f"Correct Answer:",
                        font="Arial 12 bold")
    correct_answer_label.grid(row=3, column=0,
                        sticky="w",
                        padx=5)
    correct_answer = Label(center_frame, bg=BODY_COLOR,
                        text=random_query[2], 
                        wraplength=520, 
                        justify=LEFT)
    correct_answer.grid(row=4, column=0,
                        columnspan=2,
                        padx=5,
                        sticky="w",)
    correct_answer_button = Button(center_frame, bg=BODY_COLOR,
                        text="Modify Correct Answer", 
                        width=32,  
                        command=lambda: show_update("Correct Answer")).grid(
                            row=4,
                            column=2,
                            sticky="e",
                            padx=5,
                        )

    wrong_answer_label = Label(center_frame, bg=BODY_COLOR,
                        text=f"Wrong Answer(s):",
                        font="Arial 12 bold").grid(
                            row=5,
                            column=0,
                            sticky="w",
                            padx=5
                        )

    wrong_answer_1 = Label(center_frame, bg=BODY_COLOR,
                        text=f"• {random_query[3]}", 
                        wraplength=500, 
                        justify=LEFT)
    wrong_answer_1.grid(row=6, column=0,
                        columnspan=2,
                        padx=5,
                        sticky="w")
    wrong_answer_1_button = Button(center_frame, bg=BODY_COLOR,
                        text="Modify Wrong Answer 1", 
                        width=32,  
                        command=lambda: show_update("Wrong Answer 1")).grid(
                            row=6,
                            column=2,
                            sticky="e",
                            padx=5,
                        )

    wrong_answer_2 = Label(center_frame, bg=BODY_COLOR,
                        text=f"• {random_query[4]}", 
                        wraplength=500, 
                        justify=LEFT)
    wrong_answer_2.grid(row=7, column=0,
                        columnspan=2,
                        padx=5,
                        sticky="w")
    wrong_answer_2_button = Button(center_frame, bg=BODY_COLOR,
                        text="Modify Wrong Answer 2", 
                        width=32,  
                        command=lambda: show_update("Wrong Answer 2")).grid(
                            row=7,
                            column=2,
                            sticky="e",
                            padx=5,
                        )

    wrong_answer_3 = Label(center_frame, bg=BODY_COLOR,
                        text=f"• {random_query[5]}", 
                        wraplength=300, 
                        justify=LEFT)
    wrong_answer_3.grid(row=8, column=0,
                        columnspan=2,
                        padx=5,
                        sticky="w")
    wrong_answer_3_button = Button(center_frame, bg=BODY_COLOR,
                        text="Modify Wrong Answer 3", 
                        width=32,  
                        command=lambda: show_update("Wrong Answer 3")).grid(
                            row=8,
                            column=2,
                            sticky="e",
                            padx=5
                        )

    previous_button = Button(center_frame, bg=BODY_COLOR,
                        text="Previous",
                        width=16,
                        command=lambda: update_display_values(-1),
                        state=DISABLED)
    previous_button.grid(row=9, column=0,
                        padx=5,
                        pady=5)
    next_button = Button(center_frame, bg=BODY_COLOR,
                        text="Next",
                        width=16,
                        command=lambda: update_display_values(1),
                        state=DISABLED)
    next_button.grid(row=9, column=1,
                        padx=5,
                        pady=5)

    search_label = Label(bottom_frame, bg=FOOTER_COLOR, fg="white",
                        text="Search Question:",
                        font="Arial 12 bold")
    search_label.grid(row=0, column=0,
                        padx=5,
                        pady=5)
    search_entry = StringVar(root)
    search_box = Entry(bottom_frame,
                        width=65,
                        textvariable=search_entry).grid(
                            row=0,
                            column=1,
                            columnspan=2,
                            sticky="w",
                            padx=5
                        )
    search_button = Button(bottom_frame,
                        text="Submit", 
                        width=25,  
                        command= lambda: search_database(0)).grid(
                            row=0,
                            column=3,
                            padx=5,
                            pady=5
                        )

    add_entry_button = Button(bottom_frame,
                        text="Add (N)ew Entry", 
                        width=25,  
                        command= lambda: show_add_new_entry(0)).grid(
                            row=1,
                            column=0,
                            padx=5,
                            pady=5
                        )
    delete_entry_button = Button(bottom_frame,
                        text="(D)elete Entry", 
                        width=25,  
                        command=lambda: remove_entry_by_id(0)).grid(
                            row=1,
                            column=1,
                            padx=5
                        )
    update_database_button = Button(bottom_frame,
                        text="(U)pdate Database", 
                        width=25,  
                        command=lambda: update_database(0)).grid(
                            row=1,
                            column=2,
                            padx=5
                        )
    export_database_button = Button(bottom_frame,
                        text="(E)xport Database", 
                        width=25,  
                        command=lambda: export_database(0)).grid(
                            row=1,
                            column=3,
                            padx=5,
                            pady=5
                        )

    #===========LAYOUT MANAGER==============
    top_frame.pack(fill="both")
    center_frame.pack(fill="both")
    bottom_frame.pack(fill="both")

    #=========KEYBOARD SHORTCUTS============
    root.bind("<KeyPress-Return>" , lambda event: search_database(0))
    root.bind("<KeyPress-Left>" , lambda event: update_display_values(-1))
    root.bind("<KeyPress-Right>" , lambda event: update_display_values(1))
    root.bind("<Control-n>", lambda event: show_add_new_entry(0))
    root.bind("<Control-u>", lambda event: update_database(0))
    root.bind("<Control-d>", lambda event: remove_entry_by_id(0))
    root.bind("<Control-e>", lambda event: export_database(0))
    root.bind("<F1>", lambda event: paste_and_search(0))
    root.bind("<F5>", lambda event: refresh_entries(0))

    root.mainloop()
