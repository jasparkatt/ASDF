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
# add submit and exit buttons to bottom frame

def bottom_frame(container):
    bottom_labelframe = ttk.LabelFrame(
        container, borderwidth=4, text='A 2021 Left-Handed Production', labelanchor='s', style='Bottom.TLabelframe')
    return bottom_labelframe


# water data left side frame
def leftside_frame(container):
    # add our labelframe
    left_labelframe = ttk.LabelFrame(
        container, text='Water Data', labelanchor='n', borderwidth=4)
    left_labelframe.columnconfigure(0, weight=1)
    left_labelframe.columnconfigure(1, weight=1)

    # enter water body name
    streamlabel_text = tk.StringVar()
    streamlabel = ttk.Label(left_labelframe, text='Water Fished(Name):',foreground='black', background='#FFEBF2', style='Data.TLabel')
    streamlabel.grid(column=0, row=1, sticky=tk.W,padx=5, pady=5, ipady=3, ipadx=3)
    streamlabel_entry = ttk.Entry(left_labelframe, takefocus=0, cursor='hand1', textvariable=streamlabel_text)
    streamlabel_entry.grid(column=1, row=1, sticky=tk.EW)
    
    # add species type
    def species_selected(event):
        msg = f'You selected {specieslabel_text.get()}!'
        showinfo(title='Result', message=msg)

    # tkinter stuff for species select
    species = ('Brown Trout', 'Rainbow Trout', 'Brook Trout', 'Steelhead', 'Lake Run Brown Trout', 'Carp', 'Smallmouth Bass',
               'Largemouth Bass', 'Bluegill', 'Pumpkinseed', 'Perch', 'Walleye', 'Northern Pike', 'Musky', 'Bullhead')
    specieslabel_text = tk.StringVar()
    specieslabel = ttk.Label(left_labelframe,text='Select A Species:', foreground='black', background='#FFEBF2', style='Data.TLabel')
    specieslabel.grid(column=0, row=2, sticky=tk.W,padx=5, pady=5, ipady=3, ipadx=3)
    specieslabel_combo = ttk.Combobox(left_labelframe, textvariable=specieslabel_text)
    specieslabel_combo['values'] = species
    specieslabel_combo['state'] = 'readonly'
    specieslabel_combo.grid(column=1, row=2, sticky=tk.EW)
    specieslabel_combo.bind('<<ComboboxSelected>>', species_selected)

    return left_labelframe

# create place data right side frame
def rightside_frame(container):
    right_labelframe = ttk.LabelFrame(
        container, text='Place Data', labelanchor='n', borderwidth=4)
    right_labelframe.columnconfigure(0, weight=1)
    right_labelframe.columnconfigure(1, weight=1)
    # add county select chunk
    def county_selected(event):
        msg = f'You selected {countylabel_text.get()}!'
        showinfo(title='Result', message=msg)

    countylabel_text = tk.StringVar()
    county = ('Adams','Ashland','Barron','Bayfield','Brown','Buffalo','Burnett',
                       'Calumet','Chippewa','Clark','Columbia','Crawford','Dane','Dodge',
                       'Door','Douglas','Dunn','Eau Claire','Florence','Fond du Lac','Forest',
                       'Grant','Green','Green Lake','Iowa','Iron','Jackson','Jefferson','Juneau',
                       'Kenosha','Kewaunee','La Crosse','Lafayette','Langlade','Lincoln','Manitowoc',
                       'Marathon','Marinette','Marquette','Menominee','Milwaukee','Monroe','Oconto',
                       'Oneida', 'Outagamie', 'Ozaukee', 'Pepin', 'Pierce', 'Polk', 'Portage', 'Price',
                       'Racine','Richland','Rock','Rusk','Saint Croix','Sauk','Sawyer','Shawano','Sheboygan',
                       'Taylor','Trempealeau','Vernon','Vilas','Walworth','Washburn','Washington',
                       'Waukesha', 'Waupaca', 'Waushara', 'Winnebago', 'Wood'
                       )
    countylabel = ttk.Label(right_labelframe, text='Enter County Name:',foreground='black', background='#FFEBF2', style='Data.TLabel')
    countylabel.grid(column=0, row=1, sticky=tk.W,padx=5, pady=5, ipady=3, ipadx=3)
    countylabel_combo = ttk.Combobox(right_labelframe, textvariable=countylabel_text)
    countylabel_combo['values'] = county
    countylabel_combo['state'] = 'readonly'
    countylabel_combo.grid(column=1, row=1, sticky=tk.EW)
    countylabel_combo.bind('<<ComboboxSelected>>', county_selected)
    
    # create combo box for access type i.e. public, row, private
    def access_selected(event):
        msg = f'You selected {accesslabel_text.get()}!'
        showinfo(title='Result', message=msg)

    accesslabel_text = tk.StringVar()
    access = ('Public-DNR','Public-County','Public-Other','ROW-Bridge','Private')
    accesslabel = ttk.Label(right_labelframe, text='Enter Access Type',foreground='black', background='#FFEBF2', style='Data.TLabel')
    accesslabel.grid(column=0, row=2, sticky=tk.W,padx=5, pady=5, ipady=3, ipadx=3)
    accesslabel_combo = ttk.Combobox(right_labelframe, textvariable=accesslabel_text)
    accesslabel_combo['values'] = access
    accesslabel_combo['state'] = 'readonly'
    accesslabel_combo.grid(column=1, row=2, sticky=tk.EW)
    accesslabel_combo.bind('<<ComboboxSelected>>', access_selected)

    # combo box for ownership type i.e public, private, state, county, local, nonprofit etc
    def ownership_selected(event):
        msg = f'You selected {ownershiptype_text.get()}!'
        showinfo(title='Result', message=msg)

    ownershiptype_text = tk.StringVar()
    ownership = ('Public-State', 'Public-County', 'Public-Local','Private-Permission','Private-With Easement','Private-Public(i.e.MFL Open)')
    ownershiplabel = ttk.Label(right_labelframe, text='Enter Owner Type',foreground='black', background='#FFEBF2', style='Data.TLabel')
    ownershiplabel.grid(column=0, row=3, sticky=tk.W,padx=5, pady=5, ipady=3, ipadx=3)
    ownershiplabel_combo = ttk.Combobox(right_labelframe,textvariable=ownershiptype_text)
    ownershiplabel_combo['values'] = ownership
    ownershiplabel_combo['state'] = 'readonly'
    ownershiplabel_combo.grid(column=1, row=3, sticky=tk.EW)
    ownershiplabel_combo.bind('<<ComboboxSelected>>', ownership_selected)
    
    # create a entry box for name of acces. i.e CTY HWY T access or HWY 21 access on w br of wh
    
    return right_labelframe


# create our main app window
def create_main_window():
    # create root
    root = tk.Tk()
    root.title('ASDF')
    root.geometry('600x600+15+15')
    root.iconbitmap('./assets/favicon_sa.ico')
    root.resizable(True, True)
    root.configure(bg='#FFEBF2')
    # create our style library
    style = ttk.Style()
    style.theme_use('xpnative')
    # the below is automagically applied to any labelframe label txt
    style.configure('TLabelframe.Label', font=('Red Hat Text', 11))    
    style.configure('TLabel', font=('Fira Mono', 9))
    style.configure('Bottom.TLabelframe.Label', font=('Book Antiqua', 9))
    style.configure('Data.TLabel', font=('Roboto Mono', 9))
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


# create our main window from the func above
if __name__ == "__main__":
    create_main_window()
