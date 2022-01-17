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
