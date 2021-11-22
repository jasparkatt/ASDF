import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import font
from tkinter.constants import EW, NS, NSEW
from tkinter.messagebox import showerror, showinfo, askretrycancel
from tkcalendar import DateEntry, Calendar
from ttkbootstrap import Style


def topheader_frame(container):
    # add label frame
    top_labelframe = ttk.LabelFrame(
        container, text='Log Book', labelanchor='n', style='Top.TLabelframe')
    # return the toplevel frame
    return top_labelframe

# create our 'footer' frame at bottom
# add submit and exit buttons to bottom frame


def bottom_frame(container):
    bottom_labelframe = ttk.LabelFrame(
        container, text='A 2021 Left-Handed Production', labelanchor='n', style='Bottom.TLabelframe')
    bottom_labelframe.columnconfigure(0, weight=0)
    bottom_labelframe.columnconfigure(1, weight=1)
    bottom_labelframe.columnconfigure(2, weight=0)
    # add an exit button
    close_button = ttk.Button(
        bottom_labelframe, style='warning.Outline.TButton', text='Exit', command=container.destroy)
    close_button.grid(column=0, row=1, sticky=tk.E,
                      padx=3, pady=3, ipadx=1, ipady=1)
    #add submit button
    submit_button = ttk.Button(
        bottom_labelframe, style='secondary.Outline.TButton', text='Submit', command=container.destroy)
    submit_button.grid(column=2, row=1, sticky=tk.W,
                       padx=3, pady=3, ipady=1, ipadx=1)

    return bottom_labelframe


# water data left side frame
def leftside_frame(container):
    # add our labelframe
    left_labelframe = ttk.LabelFrame(
        container, text='Water Data', labelanchor='n')
    left_labelframe.columnconfigure(0, weight=1)
    left_labelframe.columnconfigure(1, weight=1)

    # enter water body name
    streamlabel_text = tk.StringVar()
    streamlabel = ttk.Label(
        left_labelframe, text='Water Fished(Name):', style='Data.TLabel')
    streamlabel.grid(column=0, row=1, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
    streamlabel_entry = ttk.Entry(
        left_labelframe, takefocus=0, cursor='hand1', textvariable=streamlabel_text)
    streamlabel_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

    # enter water type
    def watertype_selected(event):
        msg = f'You selected {watertype_text.get()}!'
        showinfo(title='Result', message=msg)

    watertypes = ('Cold', 'Cool', 'Warm', 'Cold-Cool', 'Cool-Warm')
    watertype_text = tk.StringVar()
    watertypelabel = ttk.Label(
        left_labelframe, text='Water Type(Temp):', style='Data.TLabel')
    watertypelabel.grid(column=0, row=3, sticky=tk.W,
                        padx=5, pady=5, ipady=3, ipadx=3)
    watertypelabel_combo = ttk.Combobox(
        left_labelframe, textvariable=watertype_text)
    watertypelabel_combo['values'] = watertypes
    watertypelabel_combo['state'] = 'readonly'
    watertypelabel_combo.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)
    watertypelabel_combo.bind('<<ComboboxSelected>>',
                              watertype_selected)  # enter water type

    def waterclass_selected(event):
        msg = f'You selected {waterclass_text.get()}!'
        showinfo(title='Result', message=msg)

    waterclass = ('Class 1', 'Class 2', 'Class 3', 'Non-Trout Water')
    waterclass_text = tk.StringVar()
    waterclasslabel = ttk.Label(
        left_labelframe, text='Water Class(Trout?):', style='Data.TLabel')
    waterclasslabel.grid(column=0, row=5, sticky=tk.W,
                        padx=5, pady=5, ipady=3, ipadx=3)
    waterclasslabel_combo = ttk.Combobox(
        left_labelframe, textvariable=waterclass_text)
    waterclasslabel_combo['values'] = waterclass
    waterclasslabel_combo['state'] = 'readonly'
    waterclasslabel_combo.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)
    waterclasslabel_combo.bind('<<ComboboxSelected>>', waterclass_selected)




    # add species type

    def species_selected(event):
        msg = f'You selected {specieslabel_text.get()}!'
        showinfo(title='Result', message=msg)

    # tkinter stuff for species select
    species = ('Brown Trout', 'Rainbow Trout', 'Brook Trout', 'Steelhead', 'Lake Run Brown Trout', 'Carp', 'Smallmouth Bass',
               'Largemouth Bass', 'Bluegill', 'Pumpkinseed', 'Perch', 'Walleye', 'Northern Pike', 'Musky', 'Bullhead')
    specieslabel_text = tk.StringVar()
    specieslabel = ttk.Label(
        left_labelframe, text='Select Species Caught:', style='Data.TLabel')
    specieslabel.grid(column=0, row=2, sticky=tk.W,
                      padx=5, pady=5, ipady=3, ipadx=3)
    specieslabel_combo = ttk.Combobox(
        left_labelframe, textvariable=specieslabel_text)
    specieslabel_combo['values'] = species
    specieslabel_combo['state'] = 'readonly'
    specieslabel_combo.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)
    specieslabel_combo.bind('<<ComboboxSelected>>', species_selected)

    # add calendar date picker
    def pickadate():
        top = tk.Toplevel(container)
        ttk.Label(top, text='Choose date').pack(padx=10, pady=10)
        cal = DateEntry(top, width=12, background='darkblue',
                        foreground='white', borderwidth=2, year=2010)
        cal.pack(padx=10, pady=10)
        ttk.Button(top, style='primary.Outline.TButton', text='exit',
                   command=top.destroy).pack(pady=3, padx=3)

    datebutton_label = ttk.Label(
        left_labelframe, text='Select Date:', style='Data.TLabel')
    datebutton_label.grid(column=0, row=6, sticky=tk.W,
                          padx=5, pady=5, ipady=3, ipadx=3)
    date_button = ttk.Button(
        left_labelframe, style='secondary.Outline.TButton', text='Pick Date', command=pickadate)
    date_button.grid(column=1, row=6, sticky=tk.EW,
                     padx=5, pady=5, ipadx=1, ipady=1)

    return left_labelframe

