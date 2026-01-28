import os
import re

from data_handler import DataHandler, InvalidFileFormatError
    

class AppController:
    
    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler
        self.gui = None
        self.directory = os.getcwd()

        self.current_df = None
        self.min_year = 0
        self.max_year = 0


    def set_gui(self, gui):
        self.gui = gui
    

    def on_open_clicked(self):
        '''Open a file dialog to select a CSV file'''
        filename = self.gui.show_file_dialog(self.directory)

        #load default values if filename is selected
        if filename:
            self.directory = os.path.dirname(filename)
            self.gui.display_path_file(filename)
            
            #gets years and indicator from loaded csv
            try:
                self.data_handler.load_file(filename) 
            except InvalidFileFormatError as e:
                self.current_df = None
                self.gui.show_error(str(e))
                return

            self.min_year, self.max_year = self._min_max_years_boundary()
            
            self.gui.display_years(self.min_year, self.max_year)       
            self.gui.display_indicators(self.data_handler.get_indicators())
            
            self.current_df = self.data_handler.get_delta_df(
                self.gui.indicators_cb.get(), 
                str(self.min_year), 
                str(self.max_year)
                )
            self.gui.display_datas(self.data_handler.get_country_col(), self.current_df)


    def on_indicator_selected(self, event=None):
         #changes tooltip text for the indicator to the current one
         self.gui.set_indicator_ttp_text(self.gui.indicators_cb.get())

         self.gui.clear_selection()
         self.on_inputs_changed()


    def on_inputs_changed(self): 
        if self.current_df is None:
                return   

        try:
            indicator, start_year, end_year = self._get_user_values()
            if not (int(start_year) < int(end_year)):
                raise ValueError(f"Invalid year range: the start year must be less than the end year.")
            if not self._validate_years_input_user(start_year, end_year):
                raise ValueError(f"Year must be between {self.min_year} and {self.max_year}. ")
        except ValueError as e:
            self.gui.show_error(str(e))
            return
        
        self.current_df = self.data_handler.get_delta_df(indicator, start_year, end_year)

        #if user is filtering by countries
        if self.gui.get_selected_countries():
            self.current_df = self._filter(self.current_df)
        
        self.gui.display_datas(self.data_handler.get_country_col(), self.current_df)


    def on_filter_clicked(self):
        if self.current_df is None:
            return
        
        self.gui.clear_searchbar()

        if self.gui.get_selected_countries():
            self.current_df = self._filter(self.current_df) 
            self.gui.display_datas(self.data_handler.get_country_col(), self.current_df)


    def on_clear_clicked(self):
        if self.current_df is None:
            return
        
        self.current_df = self.data_handler.get_delta_df(
            self.gui.indicators_cb.get(), 
            str(self.min_year), 
            str(self.max_year)
            )
        
        self.gui.clear_searchbar()
        self.gui.clear_selection()
        self.gui.display_datas(self.data_handler.get_country_col(), self.current_df)
        self.gui.display_years(self.min_year, self.max_year)


    def on_heading_clicked(self, icol: int):
        if self.current_df is None:
            return
        
        self.current_df = self.data_handler.toggle_sort(icol, self.current_df)
        self.gui.display_datas(self.data_handler.get_country_col(), self.current_df)


    def _get_user_values(self):
        indicator = self.gui.indicators_cb.get()
        start_year = self.gui.start_year_spinbox.get()
        end_year = self.gui.end_year_spinbox.get()

        return indicator, start_year, end_year
    

    def _min_max_years_boundary(self):
        years_columns = self.data_handler.get_years_columns()
        
        return int(years_columns[0]), int(years_columns[-1])
    

    def _validate_years_input_user(self, start_year, end_year) -> bool:
            pattern = "^\d{4}$"
            if (re.match(pattern, start_year)) and (re.match(pattern, end_year)):
                start_year, end_year= int(start_year), int(end_year)

                return ((self.min_year<=start_year<=self.max_year) and
                        (self.min_year<=end_year<=self.max_year))
                        
            else:
                return False


    def _filter(self, df):
        selected_countries = self.gui.get_selected_countries()
        country_col = self.data_handler.get_country_col()
        
        return df[df[country_col].isin(selected_countries)]
        



