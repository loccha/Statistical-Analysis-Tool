import os

class AppController:
    
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.gui = None
        self.directory = os.getcwd()

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


    def get_user_values(self):
        indicator = self.gui.indicators_cb.get()
        start_year = self.gui.start_year_spinbox.get()
        end_year = self.gui.end_year_spinbox.get()

        return indicator, start_year, end_year


    def filter(self, df):
        #fetch selected countries
        selected_countries = self.gui.get_selected_countries()
        
        #update dataframe
        f_df = df.copy()
        f_df = f_df[f_df['COUNTRY'].isin(selected_countries)]
        return f_df
    

    def on_inputs_changed(self):
        indicator, start_year, end_year = self.get_user_values()
        self.current_df = self.data_handler.get_delta_df(indicator, start_year, end_year)

        #if the user is filtering by countries
        if self.gui.get_selected_countries():
            self.current_df = self.filter(self.current_df)
        
        self.gui.display_datas(self.current_df)


    def on_reloadAll_clicked(self):
        indicator, start_year, end_year = self.get_user_values()
        self.current_df = self.data_handler.get_delta_df(indicator, start_year, end_year)

        self.gui.display_datas(self.current_df)
    

    def on_filter_clicked(self):
        if self.gui.get_selected_countries():
            self.current_df = self.filter(self.current_df) 
            self.gui.display_datas(self.current_df)


    def min_max_years_boundarie(self):
        years_columns = self.data_handler.get_years_columns()
        return years_columns[0], years_columns[-1]



