import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.constants import CENTER, E, END, LEFT
from tkinter.messagebox import showinfo
from ttkbootstrap import Style
from tkcalendar import DateEntry, Calendar
# our root window


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Data Entry')
        self.geometry('743x255+295+55')
        self.resizable(True, True)
        self.iconbitmap('./assets/favicon.ico')
        # grid
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)

        # style from ttkbootstrap
        self.style = Style(
        theme='spiritfallslt', themes_file='C:/Users/suttr/ASDF/themes/ttkbootstrap_themes_dark.json')
        # the below is automagically applied to any labelframe label txt
        self.style.configure('TLabelframe.Label', font=('Fira Code', 11, 'italic'))
        self.style.configure('Data.TLabel', font=('Fira Code', 8, 'italic'))
        self.style.configure('Outline.TButton', font=('Overpass Mono', 10))
        self.style.configure('Bottom.TLabelframe.Label',font=('Georgia Pro', 9, 'italic'))
        # example below that works....remove
        # self.style.configure('custom.TEntry', background='green', foreground='white', font=('Helvetica', 24))

        def clear_entryboxes():
            self.streamlabel_entry.delete(0, END)
            self.accesslabel_entry.delete(0,END)


        def county_selected(event):
            msg = f'You selected {self.countylabel_text.get()}!'
            showinfo(title='Result', message=msg)

        self.countylabel_text = tk.StringVar()
        self.county = ('Adams', 'Ashland', 'Barron', 'Bayfield', 'Brown', 'Buffalo', 'Burnett',
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
        self.countylabel = ttk.Label(
            self, text='Enter County Name:', style='Data.TLabel')
        self.countylabel.grid(column=0, row=0, sticky=tk.EW,
                     padx=5, pady=5, ipady=3, ipadx=3)
        self.countylabel_combo = ttk.Combobox(
            self, textvariable=self.countylabel_text)
        self.countylabel_combo['values'] = self.county
        self.countylabel_combo['state'] = 'readonly'
        self.countylabel_combo.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)
        self.countylabel_combo.bind('<<ComboboxSelected>>', county_selected)


        # enter water body name
        self.streamlabel_text = tk.StringVar()
    
        self.streamlabel = ttk.Label(
            self, text='Water Fished(Name):', style='Data.TLabel')
        self.streamlabel.grid(column=2, row=0, sticky=tk.EW,
                     padx=5, pady=5, ipady=3, ipadx=3)
        self.streamlabel_entry = ttk.Entry(
            self, takefocus=0, cursor='hand1', textvariable=self.streamlabel_text, style='custom.TEntry')
        self.streamlabel_entry.grid(column=3, row=0, sticky=tk.EW, padx=5, pady=5)

        # enter water type
        def watertype_selected(event):
            msg = f'You selected {self.watertype_text.get()}!'
            showinfo(title='Result', message=msg)

        self.watertypes = ('Cold', 'Cool', 'Warm', 'Cold-Cool', 'Cool-Warm')
        self.watertype_text = tk.StringVar()
        self.watertypelabel = ttk.Label(
            self, text='Water Type(Temp):', style='Data.TLabel')
        self.watertypelabel.grid(column=2, row=2, sticky=tk.EW,
                        padx=5, pady=5, ipady=3, ipadx=3)
        self.watertypelabel_combo = ttk.Combobox(
            self, textvariable=self.watertype_text)
        self.watertypelabel_combo['values'] = self.watertypes
        self.watertypelabel_combo['state'] = 'readonly'
        self.watertypelabel_combo.grid(column=3, row=2, sticky=tk.EW, padx=5, pady=5)
        self.watertypelabel_combo.bind('<<ComboboxSelected>>',
                              watertype_selected)  # enter water type

        def waterclass_selected(event):
            msg = f'You selected {self.waterclass_text.get()}!'
            showinfo(title='Result', message=msg)

        self.waterclass = ('Class 1', 'Class 2', 'Class 3', 'Non-Trout Water')
        self.waterclass_text = tk.StringVar()
        self.waterclasslabel = ttk.Label(
            self, text='Water Class(Trout?):', style='Data.TLabel')
        self.waterclasslabel.grid(column=2, row=3, sticky=tk.EW,
                        padx=5, pady=5, ipady=3, ipadx=3)
        self.waterclasslabel_combo = ttk.Combobox(
            self, textvariable=self.waterclass_text)
        self.waterclasslabel_combo['values'] = self.waterclass
        self.waterclasslabel_combo['state'] = 'readonly'
        self.waterclasslabel_combo.grid(column=3, row=3, sticky=tk.EW, padx=5, pady=5)
        self.waterclasslabel_combo.bind('<<ComboboxSelected>>', waterclass_selected)

        # tkinter stuff for species select
        def species_selected(event):
            msg = f'You selected {self.specieslabel_text.get()}!'
            showinfo(title='Result', message=msg)

    
        self.species = ('Brown Trout', 'Rainbow Trout', 'Brook Trout', 'Steelhead', 'Lake Run Brown Trout', 'Carp', 'Smallmouth Bass',
               'Largemouth Bass', 'Bluegill', 'Pumpkinseed', 'Perch', 'Walleye', 'Northern Pike', 'Musky', 'Bullhead')
        self.specieslabel_text = tk.StringVar()
        self.specieslabel = ttk.Label(
            self, text='Select Species Caught:', style='Data.TLabel')
        self.specieslabel.grid(column=2, row=1, sticky=tk.EW,
                      padx=5, pady=5, ipady=3, ipadx=3)
        self.specieslabel_combo = ttk.Combobox(
            self, textvariable=self.specieslabel_text)
        self.specieslabel_combo['values'] = self.species
        self.specieslabel_combo['state'] = 'readonly'
        self.specieslabel_combo.grid(column=3, row=1, sticky=tk.EW, padx=5, pady=5)
        self.specieslabel_combo.bind('<<ComboboxSelected>>', species_selected)

        # create combo box for access type i.e. public, row, private
        def access_selected(event):
            msg = f'You selected {self.accesslabel_text.get()}!'
            showinfo(title='Result', message=msg)

        self.accesslabel_text = tk.StringVar()
        self.access = ('Public-DNR', 'Public-County',
              'Public-Other', 'ROW-Bridge', 'Private')
        self.accesslabel = ttk.Label(
            self, text='Enter Access Type:', style='Data.TLabel')
        self.accesslabel.grid(column=0, row=2, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
        self.accesslabel_combo = ttk.Combobox(
            self, textvariable=self.accesslabel_text)
        self.accesslabel_combo['values'] = self.access
        self.accesslabel_combo['state'] = 'readonly'
        self.accesslabel_combo.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)
        self.accesslabel_combo.bind('<<ComboboxSelected>>', access_selected)

    # combo box for ownership type i.e public, private, state, county, local, nonprofit etc
        def ownership_selected(event):
            msg = f'You selected {self.ownershiptype_text.get()}!'
            showinfo(title='Result', message=msg)

        self.ownershiptype_text = tk.StringVar()
        self.ownership = ('Public-State', 'Public-County', 'Public-Local',
                 'Private-Permission', 'Private-With Easement', 'Private-Public(i.e.MFL Open)')
        self.ownershiplabel = ttk.Label(self, text='Enter Owner Type:')
        self.ownershiplabel.grid(column=0, row=1, sticky=tk.W,
                        padx=5, pady=5, ipady=3, ipadx=3)
        self.ownershiplabel_combo = ttk.Combobox(
            self, textvariable=self.ownershiptype_text)
        self.ownershiplabel_combo['values'] = self.ownership
        self.ownershiplabel_combo['state'] = 'readonly'
        self.ownershiplabel_combo.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)
        self.ownershiplabel_combo.bind('<<ComboboxSelected>>', ownership_selected)

    # create a entry box for name of acces. i.e CTY HWY T access or HWY 21 access on w br of wh
        self.accessnamelabel_text = tk.StringVar()
        self.accesslabel = ttk.Label(self, text='Enter Access Name:',
                            style='Data.TLabel')
        self.accesslabel.grid(column=0, row=3, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
        self.accesslabel_entry = ttk.Entry(
            self, takefocus=0, cursor='hand1', textvariable=self.accessnamelabel_text)
        self.accesslabel_entry.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)
    # create a datepicker from tkcalender. need to pip install it first

        # add calendar date picker
        def pickadate():
            top = tk.Toplevel()
            top.geometry('278x154+3+3')
            ttk.Label(top, text='Choose date').pack(padx=10, pady=10)
            cal = DateEntry(top, width=12, background='grey',
                        foreground='white', borderwidth=2, year=2010)
            cal.pack(padx=10, pady=10)
            ttk.Button(top, style='danger.Outline.TButton', text='Exit',
                   command=top.destroy).pack(pady=3, padx=3,side='bottom')


        # add an exit button
        self.close_button = ttk.Button(
            self, style='danger.Outline.TButton', text='Exit', command=self.destroy)
        self.close_button.grid(column=0, row=5, sticky=tk.W,
                      padx=5, pady=5, ipady=3, ipadx=3)

        # add clear boxes button
        self.date_button = ttk.Button(
            self,style='secondary.Outline.TButton', text='Pick Date', command=pickadate)
        self.date_button.grid(column=1, row=4, sticky=tk.EW,columnspan=2,
                       padx=5, pady=5)

        # add date picker button
        self.clear_button = ttk.Button(
            self,style='success.Outline.TButton', text='Clear Boxes', command=clear_entryboxes)
        self.clear_button.grid(column=1, row=5, sticky=tk.EW,columnspan=2,
                       padx=5, pady=5)                                 
        #add submit button
        self.submit_button = ttk.Button(
            self, style='primary.Outline.TButton', text='Submit', command=self.destroy)
        self.submit_button.grid(column=3, row=5, sticky=tk.E,
                       padx=5, pady=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()