# create place data right side frame


def rightside_frame(container):
    right_labelframe = ttk.LabelFrame(
        container, text='Place Data', labelanchor='n')
    right_labelframe.columnconfigure(0, weight=1)
    right_labelframe.columnconfigure(1, weight=1)
    # add county select chunk

    def county_selected(event):
        msg = f'You selected {countylabel_text.get()}!'
        showinfo(title='Result', message=msg)

    countylabel_text = tk.StringVar()
    county = ('Adams', 'Ashland', 'Barron', 'Bayfield', 'Brown', 'Buffalo', 'Burnett',
                       'Calumet', 'Chippewa', 'Clark', 'Columbia', 'Crawford', 'Dane', 'Dodge',
                       'Door', 'Douglas', 'Dunn', 'Eau Claire', 'Florence', 'Fond du Lac', 'Forest',
                       'Grant', 'Green', 'Green Lake', 'Iowa', 'Iron', 'Jackson', 'Jefferson', 'Juneau',
                       'Kenosha', 'Kewaunee', 'La Crosse', 'Lafayette', 'Langlade', 'Lincoln', 'Manitowoc',
                       'Marathon', 'Marinette', 'Marquette', 'Menominee', 'Milwaukee', 'Monroe', 'Oconto',
                       'Oneida', 'Outagamie', 'Ozaukee', 'Pepin', 'Pierce', 'Polk', 'Portage', 'Price',
                       'Racine', 'Richland', 'Rock', 'Rusk', 'Saint Croix', 'Sauk', 'Sawyer', 'Shawano', 'Sheboygan',
                       'Taylor', 'Trempealeau', 'Vernon', 'Vilas', 'Walworth', 'Washburn', 'Washington',
                       'Waukesha', 'Waupaca', 'Waushara', 'Winnebago', 'Wood'
              )
    countylabel = ttk.Label(
        right_labelframe, text='Enter County Name:', style='Data.TLabel')
    countylabel.grid(column=0, row=1, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
    countylabel_combo = ttk.Combobox(
        right_labelframe, textvariable=countylabel_text)
    countylabel_combo['values'] = county
    countylabel_combo['state'] = 'readonly'
    countylabel_combo.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)
    countylabel_combo.bind('<<ComboboxSelected>>', county_selected)

    # create combo box for access type i.e. public, row, private
    def access_selected(event):
        msg = f'You selected {accesslabel_text.get()}!'
        showinfo(title='Result', message=msg)

    accesslabel_text = tk.StringVar()
    access = ('Public-DNR', 'Public-County',
              'Public-Other', 'ROW-Bridge', 'Private')
    accesslabel = ttk.Label(
        right_labelframe, text='Enter Access Type:', style='Data.TLabel')
    accesslabel.grid(column=0, row=2, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
    accesslabel_combo = ttk.Combobox(
        right_labelframe, textvariable=accesslabel_text)
    accesslabel_combo['values'] = access
    accesslabel_combo['state'] = 'readonly'
    accesslabel_combo.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)
    accesslabel_combo.bind('<<ComboboxSelected>>', access_selected)

    # combo box for ownership type i.e public, private, state, county, local, nonprofit etc
    def ownership_selected(event):
        msg = f'You selected {ownershiptype_text.get()}!'
        showinfo(title='Result', message=msg)

    ownershiptype_text = tk.StringVar()
    ownership = ('Public-State', 'Public-County', 'Public-Local',
                 'Private-Permission', 'Private-With Easement', 'Private-Public(i.e.MFL Open)')
    ownershiplabel = ttk.Label(right_labelframe, text='Enter Owner Type:')
    ownershiplabel.grid(column=0, row=3, sticky=tk.W,
                        padx=5, pady=5, ipady=3, ipadx=3)
    ownershiplabel_combo = ttk.Combobox(
        right_labelframe, textvariable=ownershiptype_text)
    ownershiplabel_combo['values'] = ownership
    ownershiplabel_combo['state'] = 'readonly'
    ownershiplabel_combo.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)
    ownershiplabel_combo.bind('<<ComboboxSelected>>', ownership_selected)

    # create a entry box for name of acces. i.e CTY HWY T access or HWY 21 access on w br of wh
    accessnamelabel_text = tk.StringVar()
    accesslabel = ttk.Label(right_labelframe, text='Enter Access Name:',
                            style='Data.TLabel')
    accesslabel.grid(column=0, row=4, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
    accesslabel_entry = ttk.Entry(
        right_labelframe, takefocus=0, cursor='hand1', textvariable=accessnamelabel_text)
    accesslabel_entry.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)
    # create a datepicker from tkcalender. need to pip install it first

    return right_labelframe

