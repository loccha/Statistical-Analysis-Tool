import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as tb

from tooltip import ToolTip 

class GUI:
    """
    View layer of the application (MVC pattern).
    
    Responsible for:
    - Building and displaying the user interface
    - Handling user interactions (button clicks, selections, searches)
    - Displaying data and error messages to the user
    - Managing form inputs (file selection, indicator choice, year range)
    - Supporting country filtering and search functionality
    
    Args:
        controller (AppController): The controller instance to handle user interactions
    
    Attributes:
        root (tk.Tk): The main tkinter window
        controller (AppController): Reference to the controller
        treeview (ttk.Treeview): Data table displaying delta calculations
        indicators_cb (ttk.Combobox): Dropdown for indicator selection
        start_year_spinbox, end_year_spinbox (tk.Spinbox): Year range selectors
        selected_countries (list): Countries selected for filtering
        country_items (dict): Mapping of countries to treeview item IDs for search
    """
    def __init__(self, controller):
        self.root = tb.Window(themename='flatly')
        self.controller = controller

        self._build_ui()

    #builds the opening UI
    def _build_ui(self):
        self.root.title("Statistical Analysis Tool")
        self.root.maxsize(700, self.root.winfo_screenheight())

        self._setup_fonts()
        self._setup_tv_col_size()
        self._build_form()
        self._build_search_bar()
        self._build_selected_countries_display()  
        self._build_filter()
        self._build_treeview()

        self._setup_bindings()

        #dictionnary country -> items for the search bar
        self.country_items = {}
    

    def _setup_fonts(self):
        """Setup font styles used in the GUI."""
        self.font1=('Bahnschrift', 11, 'normal')
        self.font2=('Bahnschrift', 10, 'bold')
        self.font3=('Bahnschrift', 9, 'normal')


    def _setup_tv_col_size(self):
        """Configure treeview column widths and set expected numbers of columns in the treeview."""
        self.nb_of_numbers_col = 3
        self.country_col_width = 225
        self.numbers_col_width = 125


    def _build_form(self):
        """Build the form section with file input, indicator selector, and year range."""
        self.form_frame=tk.Frame(self.root)
        self.form_frame.pack(padx=10, pady=20, anchor='w')
        self.form_frame.grid_columnconfigure(1, weight=1)

        self._build_years_section()
        self._build_file_section()
        self._build_indicator_section()
                

    def _build_file_section(self):
        """Build file selection section with entry field and Open button."""
        self.file_label = tk.Label(self.form_frame, font=self.font1, text='File:')
        self.file_label.grid(row=0, column=0, sticky=tk.W, pady=2)

        self.file_entry = tk.Entry(self.form_frame, width=70)
        self.file_entry.grid(row=0, column=1, padx=5, sticky="ew")
        self.file_entry.focus()

        self.open_button = ttk.Button(self.form_frame, text="Open", command=self.controller.on_open_clicked)
        self.open_button.grid(row=0, column=2, padx=20)


    def _build_indicator_section(self):
        """Build the indicator dropdown selector in the form."""
        self.current_label = tk.Label(self.form_frame, font=self.font1, text='Indicator:')
        self.current_label.grid(row=1, column=0, sticky=tk.W, pady=2)

        self.indicators_cb = ttk.Combobox(
               self.form_frame,
                values=[],    
                state="readonly",
            )
        
        self.indicators_cb.grid(row=1, column=1, padx=5, pady=3, sticky="ew")


    def _build_years_section(self):
        """Build year range selector (From/To spinboxes)."""
        self.year_frame = tk.Frame(self.form_frame)
        self.year_frame.grid(row=2, column=1, columnspan=2, sticky="ew", pady=2)

        # 'From' year selector
        self.start_year_label = tk.Label(self.form_frame, font=self.font1, text='From:')
        self.start_year_label.grid(row=2, column=0, sticky=tk.W)
        
        self.start_year_spinbox = tk.Spinbox(
            self.year_frame,
            width=10,
        )
        self.start_year_spinbox.grid(row=0, column=1, padx=5)

        # 'To' year selector
        self.end_year_label = tk.Label(self.year_frame, font=self.font1, text='To:')
        self.end_year_label.grid(row=0, column=2, padx=10)

        self.end_year_spinbox = tk.Spinbox(
            self.year_frame,
            width=10,
        )
        self.end_year_spinbox.grid(row=0, column=3)


    def _build_search_bar(self):
        """Build search bar for filtering countries by name."""
        self.search_var = tk.StringVar()
        self.selected_countries = []

        self.search_bar_frame = tk.Frame(self.root)
        self.search_bar_frame.pack(padx=10, pady=5, anchor='nw')        

        self.search_label = tk.Label(self.search_bar_frame, font=self.font2, text='Search:')
        self.search_label.pack(side='left')
        self.search_entry = tk.Entry(self.search_bar_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(padx=10)

        # Trigger search on every text change
        self.search_var.trace_add("write", self.on_search_change)


    def _build_selected_countries_display(self):
        """Build label to display selected countries for filtering."""
        self.selected_countries_frame = tk.Frame(self.root)
        self.selected_countries_frame.pack(padx=10, anchor='nw')

        self.selected_countries_label_var = tk.StringVar(value="Selected countries: ")
        self.selected_countries_label = tk.Label(
            self.selected_countries_frame,
            textvariable=self.selected_countries_label_var, 
            wraplength=self.country_col_width + self.nb_of_numbers_col*self.numbers_col_width, 
            justify='left',
            font=("Segoe UI", 8)
            )
        self.selected_countries_label.pack()


    def _build_filter(self):
        """Build Filter and Clear buttons for data filtering."""
        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack(padx=20, pady=10, anchor='nw')

        filter_button = ttk.Button(self.filter_frame, text="Filter", command=self.controller.on_filter_clicked)
        filter_button.pack(side='left')

        self.clear_button = ttk.Button(self.filter_frame, text="Clear", command=self.controller.on_clear_clicked)
        self.clear_button.pack(padx=10)


    def _build_treeview(self):
        """Build the data table with columns, scrollbar, and sortable headers."""
        tf_pady = 10
        tf_width = (2*tf_pady 
                    + self.country_col_width 
                    + self.nb_of_numbers_col*self.numbers_col_width
                    )


        self.treeview_frame = tk.Frame(self.root, width=tf_width, height=400)
        self.treeview_frame.pack(padx=20, pady=tf_pady, fill="y", expand=True, anchor='nw')

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
        self.treeview.pack(fill="y", expand=True, side=tk.LEFT)

    
        for i, col in enumerate(columns):
            self.treeview.heading(
                col, 
                text=col, 
                command=lambda 
                i=i:self.controller.on_heading_clicked(i)
                )
            

        # Country column: wider, left-aligned
        self.treeview.heading(columns[0], text=columns[0])
        self.treeview.column(columns[0], width=self.country_col_width, stretch=False)

        # Numeric columns: narrower, right-aligned
        for col in columns[1:]:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor='e', width=self.numbers_col_width, stretch=False)

        self.scroll_bar.config(command=self.treeview.yview)


    def _setup_bindings(self):
        """Bind keyboard and mouse events to handler functions."""
        self.root.bind('<Return>', lambda _: self.controller.on_inputs_changed())
        self.treeview.bind("<Double-1>", lambda event: self.on_double_click(event))
        self.indicators_cb.bind("<<ComboboxSelected>>", self.controller.on_indicator_selected)

    
    def on_double_click(self, event):
        """Handle double-click on treeview row to add country to 'Selected countries'."""
        item_id = self.treeview.identify_row(event.y)
    
        if item_id:
            # Add country to 'selected countries' if not already selected
            country = self.treeview.item(item_id)['values'][0]
            if(country not in self.selected_countries):
                self.selected_countries.append(country)
                self.display_selected_countries()


    def on_search_change(self, *args):
        """Filter treeview rows based on search query matching country names."""
        query = self.search_var.get().lower()

        # Show matching countries, hide non-matching ones
        for country, item_id in self.country_items.items():
            if query.lower() in country.lower():
                self.treeview.reattach(item_id, '', 'end')
            else:
                self.treeview.detach(item_id)


    def show_file_dialog(self, initial_dir):
        """Open a file dialog to select a CSV file."""
        filename = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Select a CSV file",
            filetypes=(("CSV files", "*.csv*"), ("all files","*.*"))
        )
        return filename 


    def display_path_file(self, path: str):
        """Display the selected file path in entry field and add tooltip."""
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, path)
        
        self.file_ttp = ToolTip(self.file_entry, path) 


    def display_indicators(self, indicators: list[str]):
        """Populate indicator dropdown with available indicators and set default."""
        self.indicators_cb['values'] = indicators

        # Set first indicator as default
        self.indicators_cb.current(0)
        self.indicators_ttp = ToolTip(self.indicators_cb, self.indicators_cb.get())


    def display_years(self, min_year: int, max_year: int):
        """
        Configure year spinboxes with available year range and default values.
        If input years are out of bounds using the arrows, they will be clamped to min and max respectively.
        """
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
        

    def display_selected_countries(self):
        """Update the selected countries label with newly added country."""
        current_label = self.selected_countries_label_var.get()
        new_country = self.selected_countries[-1]

        if len(self.selected_countries)>1:
            self.selected_countries_label_var.set(f"{current_label}, '{new_country}'")
        else:
            self.selected_countries_label_var.set(f"{current_label} '{new_country}'")
    

    def display_datas(self, country_col: str, df):
        """Populate treeview with data from DataFrame, format numbers, apply styling."""
        self.treeview.delete(*self.treeview.get_children())
        self.country_items.clear()

        # Configure row colors for alternating rows and negative values
        self.treeview.tag_configure("negative", foreground="#cc2c2c")
        self.treeview.tag_configure('pair', background="#e1dede")
        self.treeview.tag_configure('impair', background='white')

        for i, (_,row) in enumerate(df.iterrows()):
            values = list(row)
            tags = ["pair"] if i%2==0 else ["impair"]

            # Colors row's font in red if delta is negative
            if(values[-1]<0):
                tags.append('negative')
            
            # Format numbers with comma separators and 3 decimal places
            values[1:] = [f"{n:,.3f}" for n in values[1:]]
            item_id = self.treeview.insert('', 'end', values=values, tags=tags)

            # Store mapping for search functionality
            self.country_items[row[country_col].lower()] = item_id
        

    def show_error(self, error_msg: str):
        """Display error message in a messagebox."""
        messagebox.showinfo(self.root.title, error_msg)


    def get_selected_countries(self) -> list[str]:
        """Return list of countries selected for filtering."""     
        return self.selected_countries
    

    def set_indicator_ttp_text(self, indicator: str):
        """Update tooltip text for the indicator dropdown."""
        self.indicators_ttp.text = indicator


    def clear_selection(self, event=None):
        """Clear all selected countries and update display."""
        self.selected_countries = []
        self.selected_countries_label_var.set("Selected countries: ")


    def clear_searchbar(self):
        """Clear search input field."""
        self.search_var.set("")        


    def run(self):
        """Start the GUI event loop."""
        self.root.mainloop()