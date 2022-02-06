import tkinter as tk
from tkinter import ttk
from tkinterweb import HtmlFrame
import webbrowser


class MyButtons(ttk.Button):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = 'My Buttons'
        #self.command = self.destroy


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.destroy()
        # self.geometry('300x100')
        # self.title('Toplevel Window')
        #self.frame = HtmlFrame(self)  # create the HTML browser
        webbrowser.open("file:///C:/Users/suttr/ASDF/paca_geocode.html")  # load a website
        # self.frame.pack(fill="both", expand=True)  # attach the HtmlFrame widget to the parent window

        ttk.Button(self,
                   text='Close'
                   ).pack(expand=True)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('300x200')
        self.title('Main Window')

        # place a button on the root window
        ttk.Button(self,
                   text='Open a window',
                   command=self.open_window).pack(expand=True)

    def open_window(self):
        window = Window(self)
        window.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()


import tkinter as tk
from tkinter import ttk

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('help')
        self.geometry('500x200')

        tab_parent = ttk.Notebook(self)
        tab1 = ttk.Frame(tab_parent)
        tab2 = ttk.Frame(tab_parent)

        tab_parent.add(tab1, text="all records")
        tab_parent.add(tab2, text='add record')
        tab_parent.grid(row=0,column=0,columnspan=1,padx=10,pady=51)

if __name__ == "__main__":
    app = App()
    app.mainloop()


import tkinter as tk

import sqlite3

def connect():

    con1 = sqlite3.connect("<path/database_name>")

    cur1 = con1.cursor()

    cur1.execute("CREATE TABLE IF NOT EXISTS table1(id INTEGER PRIMARY KEY, First TEXT, Surname TEXT)")

    con1.commit()

    con1.close()


def View():

    con1 = sqlite3.connect("<path/database_name>")

    cur1 = con1.cursor()

    cur1.execute("SELECT * FROM <table_name>")

    rows = cur1.fetchall()    

    for row in rows:

        print(row) 

        tree.insert("", tk.END, values=row)        

    con1.close()


# connect to the database

connect() 

root = tk.Tk()

tree = ttk.Treeview(root, column=("c1", "c2", "c3"), show='headings')

tree.column("#1", anchor=tk.CENTER)

tree.heading("#1", text="ID")

tree.column("#2", anchor=tk.CENTER)

tree.heading("#2", text="FNAME")

tree.column("#3", anchor=tk.CENTER)

tree.heading("#3", text="LNAME")

tree.pack()

button1 = tk.Button(text="Display data", command=View)

button1.pack(pady=10)

root.mainloop()    