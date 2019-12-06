import sqlite3, time
import tkinter as tk
from tkinter import messagebox
from tkinter.font import BOLD


class LoginScreen(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title('Generic POS 1.0')

        height = self.master.winfo_screenheight()
        width = self.master.winfo_screenwidth()

        self.master.geometry(f'{int(width * 0.2)}x{int(height * 0.2)}+{int(width * 0.4)}+{int(height * 0.3)}')
        self.master.config(borderwidth='20')
        self.master.resizable(False, False)

        self.user_var = tk.StringVar()
        self.pass_var = tk.StringVar()

        title = tk.Label(self, text='Log-in to continue', font=('Trebuchet MS', 20, BOLD), bd=5)
        title.grid(columnspan = 2)
        username = tk.Label(self, text='Employee ID: ', font=('Trebuchet MS', 15))
        username.grid(row=1)
        username1 = tk.Entry(self, textvariable=self.user_var, font=('Trebuchet MS', 15),
                                  bd=2, relief=tk.SUNKEN)
        username1.grid(row=1, column=1)
        password = tk.Label(self, text='Password: ', font=('Trebuchet MS', 15))
        password.grid(row=2)
        password1 = tk.Entry(self, textvariable=self.pass_var, font=('Trebuchet MS', 15), show='●',
                                  bd=2, relief=tk.SUNKEN)
        password1.bind('<Return>', lambda x: self.verify(self.user_var.get(), self.pass_var.get()))
        password1.grid(row=2, column=1)
        login = tk.Button(self, text='Submit', font=('Trebuchet MS', 15), bd=5, relief=tk.RAISED,
                               command=lambda: self.verify(self.user_var.get(), self.pass_var.get()))
        login.grid(row=3, columnspan=2)


    def verify(self, username, password):
        try:
            software_user = 'Administrator'
            software_pass = 'Admin@123'

            if username == software_user and password == software_pass:
                self.master.destroy()
                MainInterface()
            else:
                self.errorMessage()
        except ValueError:
            self.errorMessage()
        except TypeError:
            self.errorMessage()


    def errorMessage(self):
        messagebox.showinfo("Login Error", "Incorrect username or password.")
        self.user_var.set('')
        self.pass_var.set('')


class MainInterface(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title('Generic POS 1.0')
        self.master.protocol('WM_DELETE_WINDOW', lambda: self.exitApplication())

        height = self.master.winfo_screenheight()
        width = self.master.winfo_screenwidth()
        self.master.geometry(f'{int(width * 0.5)}x{int(height * 0.5)}+{int(width * 0.25)}+{int(height * 0.2)}')

        self.menu_bar = tk.Menu(self)
        self.shift_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='Shift', underline=0, menu=self.shift_menu)
        self.shift_menu.add_command(label='Substitute Cashier', underline=0, command=lambda: self.doNothing())
        self.shift_menu.add_command(label='End Shift', underline=0, command=lambda: self.doNothing())
        self.shift_menu.add_command(label='End-of-Day Shift', underline=8, command=lambda: self.doNothing())
        self.shift_menu.add_separator()
        self.shift_menu.add_command(label='Exit Application', underline=1, command=lambda: self.exitApplication())

        self.customer_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='Customers', underline=0, menu=self.customer_menu)
        self.customer_menu.add_command(label='Customers', underline=0, command=lambda: self.doNothing())
        self.customer_menu.add_command(label='Add Customer', underline=0, command=lambda: self.doNothing())
        self.customer_menu.add_command(label='Remove Customer', underline=0, command=lambda: self.doNothing())
        self.customer_menu.add_command(label='Update Customer', underline=0, command=lambda: self.doNothing())

        self.product_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='Inventory', underline=0, menu=self.product_menu)
        self.product_menu.add_command(label='Products', underline=0, command=lambda: self.doNothing())
        self.product_menu.add_command(label='Add Product', underline=0, command=lambda: self.doNothing())
        self.product_menu.add_command(label='Remove Product', underline=0, command=lambda: self.doNothing())
        self.product_menu.add_command(label='Update Product', underline=0, command=lambda: self.doNothing())

        self.transactions_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='Transactions', underline=0, menu=self.transactions_menu)
        self.transactions_menu.add_command(label='View History', underline=5, command=lambda: self.doNothing())
        self.transactions_menu.add_command(label='Product Statistics', underline=8, command=lambda: self.doNothing())
        self.transactions_menu.add_command(label='Reports', underline=0, command=lambda: self.doNothing())
        self.transactions_menu.add_command(label='Logs', underline=0, command=lambda: self.doNothing())

        self.help_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='Help', underline=0, menu=self.help_menu)
        self.help_menu.add_command(label='Transactions', underline=0, command=lambda: self.doNothing())
        self.help_menu.add_command(label='Administration', underline=0, command=lambda: self.doNothing())
        self.help_menu.add_command(label='Send Report', underline=0, command=lambda: self.doNothing())

        self.about_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='About', underline=0, menu=self.about_menu)
        self.about_menu.add_cascade(label='Program', underline=0, command=lambda: self.doNothing())
        self.about_menu.add_cascade(label='Creator', underline=0, command=lambda: self.doNothing())

        self.master.config(borderwidth='20', menu=self.menu_bar)
        self.master.resizable(False, False)



    def doNothing(self):
        pass


    def exitApplication(self):
        prompt = messagebox.askyesno('Exit Program', 'Are you sure you want to exit the program?')
        if prompt:
            self.master.quit()


if __name__ == '__main__':
    employeesDB = sqlite3.connect('employees.db')
    employeesC = employeesDB.cursor()
    employeesC.execute('CREATE TABLE IF NOT EXISTS Employees (employeeID INTEGER, password TEXT, firstName TEXT, lastName TEXT, authorityLevel INTEGER)')

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

    LoginScreen().mainloop()
