import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkcalendar import DateEntry
from settings import *
import psycopg2
from PIL import Image, ImageTk
import tkinter.font as TkFont


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


class MyButton(ttk.Button):
    def __init__(self, master, **kwargs):
        # Defaults note these are 'TK' params, available params
        # differ betwen 'TK' and 'TTK' for most widgets
        # kwargs['bg'] = 'gold'
        # kwargs['fg'] = 'cadet blue'
        super().__init__(master, **kwargs)


class MyLabel(ttk.Label):
    def __init__(self, master, **kwargs):
        # defaults note these are 'TTK' params
        # kwargs['anchor'] = tk.E
        # kwargs['background'] = 'cadet blue'
        # kwargs['borderwidth'] = '4'
        # kwargs['relief'] = 'groove'
        # kwargs['font'] = ['Roboto Mono', 9, 'italic']
        # kwargs['foreground'] = 'gold'
        # kwargs['takefocus'] = 'True'
        # kwargs['padding'] = '2 2 3 3'
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


class MyEntry(ttk.Entry):
    """my entry widget class"""

    def __init__(self, master, **kwargs):
        kwargs['font'] = ['Anonymous Pro', 9, 'italic']
        kwargs['cursor'] = 'left_side'
        super().__init__(master, **kwargs)


class App(tk.Tk):
    """master class to rule all others"""

    def __init__(self):
        tk.Tk.__init__(self)
        # this will set all frames to this size; will no longer dynamic resize
        self.title('ASDF Journal')
        self.geometry('')
        self.resizable(False, False)
        self.style = ttk.Style(self)
        self._frame = None
        self.switch_frame(HomePage)

        self.style = ttk.Style()
        self.style.theme_create('SpiritFalls', parent='vista',
                                settings={
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
                                    },
                                    'TEntry': {
                                        'configure': {
                                            'cursor': 'hand2',
                                            'foreground': '#373f51',
                                            'background': '#d9d9d9',
                                            'anchor': 'center',
                                            'padding': '2 2 3 3'
                                        }
                                    },
                                    'TButton': {
                                        'configure': {
                                            'background': '#d9d9d9',
                                            'foreground': '#373f51',
                                            'font': ('Cousine', 9, 'italic'),
                                            'anchor': 'center',
                                            'padding': '2 2 3 3'

                                        },
                                        'map': {
                                            'foreground': [('pressed', '#F7717D'), ('active', '#7F2982')],
                                            'background': [('pressed', '!disabled', 'black'), ('active', 'white')]
                                        }
                                    },
                                    'Heading.TLabel': {
                                        'configure': {
                                            'font': ('Cutive Mono', 15, 'bold'),
                                            'foreground': '#373f51',
                                            'background': '#d9d9d9',
                                            'anchor': 'center',
                                            'padding': '0 0 0 30'
                                        }
                                    },
                                    'TLabel': {
                                        'configure': {
                                            'font': ('Anonymous Pro', 9, 'italic'),
                                            'foreground': '#373f51',
                                            'background': '#d9d9d9',
                                            'anchor': 'center',
                                            'padding': '2 2 3 3',
                                            'relief': 'raised'
                                        }
                                    },

                                })
        self.style.theme_use('SpiritFalls')

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        # this resets geometry on each swithc, i think overides geometry kwarg (if set) from above.
        self.winfo_toplevel().geometry("")
        self._frame.grid()


class HomePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        # self.columnconfigure(2,weight=1)
        self.configure(background='orange')

        # set up img stuff and put it in a label
        img = ImageTk.PhotoImage(Image.open(
            './assets/sna.JPG').resize((700, 500), Image.ANTIALIAS))
        label = MyLabel(self, text="ASDF Home Page", image=img,
                        compound='bottom', style='Heading.TLabel')
        # Keep a reference in case this code put is in a function.
        label.img = img
        label.place(relx=0.5, rely=0.5)
        label.grid(column=0, row=0, columnspan=3)

        # logic

        MyButton(self, style='TButton', cursor='hand1', text="Open Data Page",
                 command=lambda: master.switch_frame(DataPage)).grid(row=2, column=0, columnspan=1, sticky=tk.EW)
        MyButton(self, style='TButton', cursor='hand1', text="Open Map Page",
                 command=lambda: master.switch_frame(MapPage)).grid(row=2, column=1, columnspan=1, sticky=tk.EW)

        # shows how each frame resizes
        # my_text = MyText(self, height=2, width=10)
        # my_text.grid(row=1, columnspan=3, sticky=tk.EW)


class DataPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        # self.columnconfigure(4, weight=1)
        # self.columnconfigure(5, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        # self.configure(background='#FAF7E7')

        # create a font just for entry box. Cant do it thru ttk.style('TEntry) for some reason
        entry_font = TkFont.Font(
            family='Overpass Mono', size=10, weight='normal', slant='italic')

        # set up img stuff and put it in a label
        img = ImageTk.PhotoImage(Image.open(
            './assets/TUCaresphoto.jpg').resize((800, 420), Image.ANTIALIAS))
        label = MyLabel(self, text="ASDF Data Page", image=img,
                        compound='bottom', style='Heading.TLabel')
        # Keep a reference in case this code put is in a function.
        label.img = img
        label.place(relx=0.5, rely=0.5)
        label.grid(column=0, row=0, columnspan=5, rowspan=9)
        # do stuff here/logic
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

        # update a record
        def update_record():
            # get hilited record in treeview
            # selected = self.tree.focus()
            # update tht record
            # self.tree.item(selected, text = "", values = ("""put all yuor variables here from form"""))
            pass

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
        self.countylabel = MyLabel(
            self, text='Enter County Name:', style='TLabel').grid(column=0, row=4, sticky=tk.EW,
                                                                  padx=1, pady=1, ipady=1, ipadx=1)
        self.countylabel_combo = ttk.Combobox(
            self, textvariable=self.countylabel_text)
        self.countylabel_combo['values'] = self.county
        self.countylabel_combo['state'] = 'readonly'
        self.countylabel_combo.grid(
            column=1, row=4, sticky=tk.EW, ipadx=1, ipady=1, padx=1, pady=1)
        self.countylabel_combo.bind('<<ComboboxSelected>>')

        # enter water body name
        self.streamlabel_text = tk.StringVar()

        self.streamlabel = MyLabel(
            self, text='Water Fished(Name):', style='TLabel').grid(column=2, row=1, sticky=tk.EW,
                                                                   padx=1, pady=1, ipady=1, ipadx=1)
        self.streamlabel_entry = MyEntry(
            self, takefocus=0, cursor='hand1', textvariable=self.streamlabel_text, style='TEntry').grid(
            column=3, row=1, sticky=tk.EW, ipadx=1, ipady=1, padx=1, pady=1)

        # enter water type
        self.watertype_text = tk.StringVar()
        self.watertypes = ('Cold', 'Cool', 'Warm', 'Cold-Cool', 'Cool-Warm')

        self.watertypelabel = MyLabel(
            self, text='Water Type(Temp):', style='TLabel').grid(column=0, row=2, sticky=tk.EW,
                                                                 padx=1, pady=1, ipady=1, ipadx=1)
        self.watertypelabel_combo = ttk.Combobox(
            self, textvariable=self.watertype_text)
        self.watertypelabel_combo['values'] = self.watertypes
        self.watertypelabel_combo['state'] = 'readonly'
        self.watertypelabel_combo.grid(
            column=1, row=2, sticky=tk.EW, ipadx=1, ipady=1, padx=1, pady=1)
        self.watertypelabel_combo.bind(
            '<<ComboboxSelected>>')  # enter water type

        #  waterclass combo box

        self.waterclass = ('Class 1', 'Class 2', 'Class 3', 'Non-Trout Water')
        self.waterclass_text = tk.StringVar()
        self.waterclasslabel = MyLabel(
            self, text='Water Class(Trout?):', style='TLabel').grid(column=2, row=2, sticky=tk.EW,
                                                                    padx=1, pady=1, ipady=1, ipadx=1)
        self.waterclasslabel_combo = ttk.Combobox(
            self, textvariable=self.waterclass_text)
        self.waterclasslabel_combo['values'] = self.waterclass
        self.waterclasslabel_combo['state'] = 'readonly'
        self.waterclasslabel_combo.grid(
            column=3, row=2, sticky=tk.EW, ipadx=1, ipady=1, padx=1, pady=1)
        self.waterclasslabel_combo.bind('<<ComboboxSelected>>')

        # tkinter stuff for species select

        self.species = ('Brown Trout', 'Rainbow Trout', 'Brook Trout', 'Steelhead', 'Lake Run Brown Trout', 'Carp', 'Smallmouth Bass',
                        'Largemouth Bass', 'Bluegill', 'Pumpkinseed', 'Perch', 'Walleye', 'Northern Pike', 'Musky', 'Bullhead')
        self.specieslabel_text = tk.StringVar()
        self.specieslabel = MyLabel(
            self, text='Select Species Caught:', style='TLabel').grid(column=0, row=3, sticky=tk.EW,
                                                                      padx=1, pady=1, ipady=1, ipadx=1)
        self.specieslabel_combo = ttk.Combobox(
            self, textvariable=self.specieslabel_text)
        self.specieslabel_combo['values'] = self.species
        self.specieslabel_combo['state'] = 'readonly'
        self.specieslabel_combo.grid(
            column=1, row=3, sticky=tk.EW, ipadx=1, ipady=1, padx=1, pady=1)
        self.specieslabel_combo.bind('<<ComboboxSelected>>')

        # create combo box for access type i.e. public, row, private

        self.accesslabel_text = tk.StringVar()
        self.access = ('Public-DNR', 'Public-County',
                       'Public-Other', 'ROW-Bridge', 'Private')
        self.accesslabel = MyLabel(
            self, text='Enter Access Type:', style='TLabel').grid(column=2, row=4, sticky=tk.EW,
                                                                  padx=1, pady=1, ipady=1, ipadx=1)
        self.accesslabel_combo = ttk.Combobox(
            self, textvariable=self.accesslabel_text)
        self.accesslabel_combo['values'] = self.access
        self.accesslabel_combo['state'] = 'readonly'
        self.accesslabel_combo.grid(
            column=3, row=4, sticky=tk.EW, ipadx=1, ipady=1, padx=1, pady=1)
        self.accesslabel_combo.bind('<<ComboboxSelected>>')

    # combo box for ownership type i.e public, private, state, county, local, nonprofit etc

        self.ownershiptype_text = tk.StringVar()
        self.ownership = ('Public-State', 'Public-County', 'Public-Local',
                          'Private-Permission', 'Private-With Easement', 'Private-Public(i.e.MFL Open)')
        self.ownershiplabel = MyLabel(
            self, text='Enter Owner Type:', style='TLabel').grid(column=2, row=3, sticky=tk.EW,
                                                                 padx=1, pady=1, ipady=1, ipadx=1)
        self.ownershiplabel_combo = ttk.Combobox(
            self, textvariable=self.ownershiptype_text)
        self.ownershiplabel_combo['values'] = self.ownership
        self.ownershiplabel_combo['state'] = 'readonly'
        self.ownershiplabel_combo.grid(
            column=3, row=3, sticky=tk.EW, ipadx=1, ipady=1, padx=1, pady=1)
        self.ownershiplabel_combo.bind('<<ComboboxSelected>>')

    # create a entry box for name of acces.

        self.accessnamelabel_text = tk.StringVar()
        self.accesslabel = MyLabel(self, text='Enter Access Name:',
                                   style='TLabel').grid(column=0, row=1, sticky=tk.EW,
                                                        padx=1, pady=1, ipady=1, ipadx=1)
        self.accesslabel_entry = MyEntry(
            self, takefocus=0, cursor='hand1', textvariable=self.accessnamelabel_text, style='TEntry').grid(
            column=1, row=1, sticky=tk.EW, ipadx=1, ipady=1, padx=1, pady=1)

        # create delete box
        self.delete_box = MyEntry(self, style='TEntry', cursor='lft_ptr').grid(
            column=3, row=5, ipadx=1, ipady=1, padx=1, pady=1, sticky=tk.EW)

        def pickadate():
            self.top = tk.Toplevel()
            self.top.geometry('278x154+3+3')
            MyLabel(self.top, text='Choose date').pack(padx=5, pady=5)
            self.cal = DateEntry(self.top, width=12, background='grey',
                                 foreground='white', borderwidth=2, year=2022)
            self.cal.pack(padx=10, pady=10)
            self.cal.bind("<<DateEntrySelected>>")
            MyButton(self.top, text='Exit',
                     command=self.top.destroy).pack(pady=1, padx=1, side='bottom')

        # add an exit button
        self.submit_button = MyButton(
            self, text='Submit', command=submit).grid(column=0, row=6, sticky=tk.EW,
                                                      padx=1, pady=1)

        # add date picker button
        self.date_button = MyButton(
            self, text='Pick Date', command=pickadate).grid(column=1, row=6, sticky=tk.EW,
                                                            padx=1, pady=1)

        # add a query button
        self.query_button = MyButton(
            self, text='Select Records', command=totreeview).grid(column=2, row=6, sticky=tk.EW, columnspan=2,
                                                                  padx=1, pady=1)

        # add a query button
        self.update_button = MyButton(
            self, text='Update Records', command=update_record).grid(column=3, row=6, sticky=tk.EW, columnspan=2,
                                                                     padx=1, pady=1)

        self.delete_button = MyButton(
            self, text='Delete Record(By ID)', command=delete).grid(column=2, row=5, padx=1, pady=1, sticky=tk.EW)

        MyButton(self, style='Home.TButton', text="ASDF Home Page",
                 command=lambda: master.switch_frame(HomePage)).grid(row=7, column=1, columnspan=1, padx=1, pady=1, sticky=tk.EW)

        MyButton(self, style='Home.TButton', text="ASDF Map Page",
                 command=lambda: master.switch_frame(MapPage)).grid(row=7, column=0, columnspan=1, padx=1, pady=1, sticky=tk.EW)

        # shows how each frame resizes
        # create our treeview for the totreevirw func
        self.columns = ('ID', 'COUNTY_NM', 'OWNER_TY', 'ACCESS_TY', 'ACCESS_NM',
                        'WATER_NM', 'WATER_TY', 'WATER_CL', 'SPECIES', 'DATE')
        self.tree = ttk.Treeview(self, columns=self.columns,
                                 show='headings', style='Treeview', takefocus=True, selectmode='browse')
        # for self.column in self.columns:
        #     self.tree.column(self.column, anchor=CENTER)

        # declare our treeview headers
        self.tree.heading('ID', text='ID')
        self.tree.column('ID', minwidth=0, width=2, anchor=CENTER)
        self.tree.heading('COUNTY_NM', text='County')
        self.tree.column('COUNTY_NM', minwidth=0, width=7, anchor=CENTER)
        self.tree.heading('OWNER_TY', text='Owner Type')
        self.tree.column('OWNER_TY', minwidth=0, width=15, anchor=CENTER)
        self.tree.heading('ACCESS_TY', text='Access Type')
        self.tree.column('ACCESS_TY', minwidth=0, width=20, anchor=CENTER)
        self.tree.heading('ACCESS_NM', text='Access Name')
        self.tree.column('ACCESS_NM', minwidth=0, width=25, anchor=CENTER)
        self.tree.heading('WATER_NM', text='Water Name')
        self.tree.column('WATER_NM', minwidth=0, width=35, anchor=CENTER)
        self.tree.heading('WATER_TY', text='Water Type')
        self.tree.column('WATER_TY', minwidth=0, width=12, anchor=CENTER)
        self.tree.heading('WATER_CL', text='Water Class')
        self.tree.column('WATER_CL', minwidth=0, width=8, anchor=CENTER)
        self.tree.heading('SPECIES', text='Fish Caught')
        self.tree.column('SPECIES', minwidth=0, width=10, anchor=CENTER)
        self.tree.heading('DATE', text='Date')
        self.tree.column('DATE', minwidth=0, width=6, anchor=CENTER)
        self.tree.grid(row=8, columnspan=4, sticky=tk.NSEW,
                       padx=1, pady=1, ipadx=1, ipady=1)

        # add horz and vert scroll bars to treeview
        self.treescrollbarh = ttk.Scrollbar(
            self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.treescrollbarh.set, height=4)
        self.treescrollbarh.grid(
            row=9, columnspan=4, sticky=tk.EW, rowspan=1, padx=1, pady=1, ipadx=1, ipady=1)