#create our table frame


def tableside_frame(container):
    table_labelframe = ttk.LabelFrame(
        container, text='Table Data', labelanchor='n')
    # add data from all the diff data entry, display as a table using treeview
    
    #table_labelframe.columnconfigure(0, weight=1)
    #table_labelframe.columnconfigure(1, weight=1)
    return table_labelframe

# create our main app window
def create_main_window():
    # create root
    root = tk.Tk()
    root.title('ASDF')
    root.geometry('800x600+295+55')
    root.iconbitmap('./assets/favicon_sa.ico')
    root.resizable(True, True)    
    # create our style library
    style = Style(
        theme='springdork', themes_file='C:/Users/jon.galloy/VisualStudioCodeProjects/ASDF/themes/ttkbootstrap_themes_dark.json')
    # the below is automagically applied to any labelframe label txt
    style.configure('TLabelframe.Label', font=('Fira Code', 11, 'italic'))
    style.configure('TLabel', font=('Fira Code', 9, 'italic'))
    style.configure('Data.TLabel', font=('Fira Mono', 8, 'bold'))

    # style.configure('Bottom.TLabelframe', bd=4, bc='Black')
    style.configure('Bottom.TLabelframe.Label',
                    font=('Georgia Pro', 8, 'italic'))

    # add our other frames
    # maintain this order of adding frames to keep footer correct
    top_frame = topheader_frame(root)
    top_frame.pack(side='top', expand=0, fill='x',
                   ipady=15, ipadx=15, pady=5, padx=5)
    footer_frame = bottom_frame(root)
    footer_frame.pack(side='bottom', expand=0, fill='x',
                      ipady=3, ipadx=3, pady=5, padx=3)
    table_frame = tableside_frame(root)
    table_frame.pack(side='bottom', expand=1, fill='both',
                     ipady=3, ipadx=3, pady=5, padx=5)
    right_frame = rightside_frame(root)
    right_frame.pack(side='right', expand=1, fill='both',
                     ipady=3, ipadx=3, pady=5, padx=5)
    left_frame = leftside_frame(root)
    left_frame.pack(side='left', expand=1, fill='both',
                    ipady=3, ipadx=3, pady=5, padx=5)
    

    # run mainlooop on the root
    root.mainloop()


# create our main window from the func above
if __name__ == "__main__":
    create_main_window()
