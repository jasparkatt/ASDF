import tkinter as tk
from tkinter import LabelFrame, ttk, StringVar
from tkinter import font
import tkinter
from tkinter.constants import END, EW, NS, NSEW
from tkinter.messagebox import showerror,showinfo,askretrycancel

from tkcalendar import DateEntry, Calendar
from ttkbootstrap import Style
from settings import *
import psycopg2


class topheader_frame(ttk.LabelFrame):
    def __init__(self,master):
        ttk.LabelFrame.__init__(self,master, text='ASDF Log', labelanchor='n',style='Top.TLabelframe')
        

class leftside_frame(ttk.LabelFrame):
    def __init__(self,master):
        ttk.LabelFrame.__init__(self,master,text='Water Data', labelanchor='n')
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)

        # enter water body name
        self.streamlabel_text = tk.StringVar()    
        self.streamlabel = ttk.Label(
            self, text='Water Fished(Name):', style='Data.TLabel')
        self.streamlabel.grid(column=0, row=1, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
        self.streamlabel_entry = ttk.Entry(
            self, takefocus=0, cursor='hand1', textvariable=self.streamlabel_text)
        self.streamlabel_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

    # enter water type
        def watertype_selected(event):
            msg = f'You selected {self.watertype_text.get()}!'
            showinfo(title='Result', message=msg)

        self.watertypes = ('Cold', 'Cool', 'Warm', 'Cold-Cool', 'Cool-Warm')
        self.watertype_text = tk.StringVar()
        self.watertypelabel = ttk.Label(
            self, text='Water Type(Temp):', style='Data.TLabel')
        self.watertypelabel.grid(column=0, row=3, sticky=tk.W,
                        padx=5, pady=5, ipady=3, ipadx=3)
        self.watertypelabel_combo = ttk.Combobox(
            self, textvariable=self.watertype_text)
        self.watertypelabel_combo['values'] = self.watertypes
        self.watertypelabel_combo['state'] = 'readonly'
        self.watertypelabel_combo.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)
        self.watertypelabel_combo.bind('<<ComboboxSelected>>',
                              watertype_selected)  # enter water type

        def waterclass_selected(event):
            msg = f'You selected {self.waterclass_text.get()}!'
            showinfo(title='Result', message=msg)

        self.waterclass = ('Class 1', 'Class 2', 'Class 3', 'Non-Trout Water')
        self.waterclass_text = tk.StringVar()
        self.waterclasslabel = ttk.Label(
            self, text='Water Class(Trout?):', style='Data.TLabel')
        self.waterclasslabel.grid(column=0, row=5, sticky=tk.W,
                        padx=5, pady=5, ipady=3, ipadx=3)
        self.waterclasslabel_combo = ttk.Combobox(
            self, textvariable=self.waterclass_text)
        self.waterclasslabel_combo['values'] = self.waterclass
        self.waterclasslabel_combo['state'] = 'readonly'
        self.waterclasslabel_combo.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)
        self.waterclasslabel_combo.bind('<<ComboboxSelected>>', waterclass_selected)

    # add species type
        def species_selected(event):
            msg = f'You selected {self.specieslabel_text.get()}!'
            showinfo(title='Result', message=msg)

    # tkinter stuff for species select
        self.species = ('Brown Trout', 'Rainbow Trout', 'Brook Trout', 'Steelhead', 'Lake Run Brown Trout', 'Carp', 'Smallmouth Bass',
               'Largemouth Bass', 'Bluegill', 'Pumpkinseed', 'Perch', 'Walleye', 'Northern Pike', 'Musky', 'Bullhead')
        self.specieslabel_text = tk.StringVar()
        self.specieslabel = ttk.Label(
            self, text='Select Species Caught:', style='Data.TLabel')
        self.specieslabel.grid(column=0, row=2, sticky=tk.W,
                      padx=5, pady=5, ipady=3, ipadx=3)
        self.specieslabel_combo = ttk.Combobox(
            self, textvariable=self.specieslabel_text)
        self.specieslabel_combo['values'] = self.species
        self.specieslabel_combo['state'] = 'readonly'
        self.specieslabel_combo.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)
        self.specieslabel_combo.bind('<<ComboboxSelected>>', species_selected)

    # add calendar date picker
        def pickadate():
            top = tk.Toplevel(master)
            top.geometry('278x154+3+3')
            ttk.Label(top, text='Choose date').pack(padx=10, pady=10)
            cal = DateEntry(top, width=12, background='grey',
                        foreground='white', borderwidth=2, year=2010)
            cal.pack(padx=10, pady=10)
            ttk.Button(top, style='danger.Outline.TButton', text='exit',
                   command=top.destroy).pack(pady=3, padx=3,side='bottom')

        self.datebutton_label = ttk.Label(
            self, text='Select Date:', style='Data.TLabel')
        self.datebutton_label.grid(column=0, row=6, sticky=tk.W,
                          padx=5, pady=5, ipady=3, ipadx=3)
        self.date_button = ttk.Button(
            self, style='info.Outline.TButton', text='Pick Date', command=pickadate)
        self.date_button.grid(column=1, row=6, sticky=tk.EW,
                     padx=5, pady=5, ipadx=1, ipady=1)

                     



