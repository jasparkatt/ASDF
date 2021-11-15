import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.constants import EW, NS, NSEW


def topheader_frame(container):
    #add label frame
    top_labelframe = ttk.LabelFrame(container, text='ASDF Home', labelanchor='n', borderwidth=4)    
    # return the toplevel frame
    return top_labelframe

# create our 'footer' frame at bottom
def bottom_frame(container):
    bottom_labelframe = ttk.LabelFrame(container, borderwidth=4, text='A 2021 Left-Handed Production', labelanchor='s')
    return bottom_labelframe

# create our left side frame
def leftside_frame(container):
    # add our labelframe
    left_labelframe = ttk.LabelFrame(container, text='Water Data', labelanchor='n',borderwidth=4)
    
        
    return left_labelframe

# create our rightside frame
def rightside_frame(container):
    right_labelframe = ttk.LabelFrame(container, text='Place Data', labelanchor='n', borderwidth=4)
    return right_labelframe



# create our main app window
def create_main_window():
    #create root
    root = tk.Tk()
    root.title('AGO Login')
    root.geometry('600x600+15+15')
    root.iconbitmap('./assets/favicon_sa.ico')
    root.resizable(True, True)
    root.configure(bg='#FFEBF2')
    # create our style library
    style = ttk.Style()
    style.theme_use('winnative')
    # the below is automagically applied to any labelframe label txt
    style.configure('TLabelframe.Label', font=('Fira Code', 9))
    style.configure('Bottom.TLabelframe.Label', font=('Palatino Linotype', 8))

    #add our other frames
    # maintain this order of adding frames to keep footer correct
    top_frame = topheader_frame(root)
    top_frame.pack(side='top',expand=0,fill='x',ipady=15,ipadx=15,pady=3,padx=3)
    footer_frame = bottom_frame(root)
    footer_frame.pack(side='bottom', expand=0, fill='x',ipady=15, ipadx=15, pady=3, padx=3)
    right_frame = rightside_frame(root)
    right_frame.pack(side='right',expand=1,fill='both',ipady=3,ipadx=3,pady=3,padx=3)
    left_frame = leftside_frame(root)
    left_frame.pack(side='left',expand=1,fill='both',ipady=3, ipadx=3, pady=3, padx=3)
    
    # run mainlooop on the root 
    root.mainloop()
# create our main window from the func above
if __name__ == "__main__":
    create_main_window()
