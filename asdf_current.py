import tkinter as tk
from tkinter import ttk, font
from tkinter.constants import *
import sqlite3
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import webbrowser
import folium
from folium import plugins
import pandas as pd
from geopy.geocoders import (
    ArcGIS,
    Bing,
    Geocodio,
    Here,
    HereV7,
    MapBox,
    MapTiler,
    Nominatim,
    OpenCage,
    TomTom,
)
from shapely.geometry import MultiPoint, Point


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
        # kwargs['padding'] = '0 5 5 0'
        super().__init__(master, **kwargs)


class MyText(tk.Text):
    def __init__(self, master, **kwargs):
        kwargs["cursor"] = "hand2"
        kwargs["bg"] = "cadet blue"
        kwargs["bd"] = "4"
        kwargs["relief"] = "groove"
        kwargs["font"] = ["Roboto Mono", 9, "italic"]
        kwargs["fg"] = "gold"
        kwargs["takefocus"] = "True"
        kwargs["padx"] = "2"
        super().__init__(master, **kwargs)


class MyEntry(ttk.Entry):
    def __init__(self, master, **kwargs):
        # default kwargs
        kwargs["justify"] = tk.LEFT
        kwargs["cursor"] = "sb_left_arrow"
        super().__init__(master, **kwargs)


class DatabaseConn:
    """class to handle
    postgres db connection stuff"""

    def __init__(self):
        self.conn = sqlite3.connect("./db/mapping_notes.db")
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


class App(tk.Tk):
    """master class to rule all others"""

    def __init__(self):
        tk.Tk.__init__(self)
        # this will set all frames to this size; will no longer dynamic resize
        # self.geometry('600x400')
        self.title("GIS Helper")
        self.resizable(False, False)
        self.iconbitmap("./assets/favicon.ico")

        self._frame = None
        self.switch_frame(HomePage)
        self.style = ttk.Style(self)
        self.style.theme_create(
            "SpiritFalls",
            parent="vista",
            settings={
                "Treeview": {
                    "configure": {"font": ("PT Root UI", 9, "italic bold")},
                    "map": {
                        "background": [
                            ("!selected", "#A7A284"),
                            ("selected", "#C9B7AD"),
                        ],
                        "foreground": [("selected", "#292F36")],
                        "font": [("selected", ("Modern438Smc", 11, "bold"))],
                    },
                },
                "Treeview.Heading": {
                    "configure": {
                        "font": ("Roboto Mono", 10, "bold"),
                        "background": "#000000",
                        "foreground": "#E5E1EE",
                    }
                },
                "TEntry": {
                    "configure": {
                        "cursor": "hand2",
                        "foreground": "#373f51",
                        "background": "#d9d9d9",
                        "anchor": "center",
                    }
                },
                "TButton": {
                    "configure": {
                        "background": "#d9d9d9",
                        "foreground": "#373f51",
                        "font": ("Cousine", 9, "italic"),
                        "anchor": "center",
                    },
                    "map": {
                        "foreground": [("pressed", "#F7717D"), ("active", "#7F2982")],
                        "background": [
                            ("pressed", "!disabled", "black"),
                            ("active", "white"),
                        ],
                    },
                },
                "Heading.TLabel": {
                    "configure": {
                        "font": ("Cutive Mono", 15, "bold"),
                        "foreground": "#373f51",
                        "background": "sky blue",
                        "anchor": "center",
                        #'padding': '1 1 1 1', #'Left Top Right Bottom'
                        "relief": "flat",
                    }
                },
                "TLabel": {
                    "configure": {
                        "font": ("Anonymous Pro", 10, "italic"),
                        "foreground": "#373f51",
                        "background": "#d9d9d9",
                        "anchor": "center",
                        #'padding': '1 2 1 2',
                        "relief": "raised",
                    }
                },
            },
        )
        self.style.theme_use("SpiritFalls")

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        # this resets geometry on each swithc, i think overides geometry kwarg (if set) from above.
        self._frame.grid()
        self.winfo_toplevel().geometry("")


