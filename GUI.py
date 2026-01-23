import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class CreateToolTip(object):
    def __init__(self, widget, text, delay=500):
        self.delay = delay             #ms
        self.widget = widget
        self.text = text
        
        self.id = None
        self.tw = None

        self.widget.bind("<Enter>", self._enter)
        self.widget.bind("<Leave>", self._leave)
        self.widget.bind("<ButtonPress>", self._leave)
    

    def _enter(self, event=None):
        self._schedule()
    

    def _leave(self, event=None):
        self._unschedule()
        self._hidetip()


    def _schedule(self):
        self._unschedule()
        self.id=self.widget.after(self.delay, self._show)


    def _unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)


    def _show(self, event=None):
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(
            self.tw, text=self.text, 
            justify='left', 
            background='#ffffff', 
            relief='solid', 
            borderwidth=1, 
            #wraplength = self.wraplength
            )
        label.pack(ipadx=1)
    

    def _hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class GUI:
    def __init__(self, controller):
        self.root = tk.Tk()
        self.controller = controller

        self.build_ui()

    #builds the opening UI
    def build_ui(self):
        self.root.title("Statistical Analysis Tool")
        self._setup_fonts()
        self._build_form()
        self._build_search_bar()
        self._build_selected_countries_display()  
        self._build_filter()
        self._build_treeview()

        self._setup_bindings()

        #dictionnary country -> items for the search bar
        self.country_items = {}
    

    def _setup_fonts(self):
        self.font1=('Bahnschrift', 11, 'normal')
        self.font2=('Bahnschrift', 10, 'bold')
        self.font3=('Bahnschrift', 9, 'normal')


    def _build_form(self):
        self.form_frame=tk.Frame(self.root)
        self.form_frame.pack(padx=10, pady=20, anchor='w')
        self.form_frame.grid_columnconfigure(1, weight=1)

        self._build_years_section()
        self._build_file_section()
        self._build_indicator_section()
                

    def _build_file_section(self):
        self.file_label = tk.Label(self.form_frame, font=self.font1, text='File:')
        self.file_label.grid(row=0, column=0, sticky=tk.W, pady=2)

        self.file_entry = tk.Entry(self.form_frame, width=60)
        self.file_entry.grid(row=0, column=1, padx=5, sticky="ew")
        self.file_entry.focus()

        self.open_button = tk.Button(self.form_frame, text="Open", command=self.controller.on_open_clicked)
        self.open_button.grid(row=0, column=2, padx=20)


    def _build_indicator_section(self):
        self.current_label = tk.Label(self.form_frame, font=self.font1, text='Indicator:')
        self.current_label.grid(row=1, column=0, sticky=tk.W, pady=2)

        self.indicators_cb = ttk.Combobox(
               self.form_frame,
                values=[],    
                state="readonly",
            )
        
        self.indicators_cb.grid(row=1, column=1, padx=5, sticky="ew")


    def _build_years_section(self):
        self.year_frame = tk.Frame(self.form_frame)
        self.year_frame.grid(row=2, column=1, columnspan=2, sticky="ew", pady=2)

        #'From' section
        self.start_year_label = tk.Label(self.form_frame, font=self.font1, text='From:')
        self.start_year_label.grid(row=2, column=0, sticky=tk.W)
        
        self.start_year_spinbox = tk.Spinbox(
            self.year_frame,
            width=10,
        )
        self.start_year_spinbox.grid(row=0, column=1, padx=5)

        #'To' section
        self.end_year_label = tk.Label(self.year_frame, font=self.font1, text='To:')
        self.end_year_label.grid(row=0, column=2, padx=10)

        self.end_year_spinbox = tk.Spinbox(
            self.year_frame,
            width=10,
        )
        self.end_year_spinbox.grid(row=0, column=3)


    def _build_search_bar(self):
        self.search_var = tk.StringVar()
        self.selected_countries = []

        self.search_bar_frame = tk.Frame(self.root)
        self.search_bar_frame.pack(padx=10, pady=5, anchor='nw')        

        self.search_label = tk.Label(self.search_bar_frame, font=self.font2, text='Search:')
        self.search_label.pack(side='left')
        self.search_entry = tk.Entry(self.search_bar_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(padx=10, side='right')

        self.search_var.trace_add("write", self.on_search_change)


    def _build_selected_countries_display(self):
        self.selected_countries_frame = tk.Frame(self.root)
        self.selected_countries_frame.pack(padx=10, anchor='nw')

        #Clear selections button (X)
        self.clear_selection_button = tk.Label(self.selected_countries_frame, text='(✕)')

        self.selected_countries_label_var = tk.StringVar(value="Selected countries: ")
        #TODO: wraplength : equal to treeview with variables
        self.selected_countries_label = tk.Label(
            self.selected_countries_frame,
            textvariable=self.selected_countries_label_var, 
            wraplength=450, 
            justify='left',
            font=("Segoe UI", 8)
            )
        self.selected_countries_label.pack(side='left')


    def _build_filter(self):
        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack(padx=20, pady=10, anchor='nw')

        filter_button = tk.Button(self.filter_frame, text="Filter", command=self.controller.on_filter_clicked)
        filter_button.pack(anchor='w', side='left')

        self.clear_button = tk.Button(self.filter_frame, text="(Re)Load All", command=self.controller.on_reloadAll_clicked)
        self.clear_button.pack(padx=10, anchor='e', side='right')


    def _build_treeview(self):
        #TODO: width = pady treeview + all columns
        self.treeview_frame = tk.Frame(self.root, width=470, height=400)
        self.treeview_frame.pack(padx=20, pady=10, anchor='nw')

        self.scroll_bar = tk.Scrollbar(self.treeview_frame)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        columns=['Country name', 'From', 'To', '% Change']
        self.treeview = ttk.Treeview(
            self.treeview_frame, 
            yscrollcommand=self.scroll_bar.set,
            columns=columns,
            show='headings',
            selectmode="extended"
            )
        
        for col in columns:
            self.treeview.heading(col, text=col)

        #'Country name' column
        self.treeview.heading(columns[0], text=columns[0])
        self.treeview.column(columns[0], width=225, stretch=False)

        #Other columns
        for col in columns[1:]:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor='e', width=125, stretch=False)

        self.treeview.pack()
        self.scroll_bar.config(command=self.treeview.yview)


    def _setup_bindings(self):
        self.root.bind('<Return>', lambda event: self.controller.on_inputs_changed())
        self.treeview.bind("<Double-1>", lambda event: self.on_double_click(event))
        self.clear_selection_button.bind("<Button-1>", self.on_clear_selection_clicked)
        self.indicators_cb.bind("<<ComboboxSelected>>", self.on_selected_indicator_hovered)

    
    def on_selected_indicator_hovered(self, event=None):
         self.indicators_ttp.text = self.indicators_cb.get()


    def get_selected_countries(self):     
        return self.selected_countries
    

    def selected_countries_display_update(self):
        current_label = self.selected_countries_label_var.get()
        new_country = self.selected_countries[-1]

        if len(self.selected_countries)>1:
            self.selected_countries_label_var.set(f"{current_label}, '{new_country}'")
        else:
            self.selected_countries_label_var.set(f"{current_label} '{new_country}'")


    #'clear selection' is this button in the app --> (x)
    def on_clear_selection_clicked(self, event=None):
        self.selected_countries = []
        self.selected_countries_label_var.set("Selected countries: ")
        self.clear_selection_button.pack_forget()


    def pack_clear_selection_button(self):
        self.clear_selection_button.pack(side='left', before=self.selected_countries_label, anchor="nw")


    def on_double_click(self, event):
        
        item_id = self.treeview.identify_row(event.y)
    
        if item_id:
            #add country to 'selected countries' if not already selected
            country = self.treeview.item(item_id)['values'][0]
            if(country not in self.selected_countries):
                self.selected_countries.append(country)
                self.selected_countries_display_update()

            if len(self.selected_countries)==1 :
                self.pack_clear_selection_button()


    def show_file_dialog(self, initial_dir):
        '''Open a file dialog to select a CSV file'''
        filename = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Select a CSV file",
            filetypes=(("CSV files", "*.csv*"), ("all files","*.*"))
        )
        return filename
    

    def on_search_change(self, *args):

        query = self.search_var.get().lower()

        for country, item_id in self.country_items.items():
            if query.lower() in country.lower():
                self.treeview.reattach(item_id, '', 'end')
            else:
                self.treeview.detach(item_id)   #TODO: bug here (Item x not found)
    

    def display_path_file(self, path):
        '''Display the selected file path in the entry'''
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, path)
        
        self.file_ttp = CreateToolTip(self.file_entry, path)



    def display_indicators(self, indicators):
        self.indicators_cb['values'] = indicators

        #default first value
        self.indicators_cb.current(0)
        self.indicators_ttp = CreateToolTip(self.indicators_cb, self.indicators_cb.get())


    def display_years(self, min_year, max_year):
        self.start_year_var = tk.IntVar(value=min_year)
        self.start_year_spinbox.config(
            from_=min_year, 
            to=max_year, 
            textvariable=self.start_year_var, 
            command=self.controller.on_inputs_changed
            )
        
        self.end_year_var = tk.IntVar(value=max_year)
        self.end_year_spinbox.config(
            from_=min_year, 
            to=max_year, 
            textvariable=self.end_year_var, 
            command=self.controller.on_inputs_changed
            )


    def display_datas(self, df):
        self.treeview.delete(*self.treeview.get_children())

        #----tags color configuration----
        self.treeview.tag_configure("negative", foreground="#cc2c2c")
        self.treeview.tag_configure('pair', background="#e1dede")
        self.treeview.tag_configure('impair', background='white')

        for idx, row in df.iterrows():
            values = list(row)
            tags = []
            tags.append('pair') if idx % 2 == 0 else tags.append('impair')

            #row must be red if delta's value is negative
            if(values[-1]<0):
                tags.append('negative')
            
            #Format strings to display
            values[1:] = [f"{n:,.3f}" for n in values[1:]]

            item_id = self.treeview.insert('', 'end', values=values, tags=tags)

            #for the search bar
            self.country_items[row['COUNTRY'].lower()] = item_id


    def error(self):
        '''Error message box if exception
        '''
        messagebox.showinfo("Statistical Analysis Tool", "Please enter valid information")        


    def run(self):
        self.root.mainloop()



