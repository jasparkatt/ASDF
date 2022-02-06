import tkinter as tk
from tkinter import ttk


# kwargs declared in class cant be modified when called later
# when added as a child
class MyButton(tk.Button):
    def __init__(self, master, **kwargs):
        # Defaults note these are 'TK' params, available params
        # differ betwen 'TK' and 'TTK' for most widgets
        kwargs['bg'] = 'gold'
        kwargs['fg'] = 'cadet blue'
        kwargs['bd'] = '2'
        super().__init__(master, **kwargs)


class MyLabel(ttk.Label):
    def __init__(self, master, **kwargs):
        # defaults note these are 'TTK' params
        kwargs['anchor'] = 'center'
        kwargs['background'] = 'cadet blue'
        kwargs['borderwidth'] = '4'
        kwargs['relief'] = 'groove'
        kwargs['font'] = ['Roboto Mono', 9, 'italic']
        kwargs['foreground'] = 'gold'
        kwargs['takefocus'] = 'True'
        kwargs['padding'] = '2 2 3 3'
        super().__init__(master, **kwargs)


class MyText(tk.Text):
    def __init__(self, master, **kwargs):
        kwargs['cursor'] = 'hand2'
        kwargs['bg'] = 'cadet blue'
        kwargs['bd'] = '4'
        kwargs['relief'] = 'groove'
        kwargs['font'] = ['Roboto Mono', 9, 'italic']
        kwargs['fg'] = 'gold'
        kwargs['takefocus'] = 'True'
        kwargs['padx'] = '2'
        super().__init__(master, **kwargs)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('600x400')  # this will set all frames to this size; will no longer dynamic resize
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self.winfo_toplevel().geometry("")# this resets geometry on each swithc, i think overides geometry kwarg from above.
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        MyLabel(self, cursor='hand2', text="This is the start page").pack(
            side="top", fill="x", pady=10)
        MyButton(self, cursor='sailboat', text="Open page one",
                 command=lambda: master.switch_frame(PageOne)).pack()
        MyButton(self, cursor='hand1', text="Open page two",
                 command=lambda: master.switch_frame(PageTwo)).pack()
        my_text = MyText(self, height=2, width=10) # shows how each frame resizes
        my_text.pack(side='bottom', fill='x')


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack(
            side="top", fill="x", pady=10)
        ttk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        my_text = MyText(self, height=4, width=35) # shows how each frame resizes
        my_text.pack(side='bottom', fill='x')


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(
            side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        my_text = MyText(self, height=1, width=55) # shows how each frame resizes
        my_text.pack(side='bottom', fill='x')


if __name__ == "__main__":
    app = App()
    app.mainloop()