class rightside_frame(ttk.LabelFrame):
    def __init__(self,master):
        ttk.LabelFrame.__init__(self, master,text='Place Data', labelanchor='n')
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)

        # create combo box for access type i.e. public, row, private
        def access_selected(event):
            msg = f'You selected {self.accesslabel_text.get()}!'
            showinfo(title='Result', message=msg)

        self.accesslabel_text = tk.StringVar()
        self.access = ('Public-DNR', 'Public-County',
              'Public-Other', 'ROW-Bridge', 'Private')
        self.accesslabel = ttk.Label(
            self, text='Enter Access Type:', style='Data.TLabel')
        self.accesslabel.grid(column=0, row=1, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
        self.accesslabel_combo = ttk.Combobox(
            self, textvariable=self.accesslabel_text)
        self.accesslabel_combo['values'] = self.access
        self.accesslabel_combo['state'] = 'readonly'
        self.accesslabel_combo.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)
        self.accesslabel_combo.bind('<<ComboboxSelected>>', access_selected)

        # add county select chunk
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
        self.countylabel.grid(column=0, row=2, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
        self.countylabel_combo = ttk.Combobox(
            self, textvariable=self.countylabel_text)
        self.countylabel_combo['values'] = self.county
        self.countylabel_combo['state'] = 'readonly'
        self.countylabel_combo.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)
        self.countylabel_combo.bind('<<ComboboxSelected>>', county_selected)

        # create combo box for access type i.e. public, row, private
        def access_selected(event):
            msg = f'You selected {self.accesslabel_text.get()}!'
            showinfo(title='Result', message=msg)

        self.accesslabel_text = tk.StringVar()
        self.access = ('Public-DNR', 'Public-County',
              'Public-Other', 'ROW-Bridge', 'Private')
        self.accesslabel = ttk.Label(
            self, text='Enter Access Type:', style='Data.TLabel')
        self.accesslabel.grid(column=0, row=3, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
        self.accesslabel_combo = ttk.Combobox(
            self, textvariable=self.accesslabel_text)
        self.accesslabel_combo['values'] = self.access
        self.accesslabel_combo['state'] = 'readonly'
        self.accesslabel_combo.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)
        self.accesslabel_combo.bind('<<ComboboxSelected>>', access_selected)

        # combo box for ownership type i.e public, private, state, county, local, nonprofit etc
        def ownership_selected(event):
            msg = f'You selected {self.ownershiptype_text.get()}!'
            showinfo(title='Result', message=msg)

        self.ownershiptype_text = tk.StringVar()
        self.ownership = ('Public-State', 'Public-County', 'Public-Local',
                 'Private-Permission', 'Private-With Easement', 'Private-Public(i.e.MFL Open)')
        self.ownershiplabel = ttk.Label(self, text='Enter Owner Type:')
        self.ownershiplabel.grid(column=0, row=3, sticky=tk.W,
                        padx=5, pady=5, ipady=3, ipadx=3)
        self.ownershiplabel_combo = ttk.Combobox(
            self, textvariable=self.ownershiptype_text)
        self.ownershiplabel_combo['values'] = self.ownership
        self.ownershiplabel_combo['state'] = 'readonly'
        self.ownershiplabel_combo.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)
        self.ownershiplabel_combo.bind('<<ComboboxSelected>>', ownership_selected)

    # create a entry box for name of acces. i.e CTY HWY T access or HWY 21 access on w br of wh
        self.accessnamelabel_text = tk.StringVar()
        self.accesslabel = ttk.Label(self, text='Enter Access Name:',
                            style='Data.TLabel')
        self.accesslabel.grid(column=0, row=4, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
        self.accesslabel_entry = ttk.Entry(
            self, takefocus=0, cursor='hand1', textvariable=self.accessnamelabel_text)
        self.accesslabel_entry.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)
class tableside_frame(ttk.LabelFrame):
    def __init__(self,master):
        ttk.LabelFrame.__init__(self, master,text='Table Data', labelanchor='n')
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title('ASDF')
        self.geometry('800x600+295+55')
        self.iconbitmap('./assets/favicon_sa.ico')
        self.resizable(True,True)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=0)
        self.columnconfigure(2,weight=1)
        self.style = Style(theme='spiritfallsdk3', themes_file='C:/Users/suttr/ASDF/themes/ttkbootstrap_themes_dark.json')
        self.style.configure('TLabelframe.Label', font=('Fira Code', 11, 'italic'))
        self.style.configure('TLabel', font=('Fira Code', 9, 'italic'))
        self.style.configure('Data.TLabel', font=('Fira Mono', 8, 'bold'))
        # style.configure('Bottom.TLabelframe', bd=4, bc='Black')
        self.style.configure('Bottom.TLabelframe.Label',
                    font=('Georgia Pro', 9, 'italic'))

        self.close_button = ttk.Button(
        self, style='danger.Outline.TButton', text='Exit', command=self.destroy)
        self.close_button.pack(side='bottom',anchor='s',
                      padx=3, pady=3, ipadx=1, ipady=1)

        self.submit_button = ttk.Button(
        self, style='success.Outline.TButton', text='Submit', command=self.destroy)
        self.submit_button.pack(side='bottom',anchor='n',
                       padx=3, pady=3, ipady=1, ipadx=1)              

        # add our other frames
    # maintain this order of adding frames to keep footer correct        
        self.top_frame = topheader_frame(self)
        self.top_frame.pack(side='top', expand=0, fill='x',
                   ipady=15, ipadx=15, pady=5, padx=5)
        
        self.table_frame = tableside_frame(self)
        self.table_frame.pack(side='bottom', expand=1, fill='both',
                     ipady=3, ipadx=3, pady=5, padx=5)
        self.right_frame = rightside_frame(self)
        self.right_frame.pack(side='right', expand=1, fill='both',
                     ipady=3, ipadx=3, pady=5, padx=5)
        self.left_frame = leftside_frame(self)
        self.left_frame.pack(side='left', expand=1, fill='both',
                    ipady=3, ipadx=3, pady=5, padx=5)            

if __name__ == "__main__":
    app = App()
    app.mainloop()