class MapPage(tk.Canvas):
    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        """page class for mapping our data pts"""

        self.configure(background='gold')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        # set up img stuff and put it in a label
        img = ImageTk.PhotoImage(Image.open(
            './assets/wi.png').resize((500, 350), Image.ANTIALIAS))
        label = MyLabel(self, text="ASDF Home Page", image=img,
                        compound='bottom', style='Heading.TLabel')
        # Keep a reference in case this code put is in a function.
        label.img = img
        label.place(relx=0.5, rely=0.5)
        label.grid(column=0, row=0, columnspan=3)

        def select_cnty():
            pass

        def select_wtrnm():
            pass
        # MyLabel(self, style='TLabel',)
        MyButton(self, style='TButton', text='Select by County', command=select_cnty).grid(
            row=1, column=0, columnspan=1, sticky=tk.EW)

        MyButton(self, style='TButton', text='Select by County', command=select_wtrnm).grid(
            row=1, column=1, columnspan=1, sticky=tk.EW)

        MyButton(self, style='Home.TButton', text="ASDF Home Page",
                 command=lambda: master.switch_frame(HomePage)).grid(row=2, column=0, columnspan=1, sticky=tk.EW)

        MyButton(self, style='Home.TButton', text="ASDF Data Page",
                 command=lambda: master.switch_frame(DataPage)).grid(row=2, column=1, columnspan=1, sticky=tk.EW)


if __name__ == "__main__":
    app = App()
    app.mainloop()
