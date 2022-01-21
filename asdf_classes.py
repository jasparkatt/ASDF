
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *

import folium
import psycopg2
from tkcalendar import DateEntry

from settings import *

# our root window


class DatabaseConn():
    """class to handle      
    postgres db connection stuff"""

    def __init__(self):
        self.conn = psycopg2.connect(
            database=PG_NAME, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Data Entry')
        self.geometry('950x485+5+5')
        self.resizable(True, True)
        self.iconbitmap('./assets/favicon.ico')
        # grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        # self.columnconfigure(4,weight=1)
        self.configure(background='#E5D0CC', relief='sunken')
        # declare and create our style; customize base widget params
        self.style = ttk.Style()
        self.style.theme_create('HotChocolate', parent='',
                                settings={
                                    'TButton': {
                                        'configure': {
                                            'background': '#000000',
                                            'foreground': '#172121',
                                            'font': ('Palatino Linotype', 11),
                                            'anchor': 'center',
                                            'style': 'TButton'
                                        },
                                        'map': {
                                            'foreground': [('pressed', 'red'),
                                                           ('active', 'blue')],
                                            'background': [('pressed', '!disabled', '#ffffff'),
                                                           ('active', '#000000')]
                                        }
                                    },
                                    'TLabel': {
                                        'configure': {
                                            'font': ('Roboto Mono', 9, 'italic'),
                                            'foreground': '#172121',
                                            'relief': 'ridge',
                                            'borderwidth': 4,
                                            'anchor': 'center',
                                            'background': '#F9FBF2'

                                        }
                                    },
                                    'Treeview': {
                                        'configure': {
                                            'font': ('PT Root UI', 9, 'italic bold')

                                        },
                                        'map': {
                                            'background': [('!selected', '#A7A284'),
                                                           ('selected', '#C9B7AD')],
                                            'foreground': [('selected', '#292F36')],
                                            'font': [('selected', ("Modern438Smc", 11, 'bold'))]
                                        }
                                    },
                                    'Treeview.Heading': {
                                        'configure': {
                                            'font': ('Roboto Mono', 10, 'bold'),
                                            'background': '#000000',
                                            'foreground': '#E5E1EE'
                                        }
                                    }


                                })

        self.style.theme_use('HotChocolate')

        # use our DatabaseConnect class to connect to sqlite3 db and initialize table if needed

        # create initial table then comment out but keep it.
        db = DatabaseConn()
        db.query("""CREATE TABLE IF NOT EXISTS asdf_master (
            ID SERIAL PRIMARY KEY,
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
        db.commit()
        db.close()

        # define our query record func for qeury button

        def totreeview():
            self.tree.delete(*self.tree.get_children())
            db = DatabaseConn()
            db.query("SELECT * FROM asdf_master ORDER BY ID")
            for row in db.cur:
                self.tree.insert("", tk.END, values=(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            db.commit()
            db.close()

        # this func below dupes the totreeview func. Turn this into something else.
        def delete():
            # Create a database or connect to one
            db = DatabaseConn()
            db.query("DELETE from asdf_master WHERE id = " +
                     self.delete_box.get())

            # Delete a record
            self.delete_box.delete(0, END)

            # # Commit Changes
            db.commit()
            # # Close Connection
            db.close()

        # define our submit func for the submit button

        def submit():
            db = DatabaseConn()
            sql_bit = """INSERT INTO asdf_master (COUNTY_NM,
            OWNER_TY,
            ACCESS_TY,
            ACCESS_NM,
            WATER_NM,
            WATER_TY,
            WATER_CL,
            SPECIES,
            DATE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            data_bit = (self.countylabel_combo.get(), self.ownershiplabel_combo.get(), self.accesslabel_combo.get(), self.accesslabel_entry.get(
            ), self.streamlabel_entry.get(), self.watertypelabel_combo.get(), self.waterclasslabel_combo.get(), self.specieslabel_combo.get(), self.cal.get())
            # insert new data into our table
            db.cur.execute(sql_bit, data_bit)

            self.streamlabel_entry.delete(0, END)
            self.accesslabel_entry.delete(0, END)

        # commit changes and close conn
            db.commit()
            db.close()

        # create combobox for county selection

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
            self, text='Enter County Name:', style='TLabel')
        self.countylabel.grid(column=0, row=0, sticky=tk.EW,
                              padx=5, pady=5, ipady=3, ipadx=3)
        self.countylabel_combo = ttk.Combobox(
            self, textvariable=self.countylabel_text)
        self.countylabel_combo['values'] = self.county
        self.countylabel_combo['state'] = 'readonly'
        self.countylabel_combo.grid(
            column=1, row=0, sticky=tk.EW, padx=5, pady=5)
        self.countylabel_combo.bind('<<ComboboxSelected>>')

        # enter water body name
        self.streamlabel_text = tk.StringVar()

        self.streamlabel = ttk.Label(
            self, text='Water Fished(Name):', style='TLabel')
        self.streamlabel.grid(column=2, row=0, sticky=tk.EW,
                              padx=5, pady=5, ipady=3, ipadx=3)
        self.streamlabel_entry = ttk.Entry(
            self, takefocus=0, cursor='hand1', textvariable=self.streamlabel_text, style='custom.TEntry')
        self.streamlabel_entry.grid(
            column=3, row=0, sticky=tk.EW, padx=5, pady=5)

        # enter water type

        self.watertypes = ('Cold', 'Cool', 'Warm', 'Cold-Cool', 'Cool-Warm')
        self.watertype_text = tk.StringVar()
        self.watertypelabel = ttk.Label(
            self, text='Water Type(Temp):', style='TLabel')
        self.watertypelabel.grid(column=2, row=2, sticky=tk.EW,
                                 padx=5, pady=5, ipady=3, ipadx=3)
        self.watertypelabel_combo = ttk.Combobox(
            self, textvariable=self.watertype_text)
        self.watertypelabel_combo['values'] = self.watertypes
        self.watertypelabel_combo['state'] = 'readonly'
        self.watertypelabel_combo.grid(
            column=3, row=2, sticky=tk.EW, padx=5, pady=5)
        self.watertypelabel_combo.bind(
            '<<ComboboxSelected>>')  # enter water type

        #  waterclass combo box

        self.waterclass = ('Class 1', 'Class 2', 'Class 3', 'Non-Trout Water')
        self.waterclass_text = tk.StringVar()
        self.waterclasslabel = ttk.Label(
            self, text='Water Class(Trout?):', style='TLabel')
        self.waterclasslabel.grid(column=2, row=3, sticky=tk.EW,
                                  padx=5, pady=5, ipady=3, ipadx=3)
        self.waterclasslabel_combo = ttk.Combobox(
            self, textvariable=self.waterclass_text)
        self.waterclasslabel_combo['values'] = self.waterclass
        self.waterclasslabel_combo['state'] = 'readonly'
        self.waterclasslabel_combo.grid(
            column=3, row=3, sticky=tk.EW, padx=5, pady=5)
        self.waterclasslabel_combo.bind('<<ComboboxSelected>>')

        # tkinter stuff for species select

        self.species = ('Brown Trout', 'Rainbow Trout', 'Brook Trout', 'Steelhead', 'Lake Run Brown Trout', 'Carp', 'Smallmouth Bass',
                        'Largemouth Bass', 'Bluegill', 'Pumpkinseed', 'Perch', 'Walleye', 'Northern Pike', 'Musky', 'Bullhead')
        self.specieslabel_text = tk.StringVar()
        self.specieslabel = ttk.Label(
            self, text='Select Species Caught:', style='TLabel')
        self.specieslabel.grid(column=2, row=1, sticky=tk.EW,
                               padx=5, pady=5, ipady=3, ipadx=3)
        self.specieslabel_combo = ttk.Combobox(
            self, textvariable=self.specieslabel_text)
        self.specieslabel_combo['values'] = self.species
        self.specieslabel_combo['state'] = 'readonly'
        self.specieslabel_combo.grid(
            column=3, row=1, sticky=tk.EW, padx=5, pady=5)
        self.specieslabel_combo.bind('<<ComboboxSelected>>')

        # create combo box for access type i.e. public, row, private

        self.accesslabel_text = tk.StringVar()
        self.access = ('Public-DNR', 'Public-County',
                       'Public-Other', 'ROW-Bridge', 'Private')
        self.accesslabel = ttk.Label(
            self, text='Enter Access Type:', style='TLabel')
        self.accesslabel.grid(column=0, row=2, sticky=tk.EW,
                              padx=5, pady=5, ipady=3, ipadx=3)
        self.accesslabel_combo = ttk.Combobox(
            self, textvariable=self.accesslabel_text)
        self.accesslabel_combo['values'] = self.access
        self.accesslabel_combo['state'] = 'readonly'
        self.accesslabel_combo.grid(
            column=1, row=2, sticky=tk.EW, padx=5, pady=5)
        self.accesslabel_combo.bind('<<ComboboxSelected>>')

    # combo box for ownership type i.e public, private, state, county, local, nonprofit etc

        self.ownershiptype_text = tk.StringVar()
        self.ownership = ('Public-State', 'Public-County', 'Public-Local',
                          'Private-Permission', 'Private-With Easement', 'Private-Public(i.e.MFL Open)')
        self.ownershiplabel = ttk.Label(
            self, text='Enter Owner Type:', style='TLabel')
        self.ownershiplabel.grid(column=0, row=1, sticky=tk.EW,
                                 padx=5, pady=5, ipady=3, ipadx=3)
        self.ownershiplabel_combo = ttk.Combobox(
            self, textvariable=self.ownershiptype_text)
        self.ownershiplabel_combo['values'] = self.ownership
        self.ownershiplabel_combo['state'] = 'readonly'
        self.ownershiplabel_combo.grid(
            column=1, row=1, sticky=tk.EW, padx=5, pady=5)
        self.ownershiplabel_combo.bind('<<ComboboxSelected>>')

    # create a entry box for name of acces.

        self.accessnamelabel_text = tk.StringVar()
        self.accesslabel = ttk.Label(self, text='Enter Access Name:',
                                     style='TLabel')
        self.accesslabel.grid(column=0, row=3, sticky=tk.EW,
                              padx=5, pady=5, ipady=3, ipadx=3)
        self.accesslabel_entry = ttk.Entry(
            self, takefocus=0, cursor='hand1', textvariable=self.accessnamelabel_text)
        self.accesslabel_entry.grid(
            column=1, row=3, sticky=tk.EW, padx=5, pady=5)

        # create delete box
        self.delete_box = ttk.Entry(self)
        self.delete_box.grid(column=1, row=8, padx=5, pady=5, sticky=tk.EW)
    # create a datepicker from tkcalender.
    # add calendar date picker

        def pickadate():
            self.top = tk.Toplevel()
            self.top.geometry('278x154+3+3')
            ttk.Label(self.top, text='Choose date').pack(padx=10, pady=10)
            self.cal = DateEntry(self.top, width=12, background='grey',
                                 foreground='white', borderwidth=2, year=2022)
            self.cal.pack(padx=10, pady=10)
            self.cal.bind("<<DateEntrySelected>>")
            ttk.Button(self.top, text='Exit',
                       command=self.top.destroy).pack(pady=3, padx=3, side='bottom')

        # add an exit button
        self.close_button = ttk.Button(
            self, text='Exit', command=self.destroy)
        self.close_button.grid(column=0, row=5, sticky=tk.EW,
                               padx=5, pady=5)

        # add date picker button
        self.date_button = ttk.Button(
            self, text='Pick Date', command=pickadate)
        self.date_button.grid(column=0, row=4, sticky=tk.EW,
                              padx=5, pady=5)

        # add a query button
        self.query_button = ttk.Button(
            self, text='Select Records', command=totreeview)
        self.query_button.grid(column=3, row=4, sticky=tk.EW, columnspan=2,
                               padx=5, pady=5)

        # add submit button
        self.submit_button = ttk.Button(
            self, text='Submit Records', command=submit)
        self.submit_button.grid(column=3, row=5, sticky=tk.EW,
                                padx=5, pady=5)

        self.delete_button = ttk.Button(
            self, text='Delete Record(By ID)', command=delete)
        self.delete_button.grid(column=1, row=9, padx=2, pady=2, sticky=tk.EW)

        # create our treeview for the totreevirw func
        self.columns = ('ID', 'COUNTY_NM', 'OWNER_TY', 'ACCESS_TY', 'ACCESS_NM',
                        'WATER_NM', 'WATER_TY', 'WATER_CL', 'SPECIES', 'DATE')
        self.tree = ttk.Treeview(columns=self.columns,
                                 show='headings', style='Treeview', takefocus=True, selectmode='browse')
        for self.column in self.columns:
            self.tree.column(self.column, anchor=CENTER, width=230)

        # declare our treeview headers
        self.tree.heading('ID', text='ID')
        self.tree.heading('COUNTY_NM', text='County')
        self.tree.heading('OWNER_TY', text='Owner Type')
        self.tree.heading('ACCESS_TY', text='Access Type')
        self.tree.heading('ACCESS_NM', text='Access Name')
        self.tree.heading('WATER_NM', text='Water Name')
        self.tree.heading('WATER_TY', text='Water Type')
        self.tree.heading('WATER_CL', text='Water Class')
        self.tree.heading('SPECIES', text='Fish Caught')
        self.tree.heading('DATE', text='Date')
        self.tree.grid(row=6, columnspan=4, sticky=tk.NSEW,
                       padx=3, pady=3, ipadx=1, ipady=1)

        # add horz and vert scroll bars to treeview
        self.treescrollbarh = ttk.Scrollbar(
            self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.treescrollbarh.set, height=6)
        self.treescrollbarh.grid(row=7, columnspan=4, sticky=tk.EW, rowspan=1)

        self.treescrollbarv = ttk.Scrollbar(
            self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treescrollbarv.set)
        self.treescrollbarv.grid(
            column=5, columnspan=5, sticky=tk.NS, row=6, rowspan=1)

        

if __name__ == "__main__":
    app = App()
    app.mainloop()
