import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import font
from tkinter.constants import EW, NS, NSEW
from tkinter.messagebox import showerror, showinfo, askretrycancel


def topheader_frame(container):
    # add label frame
    top_labelframe = ttk.LabelFrame(
        container, text='Log Book', labelanchor='n', borderwidth=4)
    # return the toplevel frame
    return top_labelframe

# create our 'footer' frame at bottom


def bottom_frame(container):
    bottom_labelframe = ttk.LabelFrame(
        container, borderwidth=4, text='A 2021 Left-Handed Production', labelanchor='s', style='Bottom.TLabelframe')
    return bottom_labelframe

# create our left side frame


def leftside_frame(container):
    # add our labelframe
    left_labelframe = ttk.LabelFrame(
        container, text='Water Data', labelanchor='n', borderwidth=4)
    left_labelframe.columnconfigure(0, weight=1)
    left_labelframe.columnconfigure(1, weight=1)
    # enter water body name
    streamlabel_text = tk.StringVar()
    streamlabel = ttk.Label(left_labelframe, text='Water Fished(Name):',
                            foreground='black', background='#FFEBF2', style='Data.TLabel')
    streamlabel.grid(column=0, row=1, sticky=tk.EW)
    streamlabel_entry = ttk.Entry(
        left_labelframe, takefocus=0, cursor='hand1', textvariable=streamlabel_text)
    streamlabel_entry.grid(column=1, row=1, sticky=tk.EW)
    # add county selector

    return left_labelframe

# create our rightside frame


def rightside_frame(container):
    right_labelframe = ttk.LabelFrame(
        container, text='Place Data', labelanchor='n', borderwidth=4)
    right_labelframe.columnconfigure(0, weight=1)
    right_labelframe.columnconfigure(1, weight=1)
    # add species select chunk

    def species_selected(event):
        msg = f'You selected {specieslabel_text.get()}!'
        showinfo(title='Result', message=msg)

    # tkinter stuff for species select
    species = ('Brown Trout', 'Rainbow Trout', 'Brook Trout', 'Steelhead', 'Lake Run Brown Trout', 'Carp', 'Smallmouth Bass',
               'Largemouth Bass', 'Bluegill', 'Pumpkinseed', 'Perch', 'Walleye', 'Northern Pike', 'Musky', 'Bullhead')
    specieslabel_text = tk.StringVar()
    specieslabel = ttk.Label(right_labelframe,
        text='Select A Species:', foreground='black', background='#FFEBF2', style='Data.TLabel')
    specieslabel.grid(column=0, row=1, sticky=tk.W,
                      padx=5, pady=5, ipady=3, ipadx=3)
    specieslabel_combo = ttk.Combobox(right_labelframe, textvariable=specieslabel_text)
    specieslabel_combo['values'] = species
    specieslabel_combo['state'] = 'readonly'
    specieslabel_combo.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)
    specieslabel_combo.bind('<<ComboboxSelected>>', species_selected)
    #
    return right_labelframe


# create our main app window
def create_main_window():
    # create root
    root = tk.Tk()
    root.title('ASDF Log')
    root.geometry('600x600+15+15')
    root.iconbitmap('./assets/favicon_sa.ico')
    root.resizable(True, True)
    root.configure(bg='#FFEBF2')
    # create our style library
    style = ttk.Style()
    style.theme_use('winnative')
    # the below is automagically applied to any labelframe label txt
    style.configure('TLabelframe.Label', font=('Red Hat Text', 11))
    style.configure('Bottom.TLabelframe.Label', font=('Book Antiqua', 9))
    style.configure('TLabel', font=('Fira Mono', 9))
    style.configure('Data.TLabel', font=('Roboto Mono', 9))
    # add our other frames
    # maintain this order of adding frames to keep footer correct
    top_frame = topheader_frame(root)
    top_frame.pack(side='top', expand=0, fill='x',
                   ipady=15, ipadx=15, pady=3, padx=3)
    footer_frame = bottom_frame(root)
    footer_frame.pack(side='bottom', expand=0, fill='x',
                      ipady=15, ipadx=15, pady=3, padx=3)
    right_frame = rightside_frame(root)
    right_frame.pack(side='right', expand=1, fill='both',
                     ipady=3, ipadx=3, pady=3, padx=3)
    left_frame = leftside_frame(root)
    left_frame.pack(side='left', expand=1, fill='both',
                    ipady=3, ipadx=3, pady=3, padx=3)

    # run mainlooop on the root
    root.mainloop()


# create our main window from the func above
if __name__ == "__main__":
    create_main_window()
