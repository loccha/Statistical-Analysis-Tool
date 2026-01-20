import os

class AppController:
    
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.gui = None
        self.directory = os.getcwd()

        self.start_year = ''
        self.end_year = ''
        self.indicator = ''

        self.current_df = None


    def set_gui(self, gui):
        self.gui = gui


    def on_open_clicked(self):
        '''Open a file dialog to select a CSV file'''
        filename = self.gui.show_file_dialog(self.directory)

        if filename:
            self.directory = os.path.dirname(filename)
            self.gui.display_path_file(filename)
            
            #fetch the new indicators 
            self.data_handler.load_file(filename)

            min_year, max_year = self.min_max_years_boundarie()
            self.gui.display_years(min_year, max_year)   #test    
            self.gui.display_indicators(self.data_handler.get_indicators())


    def filter(self, df):
        #fetch selected countries
        selected_countries = self.gui.selected_countries
        
        #update dataframe
        f_df = df.copy()
        f_df = f_df[f_df['COUNTRY'].isin(selected_countries)]
        return f_df
    

    def on_enter_pressed(self):
        self.indicator = self.gui.indicators_cb.get()
        self.start_year = self.gui.start_year_spinbox.get()
        self.end_year = self.gui.end_year_spinbox.get()

        self.current_df = self.data_handler.get_delta_df(self.indicator, self.start_year, self.end_year)
        if self.gui.selected_countries:
            self.current_df = self.filter(self.current_df)
        
        self.gui.display_datas(self.current_df)

    
    def on_filter_clicked(self):
        if self.gui.selected_countries:
            self.current_df = self.filter(self.current_df) 
            self.gui.display_datas(self.current_df)


    def on_reloadAll_clicked(self):
        self.indicator = self.gui.indicators_cb.get()
        self.start_year = self.gui.start_year_spinbox.get()
        self.end_year = self.gui.end_year_spinbox.get()

        self.current_df = self.data_handler.get_delta_df(self.indicator, self.start_year, self.end_year)
        self.gui.display_datas(self.current_df)


    def min_max_years_boundarie(self):
        years_columns = self.data_handler.df.columns[2:]
        return years_columns[0], years_columns[-1]


    def on_year_change(self):
        self.start_year = str(self.gui.start_year_var.get())
        self.end_year = str(self.gui.end_year_var.get())

        self.current_df = self.data_handler.get_delta_df(self.indicator, self.start_year, self.end_year)

        if self.gui.selected_countries:
            self.current_df = self.filter(self.current_df)

        self.gui.display_datas(self.current_df)




