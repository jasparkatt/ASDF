import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.constants import CENTER, E, END, LEFT
from ttkbootstrap import Style
from tkcalendar import DateEntry
import sqlite3

# our root window

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Data Entry')
        self.geometry('950x485+5+5')
        self.resizable(True, True)
        self.iconbitmap('./assets/favicon.ico')
        # grid
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)
        #self.columnconfigure(4,weight=1)

        # style from ttkbootstrap
        style = Style(
        theme='light3', themes_file='C:/Users/suttr/ASDF/themes/ttkbootstrap_themes_dark.json')
        # the below is automagically applied to any labelframe label txt
        #self.style.configure('TLabelframe.Label', font=('Fira Code', 11, 'italic'))
        style.configure('Data.TLabel', font=('Fira Code', 8, 'italic'))
        style.configure('Outline.TButton', font=('Overpass Mono', 10))
        #self.style.configure('Bottom.TLabelframe.Label',font=('Georgia Pro', 9, 'italic'))
        style.configure('mystyle.Treeview',anchor='center',font=('Roboto Mono', 9))
        style.configure('mystyle.Treeview.Heading',anchor='center',font=('Cousine', 10,'bold'))

        # example below that works....remove
        # self.style.configure('custom.TEntry', background='green', foreground='white', font=('Helvetica', 24))

        # create func to connect to sqlite3 db and initialize table if needed

        conn = sqlite3.connect('./db/ASDF.db')
        c = conn.cursor()

        # create initial table then comment out but keep it.

        c.execute("""CREATE TABLE IF NOT EXISTS asdf_master (
            COUNTY_NM TEXT,
            OWNER_TY TEXT,
            ACCESS_TY TEXT,
            ACCESS_NM TEXT,
            WATER_NM TEXT,
            WATER_TY TEXT,
            WATER_CL TEXT,
            SPECIES TEXT,
            DATE TEXT
            )""")
        
        # define our delete record func for delete button

        # define our query record func for qeury button
        def totreeview():
            self.tree.delete(*self.tree.get_children())
            conn = sqlite3.connect('./db/ASDF.db')
            c = conn.cursor()

            c.execute("SELECT *,rowid FROM asdf_master ORDER BY rowid")
            for row in c:
                self.tree.insert("",tk.END,values=(row[9], row[0], row[1], row[2],row[3], row[4], row[5],row[6], row[7], row[8]))

            conn.commit()
            conn.close()

        # this func below dupes the totreeview func. Turn this into something else.
        # def queryrecord():
        #     conn = sqlite3.connect('./db/ASDF.db')
        #     c = conn.cursor()

        #     # do our query sql here
        #     c.execute("SELECT *, rowid FROM asdf_master")
        #     records = c.fetchall()
        #     # QA QC print statement. WIll need to figure out how to return this to a treeveiw here.
        #     print(records)


        #     #commit changes and close conn
        #     conn.commit()
        #     conn.close()

        # define our submit func for the submit button

        def submit():
            conn = sqlite3.connect('./db/ASDF.db')
            c = conn.cursor()

            #insert new data into our table
            c.execute("INSERT INTO asdf_master VALUES (:countylabel_combo, :ownershiplabel_combo, :accesslabel_combo, :accesslabel_entry, :streamlabel_entry, :watertypelabel_combo, :waterclasslabel_combo, :specieslabel_combo, :cal)",
                {
                    'countylabel_combo': countylabel_combo.get(),
                    'ownershiplabel_combo': ownershiplabel_combo.get(),
                    'accesslabel_combo': accesslabel_combo.get(),
                    'accesslabel_entry': accesslabel_entry.get(),
                    'streamlabel_entry': streamlabel_entry.get(),
                    'watertypelabel_combo': watertypelabel_combo.get(),
                    'waterclasslabel_combo': waterclasslabel_combo.get(),
                    'specieslabel_combo': specieslabel_combo.get(),
                    'cal': self.cal.get()
                })
            
            streamlabel_entry.delete(0, END)
            accesslabel_entry.delete(0,END)    

        #commit changes and close conn
            conn.commit()
            conn.close()

        
        # create combobox for county selection

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
            self, text='Enter County Name:', style='Data.TLabel')
        countylabel.grid(column=0, row=0, sticky=tk.EW,
                     padx=5, pady=5, ipady=3, ipadx=3)
        countylabel_combo = ttk.Combobox(
            self, textvariable=countylabel_text)
        countylabel_combo['values'] = county
        countylabel_combo['state'] = 'readonly'
        countylabel_combo.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)
        countylabel_combo.bind('<<ComboboxSelected>>')


        # enter water body name
        streamlabel_text = tk.StringVar()
    
        streamlabel = ttk.Label(
            self, text='Water Fished(Name):', style='Data.TLabel')
        streamlabel.grid(column=2, row=0, sticky=tk.EW,
                     padx=5, pady=5, ipady=3, ipadx=3)
        streamlabel_entry = ttk.Entry(
            self, takefocus=0, cursor='hand1', textvariable=streamlabel_text, style='custom.TEntry')
        streamlabel_entry.grid(column=3, row=0, sticky=tk.EW, padx=5, pady=5)

        # enter water type

        watertypes = ('Cold', 'Cool', 'Warm', 'Cold-Cool', 'Cool-Warm')
        watertype_text = tk.StringVar()
        watertypelabel = ttk.Label(
            self, text='Water Type(Temp):', style='Data.TLabel')
        watertypelabel.grid(column=2, row=2, sticky=tk.EW,
                        padx=5, pady=5, ipady=3, ipadx=3)
        watertypelabel_combo = ttk.Combobox(
            self, textvariable=watertype_text)
        watertypelabel_combo['values'] = watertypes
        watertypelabel_combo['state'] = 'readonly'
        watertypelabel_combo.grid(column=3, row=2, sticky=tk.EW, padx=5, pady=5)
        watertypelabel_combo.bind('<<ComboboxSelected>>')  # enter water type

        #  waterclass combo box

        waterclass = ('Class 1', 'Class 2', 'Class 3', 'Non-Trout Water')
        waterclass_text = tk.StringVar()
        waterclasslabel = ttk.Label(
            self, text='Water Class(Trout?):', style='Data.TLabel')
        waterclasslabel.grid(column=2, row=3, sticky=tk.EW,
                        padx=5, pady=5, ipady=3, ipadx=3)
        waterclasslabel_combo = ttk.Combobox(
            self, textvariable=waterclass_text)
        waterclasslabel_combo['values'] = waterclass
        waterclasslabel_combo['state'] = 'readonly'
        waterclasslabel_combo.grid(column=3, row=3, sticky=tk.EW, padx=5, pady=5)
        waterclasslabel_combo.bind('<<ComboboxSelected>>')

        # tkinter stuff for species select
    
        species = ('Brown Trout', 'Rainbow Trout', 'Brook Trout', 'Steelhead', 'Lake Run Brown Trout', 'Carp', 'Smallmouth Bass',
               'Largemouth Bass', 'Bluegill', 'Pumpkinseed', 'Perch', 'Walleye', 'Northern Pike', 'Musky', 'Bullhead')
        specieslabel_text = tk.StringVar()
        specieslabel = ttk.Label(
            self, text='Select Species Caught:', style='Data.TLabel')
        specieslabel.grid(column=2, row=1, sticky=tk.EW,
                      padx=5, pady=5, ipady=3, ipadx=3)
        specieslabel_combo = ttk.Combobox(
            self, textvariable=specieslabel_text)
        specieslabel_combo['values'] = species
        specieslabel_combo['state'] = 'readonly'
        specieslabel_combo.grid(column=3, row=1, sticky=tk.EW, padx=5, pady=5)
        specieslabel_combo.bind('<<ComboboxSelected>>')

        # create combo box for access type i.e. public, row, private
        
        accesslabel_text = tk.StringVar()
        access = ('Public-DNR', 'Public-County',
              'Public-Other', 'ROW-Bridge', 'Private')
        accesslabel = ttk.Label(
            self, text='Enter Access Type:', style='Data.TLabel')
        accesslabel.grid(column=0, row=2, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
        accesslabel_combo = ttk.Combobox(
            self, textvariable=accesslabel_text)
        accesslabel_combo['values'] = access
        accesslabel_combo['state'] = 'readonly'
        accesslabel_combo.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)
        accesslabel_combo.bind('<<ComboboxSelected>>')

    # combo box for ownership type i.e public, private, state, county, local, nonprofit etc
        
        ownershiptype_text = tk.StringVar()
        ownership = ('Public-State', 'Public-County', 'Public-Local',
                 'Private-Permission', 'Private-With Easement', 'Private-Public(i.e.MFL Open)')
        ownershiplabel = ttk.Label(self, text='Enter Owner Type:')
        ownershiplabel.grid(column=0, row=1, sticky=tk.W,
                        padx=5, pady=5, ipady=3, ipadx=3)
        ownershiplabel_combo = ttk.Combobox(
            self, textvariable=ownershiptype_text)
        ownershiplabel_combo['values'] = ownership
        ownershiplabel_combo['state'] = 'readonly'
        ownershiplabel_combo.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)
        ownershiplabel_combo.bind('<<ComboboxSelected>>')

    # create a entry box for name of acces.

        accessnamelabel_text = tk.StringVar()
        accesslabel = ttk.Label(self, text='Enter Access Name:',
                            style='Data.TLabel')
        accesslabel.grid(column=0, row=3, sticky=tk.W,
                     padx=5, pady=5, ipady=3, ipadx=3)
        accesslabel_entry = ttk.Entry(
            self, takefocus=0, cursor='hand1', textvariable=accessnamelabel_text)
        accesslabel_entry.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)
    # create a datepicker from tkcalender.
    # add calendar date picker
        def pickadate():
            self.top = tk.Toplevel()
            self.top.geometry('278x154+3+3')
            ttk.Label(self.top, text='Choose date').pack(padx=10, pady=10)
            self.cal = DateEntry(self.top, width=12, background='grey',
                        foreground='white', borderwidth=2, year=2018)
            self.cal.pack(padx=10, pady=10)
            self.cal.bind("<<DateEntrySelected>>")
            ttk.Button(self.top, style='danger.Outline.TButton', text='Exit',
                   command=self.top.destroy).pack(pady=3, padx=3,side='bottom')


        # add an exit button
        close_button = ttk.Button(
            self, style='danger.Outline.TButton', text='Exit', command=self.destroy)
        close_button.grid(column=0, row=5, sticky=tk.EW,
                      padx=5, pady=5)

        # add date picker button
        date_button = ttk.Button(
            self,style='secondary.Outline.TButton', text='Pick Date', command=pickadate)
        date_button.grid(column=0, row=4, sticky=tk.EW,
                       padx=5, pady=5)

        # add a query button
        query_button = ttk.Button(
            self, style='primary.Outline.TButton', text='Select Records', command=totreeview)
        query_button.grid(column=3, row=4, sticky=tk.EW,columnspan=2,
                       padx=5, pady=5)

        #add submit button
        submit_button = ttk.Button(
            self, style='primary.Outline.TButton', text='Submit Records', command=submit)
        submit_button.grid(column=3, row=5, sticky=tk.EW,
                       padx=5, pady=5)               
        
        #create our treeview for the totreevirw func
        self.columns = ('ROWID', 'COUNTY_NM', 'OWNER_TY', 'ACCESS_TY', 'ACCESS_NM', 'WATER_NM', 'WATER_TY', 'WATER_CL', 'SPECIES', 'DATE')
        self.tree = ttk.Treeview(columns=self.columns, show='headings',style='mystyle.Treeview')
        for self.column in self.columns:
            self.tree.column(self.column, anchor=CENTER, width=230)

        #declare our treeview headers       
        self.tree.heading('ROWID',text='ID')
        self.tree.heading('COUNTY_NM',text='County')
        self.tree.heading('OWNER_TY',text='Owner Type')
        self.tree.heading('ACCESS_TY',text='Access Type')
        self.tree.heading('ACCESS_NM',text='Access Name')
        self.tree.heading('WATER_NM',text='Water Name')
        self.tree.heading('WATER_TY',text='Water Type')
        self.tree.heading('WATER_CL',text='Water Class')
        self.tree.heading('SPECIES',text='Fish Caught')
        self.tree.heading('DATE',text='Date')
        self.tree.grid(row=6,columnspan=4,sticky=tk.NSEW,padx=5,pady=5,ipadx=3,ipady=3)

        # add horz and vert scroll bars to treeview  
        self.treescrollbarh = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(xscrollcommand = self.treescrollbarh.set,height=8)
        self.treescrollbarh.grid(row=7,columnspan=4,sticky=tk.EW, rowspan=1)

        self.treescrollbarv = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand = self.treescrollbarv.set)
        self.treescrollbarv.grid(column=5,columnspan=5, sticky=tk.NS,row=6,rowspan=5)            
                            
        # add a delete button               
                                 
        

        #commit to and close DB 
        conn.commit()
        conn.close()               

if __name__ == "__main__":
    app = App()
    app.mainloop()