class HomePage(tk.Canvas):
    def __init__(self, master):
        tk.Canvas.__init__(self, master)

        self.configure(bg="indigo")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        MyLabel(
            self,
            style="Heading.TLabel",
            text="Waupaca County GIS & Addressing",
            background="cadet blue",
        ).grid(row=0, column=0, columnspan=3, sticky=tk.EW, pady=10)
        MyButton(
            self,
            cursor="hand1",
            text="Mapping",
            command=lambda: master.switch_frame(MappingPage),
        ).grid(row=3, column=0, columnspan=1, sticky=tk.EW)
        MyButton(
            self,
            cursor="hand1",
            text="Addressing",
            command=lambda: master.switch_frame(AddressingPage),
        ).grid(row=3, column=1, columnspan=1, sticky=tk.EW)
        MyButton(
            self,
            cursor="hand1",
            text="Notes",
            command=lambda: master.switch_frame(DataPage),
        ).grid(row=3, column=2, columnspan=1, sticky=tk.EW)
        # shows how each frame resizes

        img = ImageTk.PhotoImage(
            Image.open('./assets/sna.JPG').resize((700, 500), Image.ANTIALIAS)
        )
        label = MyLabel(self, image=img, compound="image", style="Heading.TLabel")
        # Keep a reference in case this code put is in a function.
        label.img = img
        label.place(relx=0.5, rely=0.5)
        label.grid(column=0, row=1, columnspan=3)
        MyLabel(self, text="Testing Label Fonts", style="TLabel").grid(
            row=2, columnspan=3, sticky=tk.EW, pady=2
        )


class MappingPage(tk.Canvas):
    def __init__(self, master):
        tk.Canvas.__init__(self, master)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(bg="indigo")
        MyLabel(
            self,
            style="Heading.TLabel",
            cursor="hand1",
            text="Mapping Problems",
            background="cadet blue",
        ).grid(row=0, column=0, columnspan=3, sticky=tk.EW, pady=10)
        MyButton(
            self,
            cursor="hand1",
            text="Home",
            command=lambda: master.switch_frame(HomePage),
        ).grid(row=3, column=0, columnspan=3, sticky=tk.EW)
        img = ImageTk.PhotoImage(
            Image.open("./assets/HomeWater.jpg").resize((400, 300), Image.ANTIALIAS)
        )
        label = MyLabel(self, image=img, compound="image", style="Heading.TLabel")
        # Keep a reference in case this code put is in a function.
        label.img = img
        label.place(relx=0.5, rely=0.5)
        label.grid(column=0, row=1, columnspan=3)
        MyLabel(self, text="Testing Label Fonts", style="TLabel").grid(
            row=2, columnspan=3, sticky=tk.EW, pady=2
        )


