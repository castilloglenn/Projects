import tkinter as tk
from tkinter import messagebox

# ===================================================DECLARATION=======================================================
root = tk.Tk()
root.title('For BSIT-1D')
root.geometry('415x260')
root.resizable(0, 0)

steps_input = tk.StringVar()
spaces_between = tk.StringVar()
output = tk.StringVar()
thank_output = tk.StringVar()
operation = ''


# ====================================================THE PROCESS======================================================
def submit_copy():
    try:
        global operation
        root.clipboard_clear()
        steps = steps_input.get()
        spaces = spaces_between.get()
        if int(steps) > 0 and int(spaces) >= 0:
            spaces_result = ''
            for spaces in range(1, int(spaces) + 1):
                spaces_result += "\n"
            for step_result in range(1, int(steps) + 1):
                operation += ("\nStep " + str(step_result) + ":" + spaces_result)
            output.set('Copied')
            thank_output.set('Thank you for using! \nYou may now paste it \nin your document.')
            root.clipboard_append(operation)
            operation = ''
        else:
            tk.messagebox.showinfo('Invalid input', 'Use positive integers only')
    except ValueError:
        tk.messagebox.showinfo('Invalid input', 'Please enter a valid number.')
    except ZeroDivisionError:
        tk.messagebox.showinfo('Invalid input', 'Please enter a valid number.')


# ============================================TKINTER LABELS AND BUTTONS==================================================
title = tk.Label(root, text='Automatic Steps Printer', font=('Arial', 20, 'bold'), padx=10).grid(column=1, columnspan=4)
author = tk.Label(root, text='by: Allen Glenn E. Castillo', font=('Arial', 10)).grid(row=1, column=1, columnspan=4)

steps_input_label = tk.Label(root, text='Number of steps: ', font=('Arial', 15), padx=10).grid(row=2, column=1, columnspan=2)
steps_user_input = tk.Entry(root, font=('Arial', 15), textvariable=steps_input,
                            justify=tk.CENTER).grid(row=2, column=3, columnspan=2)

spaces_between_label = tk.Label(root, text='Spaces between: ', font=('Arial', 15)).grid(row=3, column=1, columnspan=2)
spaces_between_input = tk.Entry(root, font=('Arial', 15), textvariable=spaces_between,
                                justify=tk.CENTER).grid(row=3, column=3, columnspan=2)

status_field = tk.Label(root, text='Status:', font=('Arial', 15), justify=tk.CENTER).grid(row=4, column=1)
output_field = tk.Label(root, font=('Arial', 15), textvariable=output,
                        justify=tk.CENTER).grid(row=4, column=2)
submit_button = tk.Button(root, text='Copy Result', font=('Arial', 15),
                          bd=5, command=lambda: submit_copy()).grid(row=4, column=3, columnspan=2)

thank_you = tk.Label(root, font=('Arial', 15), bd=20,
                     textvariable=thank_output).grid(row=5, columnspan=6)

root.mainloop()
