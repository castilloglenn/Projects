import sqlite3, time
import tkinter as tk
from tkinter import messagebox
from tkinter.font import BOLD


class LoginScreen(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title('Generic Pharmacy POS 1.0')

        height = self.master.winfo_screenheight()
        width = self.master.winfo_screenwidth()

        self.master.geometry(f'{int(width * 0.2)}x{int(height * 0.2)}+{int(width * 0.4)}+{int(height * 0.3)}')
        self.master.config(borderwidth='20')
        self.master.resizable(False, False)

        user_var = tk.StringVar()
        pass_var = tk.StringVar()

        self.title = tk.Label(self, text='Log-in to continue', font=('Trebuchet MS', 20, BOLD), bd=5)
        self.title.grid(columnspan = 2)
        self.username = tk.Label(self, text='Username: ', font=('Trebuchet MS', 15))
        self.username.grid(row=1)
        self.username1 = tk.Entry(self, textvariable=user_var, font=('Trebuchet MS', 15),
                                  bd=2, relief=tk.SUNKEN)
        self.username1.grid(row=1, column=1)
        self.password = tk.Label(self, text='Password: ', font=('Trebuchet MS', 15))
        self.password.grid(row=2)
        self.password1 = tk.Entry(self, textvariable=pass_var, font=('Trebuchet MS', 15), show='●',
                                  bd=2, relief=tk.SUNKEN)
        self.password1.bind('<Return>', lambda x: self.verify(user_var.get(), pass_var.get()))
        self.password1.grid(row=2, column=1)
        self.login = tk.Button(self, text='Submit', font=('Trebuchet MS', 15), bd=5, relief=tk.RAISED,
                               command=lambda: self.verify(user_var.get(), pass_var.get()))
        self.login.grid(row=3, columnspan=2)


    def verify(self, username, password):
        software_user = 'Administrator'
        software_pass = 'Admin@123'

        if username == software_user and password == software_pass:
            self.master.destroy()
            MainInterface()
        else:
            messagebox.showinfo("Warning!", "Wrong username or password.")
            self.username1.delete(0, 'end')
            self.password1.delete(0, 'end')


class MainInterface(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title('Generic Pharmacy POS 1.0')
        self.master.protocol('WM_DELETE_WINDOW', lambda: self.exitApplication())

        height = self.master.winfo_screenheight()
        width = self.master.winfo_screenwidth()
        self.master.geometry(f'{int(width * 0.5)}x{int(height * 0.5)}+{int(width * 0.25)}+{int(height * 0.2)}')

        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Customers', menu=self.file_menu)
        self.file_menu.add_command(label='Browse Customers List', command=self.doNothing())
        self.file_menu.add_command(label='Add Customer', command=self.doNothing())
        self.file_menu.add_command(label='Remove Customer', command=self.doNothing())
        self.file_menu.add_command(label='Update Customer', command=self.doNothing())
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit Application', command=lambda: self.exitApplication())

        self.master.config(borderwidth='20', menu=self.menu_bar)
        self.master.resizable(False, False)



    def doNothing(self):
        pass


    def exitApplication(self):
        prompt = messagebox.askyesno('Exit Application', 'Are you sure?')
        if prompt:
            self.master.quit()


if __name__ == '__main__':
    customerDB = sqlite3.connect('customers.db')
    customerC = customerDB.cursor()
    customerC.execute(
        'CREATE TABLE IF NOT EXISTS Accounts (customerID INTEGER, firstName TEXT, lastName TEXT, age INTEGER, emailAdd TEXT)')
    customerC.execute('CREATE TABLE IF NOT EXISTS Points (customerID INTEGER, points INTEGER)')

    transactionDB = sqlite3.connect('transactions.db')
    transactionC = transactionDB.cursor()
    transactionC.execute(
        'CREATE TABLE IF NOT EXISTS Transactions (date TEXT, customerID INTEGER, transactionCode TEXT)')
    transactionC.execute('CREATE TABLE IF NOT EXISTS Reports (date TEXT, sales REAL, stats REAL)')

    productDB = sqlite3.connect('products.db')
    productC = productDB.cursor()
    productC.execute('CREATE TABLE IF NOT EXISTS Products (categoryCode TEXT, barCode INTEGER, productName TEXT, sellingPrice REAL)')

    root = tk.Tk()
    cls = LoginScreen()
    root.mainloop()
