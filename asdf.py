import tkinter as tk
from tkinter import StringVar, ttk
from tkinter.messagebox import showerror, showinfo, askretrycancel



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # set some params for main 'App' window
        self.title('ASDF')
        self.geometry('350x350+15+25')
        self.resizable(True,True)
        self.iconbitmap('./assets/favicon_sa.ico')
        self.configure(bg='#FFEBF2')
        # set App window grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        #add label frame
        self.mainlabelframe = ttk.LabelFrame(self)   
        self.mainlabelframe.grid(row=0, columnspan=3, sticky='NSEW', padx=2, pady=2, ipadx=4, ipady=4)
        self.heading = ttk.Label(self.mainlabelframe, foreground='black',style='Heading.TLabel', text='Fishing Spots')
        self.heading.grid(column=1, row=0, rowspan=1, pady=4, padx=4, sticky=tk.NS)

        # data entry label and entry box creation
        # Species caught
        def species_selected(event):
            msg = f'You selected {self.specieslabel_text.get()}!'
            showinfo(title='Result', message=msg)

        self.species = ('Brown Trout', 'Rainbow Trout', 'Brook Trout', 'Steelhead', 'Lake Run Brown Trout', 'Carp', 'Smallmouth Bass',
                        'Largemouth Bass', 'Bluegill', 'Pumpkinseed', 'Perch', 'Walleye', 'Northern Pike', 'Musky', 'Bullhead')
        self.specieslabel_text = tk.StringVar()
        self.specieslabel = ttk.Label(self, text='Select Species:', foreground='black', background='#FFEBF2', style='Data.TLabel')
        self.specieslabel.grid(column=0, row=1, sticky=tk.W,padx=5, pady=5, ipady=3, ipadx=3)
        self.specieslabel_combo = ttk.Combobox(self, textvariable=self.specieslabel_text)
        self.specieslabel_combo['values'] = self.species
        self.specieslabel_combo['state'] = 'readonly'
        self.specieslabel_combo.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)
        self.specieslabel_combo.bind('<<ComboboxSelected>>', species_selected)

        # stream name
        self.streamlabel_text = tk.StringVar()
        self.streamlabel = ttk.Label(self, text='Enter Stream Name:', foreground='black', background='#FFEBF2',style='Data.TLabel')
        self.streamlabel.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5, ipady=3, ipadx=3)
        self.streamlabel_entry = ttk.Entry(self, takefocus=0, cursor='hand1', textvariable=self.streamlabel_text)
        self.streamlabel_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        # County name
        def county_selected(event):
            msg = f'You selected {self.countylabel_text.get()}!'
            showinfo(title='Result', message=msg)
        self.countylabel_text = tk.StringVar()
        self.county = ('Adams',
                    'Ashland',
                    'Barron',
                    'Bayfield',
                    'Brown',
                    'Buffalo',
                    'Burnett',
                    'Calumet',
                    'Chippewa',
                    'Clark',
                    'Columbia',
                    'Crawford',
                    'Dane',
                    'Dodge',
                    'Door',
                    'Douglas',
                    'Dunn',
                    'Eau Claire',
                    'Florence',
                    'Fond du Lac',
                    'Forest',
                    'Grant',
                    'Green',
                    'Green Lake',
                    'Iowa',
                    'Iron',
                    'Jackson',
                    'Jefferson',
                    'Juneau',
                    'Kenosha',
                    'Kewaunee',
                    'La Crosse',
                    'Lafayette',
                    'Langlade',
                    'Lincoln',
                    'Manitowoc',
                    'Marathon',
                    'Marinette',
                    'Marquette',
                    'Menominee',
                    'Milwaukee')
        self.countylabel = ttk.Label(self, text='Enter County Name:', foreground='black', background='#FFEBF2', style='Data.TLabel')
        self.countylabel.grid(column=0, row=3, sticky=tk.W,padx=5, pady=5, ipady=3, ipadx=3)
        self.countylabel_combo = ttk.Combobox(
            self, textvariable=self.countylabel_text)
        self.countylabel_combo['values'] = self.county
        self.countylabel_combo['state'] = 'readonly'
        self.countylabel_combo.grid(
            column=1, row=3, sticky=tk.E, padx=5, pady=5)
        self.countylabel_combo.bind('<<ComboboxSelected>>', county_selected)

        
        # style library
        self.style = ttk.Style(self)
        self.style.theme_use('winnative')
        self.style.configure('TButton', font=('Roboto Mono', 9))
        self.style.configure('TLabel', font=('Fira Mono', 9))
        self.style.configure('Data.TLabel', font=('Fira Code', 10))
        self.style.configure('Heading.TLabel', font=('Palatino Linotype', 12))
        self.style.configure('AGO_Button.TButton', font=('Overpass Mono', 9))


if __name__ == "__main__":
    app = App()
    app.mainloop()
