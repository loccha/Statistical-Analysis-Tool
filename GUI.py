import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class GUI:

    def __init__(self, controller):
        self.root = tk.Tk()
        self.controller = controller

        self.root.bind('<Return>', lambda event: self.controller.on_enter_pressed())

        self.build_ui()

    #builds the opening UI
    def build_ui(self):
        self.root.title("Statistical Analysis Tool")
        self.font1=('Bahnschrift', 11, 'normal')

        #----Main form frame----
        self.form_frame=tk.Frame(self.root)
        self.form_frame.pack(padx=10, pady=10, anchor='w')

        self.form_frame.grid_columnconfigure(1, weight=1)

        #----- Row 0: File-------
        self.file_label = tk.Label(self.form_frame, font=self.font1, text='File:')
        self.file_label.grid(row=0, column=0, sticky=tk.W, pady=2)

        self.file_entry = tk.Entry(self.form_frame, width=50)
        self.file_entry.grid(row=0, column=1, sticky="ew")
        self.file_entry.focus()

        self.open_button = tk.Button(self.form_frame, text="Open", command=self.controller.on_open_clicked)
        self.open_button.grid(row=0, column=2, padx=20)

        #-----Row 1: Indicator------
        self.current_label = tk.Label(self.form_frame, font=self.font1, text='Indicator:')
        self.current_label.grid(row=1, column=0, sticky=tk.W, pady=2)

        self.indicators_cb = ttk.Combobox(
               self.form_frame,
                values=[],    
                state="readonly"   
            )
        
        self.indicators_cb.grid(row=1, column=1, sticky="ew")

        #-----Row 2: years entries-------
        self.year_frame = tk.Frame(self.form_frame)
        self.year_frame.grid(row=2, column=1, columnspan=2, sticky="ew", pady=2)

        #start year
        self.start_year_label = tk.Label(self.form_frame, font=self.font1, text='From:')
        self.start_year_label.grid(row=2, column=0, sticky=tk.W)

        self.start_year_spinbox = tk.Spinbox(
            self.year_frame,
            #from_=1980,  #TODO: min year in the datas
            #to=2030,     #TODO: max year in the datas
            width=10,
        )

        self.start_year_spinbox.grid(row=0, column=1)

        #end year
        self.end_year_label = tk.Label(self.year_frame, font=self.font1, text='To:')
        self.end_year_label.grid(row=0, column=2, padx=10)

        self.end_year_spinbox = tk.Spinbox(
            self.year_frame,
            #from_=1980,  #TODO: min year in the datas
            #to=2030,     #TODO: max year in the datas
            width=10,
        )
        self.end_year_spinbox.grid(row=0, column=3)


        #----------Treeview-------------
        self.treeview_frame = tk.Frame(self.root, width=470, height=400)
        #self.treeview_frame.pack_propagate(False)
        self.treeview_frame.pack(padx=20, pady=20, anchor='nw')

        self.scroll_bar = tk.Scrollbar(self.treeview_frame)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        columns=['COUNTRY', 'START', 'END', 'CHANGE']
        self.treeview = ttk.Treeview(
            self.treeview_frame, 
            yscrollcommand=self.scroll_bar.set,
            columns=columns,
            show='headings'
            )
        
        for col in columns:
            self.treeview.heading(col, text=col)

        #COUNTRY column
        self.treeview.heading(columns[0], text=columns[0])
        self.treeview.column(columns[0], width=225, stretch=False)

        #numbers columns
        for col in columns[1:]:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor='e', width=75, stretch=False)

        self.treeview.pack()

        self.scroll_bar.config(command=self.treeview.yview)


    def show_file_dialog(self, initial_dir):
        '''Open a file dialog to select a CSV file'''
        filename = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Select a CSV file",
            filetypes=(("CSV files", "*.csv*"), ("all files","*.*"))
        )
        return filename
    
    def display_path_file(self, path):
        '''Display the selected file path in the entry'''
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, path)

    def display_indicators(self, indicators):
        self.indicators_cb['values'] = indicators

    def display_datas(self, df):
        self.treeview.delete(*self.treeview.get_children())

        for idx, row in df.iterrows():
            tags = []
            tags.append('pair') if idx % 2 == 0 else tags.append('impair')
            if(list(row)[3]<0):
                tags.append('negative')
            self.treeview.insert('', 'end', values=list(row), tags=tags)
        
        self.treeview.tag_configure("negative", foreground="#cc2c2c")
        self.treeview.tag_configure('pair', background="#c7c7c7")
        self.treeview.tag_configure('impair', background='white')

    # def enable(self):
    #     '''Change the entry state from readonly to normal'''
    #     self.file_entry.config(state="normal") 
        
    def reset(self):
        ''' Delete everything in self.stats(Treeview)
        '''
        for i in self.treeview.get_children():
            self.treeview.delete(i)
    
    #TODO: limit the years to min and max years
    def min_max_years_boundaries(self):
        return None

    def error(self):
        '''Error message box if exception
        '''
        messagebox.showinfo("Statistical Analysis Tool", "Please enter valid information")        

    def run(self):
        self.root.mainloop()



