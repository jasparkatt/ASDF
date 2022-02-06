from cgitb import text
from distutils import command
from re import T
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import font as tkfont
import folium
import psycopg2
from tkcalendar import DateEntry
from PIL import Image, ImageTk

from settings import *




# define db conn class
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

# define Button class
class MyButton(ttk.Button):
    """extend tk.Button class
    style params are mapped in """

    def __init__(self, master, *args, **kwargs):
        ttk.Button.__init__(self, master, *args, **kwargs)

# define label class
class MyLabel(ttk.Label):
    """my label class"""

    def __init__(self, master, *args, **kwargs):
        ttk.Label.__init__(self, master, *args, **kwargs)

# class for entry widget
class MyEntry(ttk.Entry):
    """my entry widget class"""

    def __init__(self, master, *args, **kwargs):
        ttk.Entry.__init__(self, master, *args, **kwargs)
        

# our root window
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.view_font = tkfont.Font(family='Tahoma', size=8, slant='italic',weight='normal')
        self.entry_font = tkfont.Font(family='PT Root UI', size=9, weight="bold", slant="italic")
        self.title_font = tkfont.Font(family='Overpass Mono', size=16, weight="bold", slant="italic")
        self.title('ASDF Journal')
        self.iconbitmap('./assets/favicon.ico')
        self.resizable(True,True)

        # create our style
        self.style = ttk.Style()
        self.style.theme_create('HotChocolate', parent='winnative',
                                settings={
                                    'TButton': {
                                        'configure': {
                                            'background': '#F9FBF2',
                                            'foreground': '#172121',
                                            'font': ('Palatino Linotype', 11),
                                            'anchor': 'center'
                                        },
                                        'map': {
                                            'foreground': [('pressed', 'red'),
                                                           ('active', 'blue')],
                                            'background': [('pressed', '!disabled', '#ffffff'),
                                                           ('active', '#F0F2A6')]
                                        }
                                    },
                                    'TLabel': {
                                        'configure': {
                                            'font': ('Roboto Mono', 9, 'italic'),
                                            'foreground': '#172121',
                                            'relief': 'ridge',
                                            'borderwidth': 2,
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
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = ttk.Frame(self)
        container.grid(column=0,row=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, DataPage, DataViewPage, MapPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()


class HomePage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)

        # set up img stuff and put it in a label         
        img = ImageTk.PhotoImage(Image.open('./assets/sna.JPG').resize((700,500), Image.ANTIALIAS))
        label = MyLabel(self, text="ASDF Home Page", font=controller.title_font, image=img, compound='bottom')
        label.img = img  # Keep a reference in case this code put is in a function.
        label.place(relx=0.5, rely=0.5)
        label.grid(column=0,row=0, columnspan=3)

        # add buttons
        goto_view_btn = MyButton(self,text='Go view the Data',
                            command=lambda: controller.show_frame("DataViewPage"))
        goto_data_btn = MyButton(self, text="Go to the Data Entry Page",
                            command=lambda: controller.show_frame("DataPage"))
        goto_map_btn = MyButton(self, text="Go to the Map Page",
                            command=lambda: controller.show_frame("MapPage"))
        goto_data_btn.grid(column=0,row=2,sticky=tk.EW)
        goto_map_btn.grid(column=1,row=2,sticky=tk.EW)
        goto_view_btn.grid(column=2,row=2, sticky=tk.EW)


class DataViewPage(ttk.Frame):
    """class for our treeview viewing pleasure"""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        label = MyLabel(self, text="ASDF Data Views", font=controller.title_font)
        label.grid(column=0,row=0, columnspan=5, sticky=tk.EW)

        # do something here insert into our treeview
        # define our query record func for qeury button
        # define our Treeview
        def totreeview():
            my_entry = tk.Text(self,height=10,wrap='char',width=100)
            my_entry.grid(column=0,row=1,rowspan=1)
            db = DatabaseConn()
            db.query("SELECT * FROM asdf_master ORDER BY ID")
            for row in db.cur:
                my_entry.insert('1.0',row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                # self.tree.insert("", tk.END, values=(
                #     row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            db.commit()
            db.close()

         
        

            
      

        # create and place  our 'navigation' buttons
        # add a query button

        query_button = MyButton(self, text='Select All', command=totreeview)
        
        goto_home_btn = MyButton(self, text="Back to the Home Page",
                           command=lambda: controller.show_frame("HomePage"))
        
        goto_data_btn = MyButton(self, text="Go to the Data Entry Page",
                            command=lambda: controller.show_frame("DataPage"))
        goto_map_btn = MyButton(self, text="Go to the Map Page",
                            command=lambda: controller.show_frame("MapPage"))
        query_button.grid(column=0, row=4, sticky=tk.EW,
                               padx=5, pady=5)
        goto_home_btn.grid(column=0,row=3,sticky=tk.EW)                    
        goto_data_btn.grid(column=1,row=3,sticky=tk.EW)
        goto_map_btn.grid(column=2,row=3,sticky=tk.EW)


class DataPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4,weight=1)
        label = MyLabel(self, text="ASDF Data Entry", font=controller.title_font)
        label.grid(column=0,row=0, columnspan=5, sticky=tk.EW)

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
        self.countylabel = MyLabel(
            self, text='Enter County Name:', style='TLabel')
        self.countylabel.grid(column=0, row=1, sticky=tk.EW,
                              padx=5, pady=5, ipady=3, ipadx=3)
        self.countylabel_combo = ttk.Combobox(
            self, textvariable=self.countylabel_text)
        self.countylabel_combo['values'] = self.county
        self.countylabel_combo['state'] = 'readonly'
        self.countylabel_combo.grid(
            column=1, row=1, sticky=tk.EW, padx=5, pady=5)
        self.countylabel_combo.bind('<<ComboboxSelected>>')

        # enter water body name
        self.streamlabel_text = tk.StringVar()

        self.streamlabel = MyLabel(
            self, text='Water Fished(Name):', style='TLabel')
        self.streamlabel.grid(column=2, row=1, sticky=tk.EW,
                              padx=5, pady=5, ipady=3, ipadx=3)
        self.streamlabel_entry = MyEntry(
            self, takefocus=0, cursor='hand1', textvariable=self.streamlabel_text, style='custom.TEntry')
        self.streamlabel_entry.grid(
            column=3, row=1, sticky=tk.EW, padx=5, pady=5)

        # enter water type

        self.watertypes = ('Cold', 'Cool', 'Warm', 'Cold-Cool', 'Cool-Warm')
        self.watertype_text = tk.StringVar()
        self.watertypelabel = MyLabel(
            self, text='Water Type(Temp):', style='TLabel')
        self.watertypelabel.grid(column=2, row=3, sticky=tk.EW,
                                 padx=5, pady=5, ipady=3, ipadx=3)
        self.watertypelabel_combo = ttk.Combobox(
            self, textvariable=self.watertype_text)
        self.watertypelabel_combo['values'] = self.watertypes
        self.watertypelabel_combo['state'] = 'readonly'
        self.watertypelabel_combo.grid(
            column=3, row=3, sticky=tk.EW, padx=5, pady=5)
        self.watertypelabel_combo.bind(
            '<<ComboboxSelected>>')  # enter water type

        #  waterclass combo box

        self.waterclass = ('Class 1', 'Class 2', 'Class 3', 'Non-Trout Water')
        self.waterclass_text = tk.StringVar()
        self.waterclasslabel = MyLabel(
            self, text='Water Class(Trout?):', style='TLabel')
        self.waterclasslabel.grid(column=2, row=4, sticky=tk.EW,
                                  padx=5, pady=5, ipady=3, ipadx=3)
        self.waterclasslabel_combo = ttk.Combobox(
            self, textvariable=self.waterclass_text)
        self.waterclasslabel_combo['values'] = self.waterclass
        self.waterclasslabel_combo['state'] = 'readonly'
        self.waterclasslabel_combo.grid(
            column=3, row=4, sticky=tk.EW, padx=5, pady=5)
        self.waterclasslabel_combo.bind('<<ComboboxSelected>>')

        # tkinter stuff for species select

        self.species = ('Brown Trout', 'Rainbow Trout', 'Brook Trout', 'Steelhead', 'Lake Run Brown Trout', 'Carp', 'Smallmouth Bass',
                        'Largemouth Bass', 'Bluegill', 'Pumpkinseed', 'Perch', 'Walleye', 'Northern Pike', 'Musky', 'Bullhead')
        self.specieslabel_text = tk.StringVar()
        self.specieslabel = MyLabel(
            self, text='Select Species Caught:', style='TLabel')
        self.specieslabel.grid(column=2, row=2, sticky=tk.EW,
                               padx=5, pady=5, ipady=3, ipadx=3)
        self.specieslabel_combo = ttk.Combobox(
            self, textvariable=self.specieslabel_text)
        self.specieslabel_combo['values'] = self.species
        self.specieslabel_combo['state'] = 'readonly'
        self.specieslabel_combo.grid(
            column=3, row=2, sticky=tk.EW, padx=5, pady=5)
        self.specieslabel_combo.bind('<<ComboboxSelected>>')

        # create combo box for access type i.e. public, row, private

        self.accesslabel_text = tk.StringVar()
        self.access = ('Public-DNR', 'Public-County',
                       'Public-Other', 'ROW-Bridge', 'Private')
        self.accesslabel = MyLabel(
            self, text='Enter Access Type:', style='TLabel')
        self.accesslabel.grid(column=0, row=3, sticky=tk.EW,
                              padx=5, pady=5, ipady=3, ipadx=3)
        self.accesslabel_combo = ttk.Combobox(
            self, textvariable=self.accesslabel_text)
        self.accesslabel_combo['values'] = self.access
        self.accesslabel_combo['state'] = 'readonly'
        self.accesslabel_combo.grid(
            column=1, row=3, sticky=tk.EW, padx=5, pady=5)
        self.accesslabel_combo.bind('<<ComboboxSelected>>')

    # combo box for ownership type i.e public, private, state, county, local, nonprofit etc

        self.ownershiptype_text = tk.StringVar()
        self.ownership = ('Public-State', 'Public-County', 'Public-Local',
                          'Private-Permission', 'Private-With Easement', 'Private-Public(i.e.MFL Open)')
        self.ownershiplabel = MyLabel(
            self, text='Enter Owner Type:', style='TLabel')
        self.ownershiplabel.grid(column=0, row=2, sticky=tk.EW,
                                 padx=5, pady=5, ipady=3, ipadx=3)
        self.ownershiplabel_combo = ttk.Combobox(
            self, textvariable=self.ownershiptype_text)
        self.ownershiplabel_combo['values'] = self.ownership
        self.ownershiplabel_combo['state'] = 'readonly'
        self.ownershiplabel_combo.grid(
            column=1, row=2, sticky=tk.EW, padx=5, pady=5)
        self.ownershiplabel_combo.bind('<<ComboboxSelected>>')

    # create a entry box for name of acces.

        self.accessnamelabel_text = tk.StringVar()
        self.accesslabel = MyLabel(self, text='Enter Access Name:',
                                     style='TLabel')
        self.accesslabel.grid(column=0, row=4, sticky=tk.EW,
                              padx=5, pady=5, ipady=3, ipadx=3)
        self.accesslabel_entry = MyEntry(
            self, takefocus=0, cursor='hand1', textvariable=self.accessnamelabel_text, font=controller.entry_font)
        self.accesslabel_entry.grid(
            column=1, row=4, sticky=tk.EW, padx=5, pady=5)

        # create delete box
        self.delete_box = MyEntry(self, font=controller.entry_font)
        self.delete_box.grid(column=3, row=5, padx=5, pady=5, sticky=tk.EW)
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
            MyButton(self.top, text='Exit',
                       command=self.top.destroy).pack(pady=3, padx=3, side='bottom')

        # add an exit button
        self.close_button = MyButton(
            self, text='Exit', command=lambda: controller.show_frame("HomePage"))
        self.close_button.grid(column=0, row=6, sticky=tk.EW,
                               padx=5, pady=5)

        # add date picker button
        self.date_button = MyButton(
            self, text='Pick Date', command=pickadate)
        self.date_button.grid(column=0, row=5, sticky=tk.EW,
                              padx=5, pady=5)

        

        # add submit button
        self.submit_button = MyButton(
            self, text='Submit Records', command=submit)
        self.submit_button.grid(column=3, row=6, sticky=tk.EW,
                                padx=5, pady=5)

        self.delete_button = MyButton(
            self, text='Delete Record(By ID)', command=delete)
        self.delete_button.grid(column=2, row=5, padx=2, pady=2, sticky=tk.EW)

        
        # create initial table then comment out but keep it.
        goto_home_btn = MyButton(self, text="Back to the Home Page",
                           command=lambda: controller.show_frame("HomePage"))
        goto_home_btn.grid(column=0,row=8)


class MapPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0,weight=1)
        label = MyLabel(self, text="ASDF Map Viewer", font=controller.title_font)
        label.grid(column=0,row=0, columnspan=5, sticky=tk.EW)
        # create and place  our 'navigation' buttons
        goto_home_btn = MyButton(self, text="Back to the Home Page",
                           command=lambda: controller.show_frame("HomePage"))
        
        goto_data_btn = MyButton(self, text="Go to the Data Entry Page",
                            command=lambda: controller.show_frame("DataPage"))
        goto_view_btn = MyButton(self, text="Go view the Data",
                            command=lambda: controller.show_frame("DataViewPage"))

        goto_home_btn.grid(column=0,row=3,sticky=tk.EW)                    
        goto_data_btn.grid(column=1,row=3,sticky=tk.EW)
        goto_view_btn.grid(column=2,row=3,sticky=tk.EW)


if __name__ == "__main__":
    app = App()
    app.mainloop()
