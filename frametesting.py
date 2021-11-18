import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import font
from tkinter.constants import EW, NS, NSEW


def topheader_frame(container):
    #add label frame
    top_labelframe = ttk.LabelFrame(container, text='ASDF Home', labelanchor='n', borderwidth=4)    
    # return the toplevel frame
    return top_labelframe

# create our 'footer' frame at bottom
def bottom_frame(container):
    bottom_labelframe = ttk.LabelFrame(container, borderwidth=4, text='Footnotes & Thankyous', labelanchor='s')
    return bottom_labelframe

# create our left side frame
def leftside_frame(container):
    left_labelframe = ttk.LabelFrame(container, text='Place Data', labelanchor='n')
    return left_labelframe
    # add our labelframe
def rightside_frame(container):
    right_labelframe = ttk.LabelFrame(container, text='Place Data', labelanchor='n')
    return right_labelframe



# create our main app window
def create_main_window():
    # create root
    root = tk.Tk()
    root.title('ASDF')
    root.geometry('800x600+295+55')
    root.iconbitmap('./assets/favicon_sa.ico')
    root.resizable(True, True)
    root.configure(bg='#FFEBF2')
    #create our new style library
    style = ttk.Style()
    style.theme_create('style', parent='alt', 
    settings = { 'TLabelframe': {
        'configure': {
            'background': 'white',
            'relief': 'solid', # has to be 'solid' to color 
            'bordercolor': 'orange',
            'borderwidth': 1
        }
    },
    'TLabelframe.Label': {
        'configure': {
            'foreground': 'green',
            'background': 'white'
        }
    }
})
    style.theme_use('style')

    # create our style library(this is the old)
    """ style = ttk.Style()
    style.theme_use('vista')
    # the below is automagically applied to any labelframe label txt    
    style.configure('TLabelframe.Label', font=('Red Hat Text', 11))    
    style.configure('TLabel', font=('Fira Mono', 9))
    style.configure('Bottom.TLabelframe', bd=4, bc='Black')
    style.configure('Bottom.TLabelframe.Label', font=('Book Antiqua', 9))
    style.configure('Data.TLabel', font=('Roboto Mono', 9)) """
    # add our other frames
    # maintain this order of adding frames to keep footer correct
    top_frame = topheader_frame(root)
    top_frame.pack(side='top', expand=0, fill='x',
                   ipady=15, ipadx=15, pady=3, padx=3)
    footer_frame = bottom_frame(root)
    footer_frame.pack(side='bottom', expand=0, fill='x',
                      ipady=20, ipadx=20, pady=3, padx=3)
    right_frame = rightside_frame(root)
    right_frame.pack(side='right', expand=1, fill='both',
                     ipady=3, ipadx=3, pady=3, padx=3)
    left_frame = leftside_frame(root)
    left_frame.pack(side='left', expand=1, fill='both',
                    ipady=3, ipadx=3, pady=3, padx=3)

    # run mainlooop on the root
    root.mainloop()

if __name__ == "__main__":
    create_main_window()