class AddressingPage(tk.Canvas):
    def __init__(self, master):
        tk.Canvas.__init__(self, master)

        self.configure(bg="indigo")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # header bar for page
        MyLabel(
            self,
            style="Heading.TLabel",
            text="Reverse Geocode",
            background="cadet blue",
        ).grid(row=0, column=0, columnspan=3, sticky=tk.EW, pady=10)

        img = ImageTk.PhotoImage(
            Image.open("./assets/TUCaresphoto.jpg").resize((650, 500), Image.ANTIALIAS)
        )
        label = MyLabel(self, image=img, compound="image", style="Heading.TLabel")
        # Keep a reference in case this code put is in a function.
        label.img = img
        label.place(relx=0.5, rely=0.5)
        label.grid(column=0, row=1, columnspan=3)

        xvalu = tk.StringVar(value="45.00")
        yvalu = tk.StringVar(value="-90.00")
        # create x,y entry widgets
        x_label = MyLabel(self, style="TLabel", text="Input Lng(X):")
        x_label.grid(column=0, row=2, sticky=tk.EW, columnspan=1)
        x_entry = MyEntry(self, textvariable=xvalu, style="TEntry")
        x_entry.grid(column=1, row=2, sticky=tk.EW, columnspan=1)
        x_entry.focus()
        # y value
        y_label = MyLabel(self, style="TLabel", text="Input Lat(Y):")
        y_label.grid(column=0, row=3, sticky=tk.EW, columnspan=1)
        y_entry = MyEntry(self, textvariable=yvalu, style="TEntry")
        y_entry.grid(column=1, row=3, sticky=tk.EW, columnspan=1)
        y_entry.focus()

        # geopy geocoders
        def geo_coder():
            pd.set_option("display.max_columns", 20)
            pd.set_option("display.width", 2000)
            geocoders = [
                ArcGIS(),
                Here(apikey="WKO8yQIM-Q16v35aon2VUWO8SRnwIBe1d90AVYnyhiA"),
                TomTom(api_key="a6kNGPQpvIqOJAd74MBpZThsgWlXwIub"),
                Bing(
                    api_key="AvF0HgMbtWNEZIGeqoRe23qhLDW106zb-l81BwbXrjruhdr3N3Ws6Ep_dan06wy7"
                ),
                MapBox(
                    api_key="pk.eyJ1IjoiYnVkc3V0dHJlZSIsImEiOiJja2hzNHVwMngwOXFrMnBtdGtqZTJ2YmM4In0.9WAWdGwJ0gG6grCp48jykA"
                ),
                # Nominatim(user_agent='tk_geopy_pd.py', scheme='https'),
                HereV7(apikey="WKO8yQIM-Q16v35aon2VUWO8SRnwIBe1d90AVYnyhiA"),
                # Geocodio(api_key='88818fcfed8c311866226ed6fc435ed6d632d6d'),
                MapTiler(api_key="bxHmq2Gzx41V3hATuN0H"),
                OpenCage(api_key="6dc49d0fe13f40458c6c7b9be560355e"),
            ]

            returned_addr_list = []
            returned_LatLong_list = []
            x_coord = float(xvalu.get())
            y_coord = float(yvalu.get())

            for geocoder in geocoders:
                query = [x_coord, y_coord]
                rvs = geocoder.reverse(query=query)
                addr = rvs.address
                lat = rvs.latitude
                long = rvs.longitude
                returned_addr_list.append([lat, long, geocoder, addr])
                returned_LatLong_list.append([lat, long])

            # collect address, la
            # create a pandas dataframe to hold our collected data in returned_addr_list in table format
            # also used to create individual lists of single components to plug into our mapping latter
            # use shapely module to do some math on our returned lat/long
            # get a 'centroid' value from all returned lat/long in list
            # calc a distance value from user input lat/lng to 'centroid' lat/lng--reference only i guess

            # latlng_list_toMultiPt = MultiPoint(returned_LatLong_list)
            returned_latlng_list_toMultiPt = MultiPoint(returned_LatLong_list).centroid
            cent_pt = Point(returned_latlng_list_toMultiPt)
            addr_list_df = pd.DataFrame(
                returned_addr_list, columns=["lat", "long", "Geocoder", "Addreguess"]
            )

            # create some list and dict for later use from the dataframe
            lat_list = list(addr_list_df["lat"])
            long_list = list(addr_list_df["long"])
            geocoder_list = list(addr_list_df["Geocoder"])
            addr_list = list(addr_list_df["Addreguess"])
            # dist_dict = (dict(zip(geocoder_list, returned_LatLong_list)))

            addr_list_df["Geocoder"] = addr_list_df["Geocoder"].map(
                lambda x: str(x)[22:-30]
            )
            mapping_dict = {
                "s.ArcGIS": "ArcGIS",
                "Here": "Here",
                "m.TomTom": "TomTom",
                "Bing": "Bing",
                "x.MapBox": "Mapbox",
                # "atim.Nominatim":"Nominatim",
                "HereV7": "HereV7",
                # "dio.Geocodio":"Geocodio",
                "ler.MapTiler": "MapTiler",
                "age.OpenCage": "OpenCage",
            }
            addr_list_df["Geocoder"] = addr_list_df["Geocoder"].replace(
                mapping_dict, regex=True
            )

            print(addr_list_df.head(3))

            # map stuff
            attr = ("Esri",)
            name = "Esri Satellite"

            # create folium map using the derived centroid x,y as our 'open to' location
            # declare some other base tiles and add them to the folium map control
            # add the mouse position plug in to easily acquire map coords

            m = folium.Map(
                location=[cent_pt.x, cent_pt.y],
                zoom_start=18,
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{"
                "z}/{y}/{x}",
                attr=attr,
                name=name,
            )
            # m = folium.Map(location=[cent_pt.x, cent_pt.y], zoom_start=18)
            tiles = ["cartodbpositron", "openstreetmap", "cartodbdark_matter"]
            for tile in tiles:
                folium.TileLayer(tile).add_to(m)
            folium.plugins.MousePosition(num_digits=6).add_to(m)
            folium.LayerControl().add_to(m)

            # use the above mentioned lists from the DF to add markers and populate popups and tooltips
            # differentiate between centroid pt and reverse geocoded points with 2 different marker 'sets'
            for lat, long, Addreguess, Geocoder in zip(
                lat_list, long_list, addr_list, geocoder_list
            ):
                m.add_child(
                    folium.CircleMarker(
                        location=[lat, long],
                        tooltip=Geocoder,
                        popup=Addreguess,
                        radius=4,
                        color="purple",
                        fill_color="lightblue",
                        fill_opacity=0.6,
                    )
                )
                m.add_child(
                    folium.Circle(
                        location=[cent_pt.x, cent_pt.y],
                        tooltip="centroid",
                        radius=2,
                        color="darkred",
                        fill_color="orange",
                        fill_opacity=0.6,
                    )
                )
                m.add_child(
                    folium.Marker(
                        location=[x_coord, y_coord],
                        tooltip="User Input",
                        icon=folium.Icon(color="beige", icon="info-sign"),
                    )
                )

            # save and open your generated folium html map
            m.save("paca_geocode.html")

            # # create our treeview for the totreevirw func
            columns = list(addr_list_df)
            tree = ttk.Treeview(
                self, columns=columns, show="headings", style="Treeview"
            )
            # for column in columns:
            #     tree.column(column, anchor=CENTER, width=230)

            # declare our treeview headers
            # for i in columns:
            #     tree.column(i, width=0, minwidth=500, anchor=CENTER,stretch=True)
            #     tree.heading(i, text=i, anchor=CENTER)
            tree.heading("lat", text="Lat", anchor="w")
            tree.column("lat", minwidth=0, width=80, anchor="w")
            tree.heading("long", text="Long", anchor="w")
            tree.column("long", minwidth=0, width=80, anchor="w")
            tree.heading("Geocoder", text="Geocoder", anchor="w")
            tree.column("Geocoder", minwidth=0, width=60, anchor="w")
            tree.heading("Addreguess", text="Addreguess", anchor="w")
            tree.column("Addreguess", minwidth=0, width=400, anchor="w")

            for index, row in addr_list_df.iterrows():
                tree.insert("", 0, text=index, values=list(row))
            tree.grid(row=5, columnspan=3, sticky=tk.NSEW)

            # add horz and vert scroll bars to treeview
            # treescrollbarh = ttk.Scrollbar(
            #     self, orient='horizontal', command=tree.xview)
            # tree.configure(xscrollcommand=treescrollbarh.set, height=8)
            # treescrollbarh.grid(row=7, columnspan=4, sticky=tk.EW, rowspan=1)

            # treescrollbarv = ttk.Scrollbar(
            #     self, orient='vertical', command=tree.yview)
            # tree.configure(yscrollcommand=treescrollbarv.set)
            # treescrollbarv.grid(column=5, columnspan=5,
            #                     sticky=tk.NS, row=5, rowspan=4)

        def open_map():
            webbrowser.open("paca_geocode.html", new=2)

        def clear_boxes():
            x_entry.delete(0, END)
            y_entry.delete(0, END)
            # for item in tree.get_children():
            #     tree.delete(item)

        # create our buttons
        geocode_button = MyButton(
            self, text="GEOCODE", command=geo_coder, style="TButton"
        )
        geocode_button.grid(row=2, column=2, sticky=tk.EW)

        exit_button = MyButton(
            self,
            text="Home",
            style="TButton",
            command=lambda: master.switch_frame(HomePage),
        ).grid(row=4, column=0, sticky=tk.EW)

        openmap_button = MyButton(
            self, text="OPEN MAP", command=open_map, style="TButton"
        )
        openmap_button.grid(row=3, column=2, sticky=tk.EW)

        clear_button = MyButton(
            self, command=clear_boxes, text="CLEAR", style="TButton"
        )
        clear_button.grid(row=4, column=2, sticky=tk.EW)


class DataPage(tk.Canvas):
    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.configure(bg="Indigo")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
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

        #logic
        def pickadate():
            self.top = tk.Toplevel()
            self.top.geometry('278x154+3+3')
            MyLabel(self.top, text='Choose Date').pack(padx=10, pady=10)
            self.date = DateEntry(self.top, width=12, background='grey',
                                  foreground='white', borderwidth=2, year=2018)
            self.date.pack(padx=10, pady=10)
            self.date.bind("<<DateEntrySelected>>")
            MyButton(self.top, style='TButton', text='Exit',
                       command=self.top.destroy).pack(pady=3, padx=3, side='bottom')


        def select():
            tree.delete(*tree.get_children())
            db = DatabaseConn()
            db.query("SELECT * FROM notes_master ORDER BY ID")
            for row in db.cur:
                tree.insert("", tk.END, values=(
                    row[5], row[0], row[1], row[2], row[3], row[4]))
            db.commit()
            db.close()

        def submit():
            pass

        # figure out how to compound the wc logo into this header label widget, then change favicon
        MyLabel(
            self,
            style="Heading.TLabel",
            text="General Problems/Notes",
            background="cadet blue",
        ).grid(row=0, column=0, columnspan=3, sticky=tk.EW, pady=10)
        # set up data entry
        data_font = font.Font(
            family="IBM Plex Mono", size=9, weight="normal", slant="italic"
        )
        trs_valu = tk.StringVar(value="Town-Range-Section")
        pin_valu = tk.StringVar(value="Parcel Number")
        note_valu = tk.StringVar(value="Problem")
        fixed_valu = tk.StringVar(value="Fixed?")
        # buttons and widgets
        # TRS
        MyLabel(self, style="TLabel", text="T-R-S: ").grid(
            column=0, row=1, sticky=tk.EW, columnspan=1
        )
        MyEntry(self, style="TEntry", textvariable=trs_valu, font=data_font).grid(
            column=1, row=1, sticky=tk.EW, columnspan=3
        )
        # Parcel ID
        MyLabel(self, style="TLabel", text="Parcel ID: ").grid(
            column=0, row=2, sticky=tk.EW, columnspan=1
        )
        MyEntry(self, style="TEntry", textvariable=pin_valu, font=data_font).grid(
            column=1, row=2, sticky=tk.EW, columnspan=3
        )
        # Notes
        MyLabel(self, style="TLabel", text="Note: ").grid(
            column=0, row=3, sticky=tk.EW, columnspan=1
        )
        MyEntry(self, style="TEntry", textvariable=note_valu, font=data_font).grid(
            column=1, row=3, sticky=tk.EW, columnspan=3
        )
        # Action taken list
        fixed = ("Yes", "No", "On Hold", "Waiting for Direction")
        MyLabel(self, text="Problem Resolved?:", style="TLabel").grid(
            column=0, row=5, sticky=tk.EW, columnspan=1
        )
        fixed_combo = ttk.Combobox(self, textvariable=fixed_valu)
        fixed_combo["values"] = fixed
        fixed_combo["state"] = "readonly"
        fixed_combo.grid(column=1, row=5, sticky=tk.EW, columnspan=2)
        fixed_combo.bind("<<ComboboxSelected>>")

        MyLabel(self, text="Delete Record(ID)", style="TLabel").grid(
            column=0, row=6, sticky=tk.EW, columnspan=1
        )
        MyEntry(self, style="TEntry", font=data_font).grid(
            column=1, row=6, sticky=tk.EW, columnspan=2
        )

        MyButton(
            self,
            text="Home",
            style="TButton",
            command=lambda: master.switch_frame(HomePage),
        ).grid(column=0, columnspan=1, sticky=tk.EW, row=7)

        MyButton(self, text="Delete", style="TButton").grid(
            column=0, columnspan=1, sticky=tk.EW, row=8
        )

        MyButton(self, text="Add", style="TButton").grid(
            column=1, columnspan=1, sticky=tk.EW, row=8
        )

        MyButton(self, text="Update", style="TButton").grid(
            column=2, columnspan=1, sticky=tk.EW, row=8
        )

        MyButton(self, text="Select All", command=select, style="TButton").grid(
            row=7, column=1, columnspan=1, sticky=tk.EW
        )

        MyButton(self, text="Submit", command=submit, style="TButton").grid(
            row=7, column=2, columnspan=1, sticky=tk.EW
        )

        # create our treeview for the totreevirw func
        columns = ("ROWID", "T-R-S", "PIN", "NOTE", "FIXED?", "DATE")
        tree = ttk.Treeview(
            self, columns=columns, show="headings", style="mystyle.Treeview"
        )

        # for column in columns:
        #     tree.column(column, anchor=CENTER, width=100)

        # declare our treeview headers
        tree.heading("ROWID", text="ID")
        tree.column("ROWID", minwidth=0, width=3, anchor=CENTER)
        tree.heading("T-R-S", text="T-R-S")
        tree.column("T-R-S", minwidth=0, width=15, anchor=CENTER)
        tree.heading("PIN", text="PIN")
        tree.column("PIN", minwidth=0, width=12, anchor=CENTER)
        tree.heading("NOTE", text="NOTE")
        tree.column("NOTE", minwidth=0, width=40, anchor=CENTER)
        tree.heading("FIXED?", text="FIXED?")
        tree.column("FIXED?", minwidth=0, width=3, anchor=CENTER)
        tree.heading("DATE", text="DATE")
        tree.column("DATE", minwidth=0, width=15, anchor=CENTER)
        tree.grid(row=9, columnspan=3, sticky=tk.NSEW, ipadx=1, ipady=1)

        # add horz and vert scroll bars to treeview
        treescrollbarh = ttk.Scrollbar(self, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=treescrollbarh.set, height=8)
        treescrollbarh.grid(row=10, columnspan=3, sticky=tk.EW, rowspan=1)

        # treescrollbarv = ttk.Scrollbar(
        #     self, orient='vertical', command=tree.yview)
        # tree.configure(yscrollcommand=treescrollbarv.set)
        # treescrollbarv.grid(column=0, columnspan=6,
        #                     sticky=tk.NS, row=9, rowspan=2)
        #
        # # commit to and close DB
        # conn.commit()
        # conn.close()

        # shows how each frame resizes


if __name__ == "__main__":
    app = App()
    app.mainloop()
