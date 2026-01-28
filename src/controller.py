import os
import re

from data_handler import DataHandler, InvalidFileFormatError

class AppController:
    """
    Controller layer of the application (MVC pattern).

    Responsible for:
    - Handling user interactions from the GUI
    - Coordinating between the GUI and the DataHandler
    - Updating the GUI based on data changes

    Args:
        data_handler (DataHandler): Instance of the DataHandler class
    
    Attributes:
        data_handler (DataHandler): Instance of the DataHandler class
        gui (GUI): Reference to the GUI component (set later)
        directory (str): Current working directory for file dialogs
        current_df (pd.DataFrame): Currently displayed DataFrame in GUI
        min_year (int): Minimum year available in the data
        max_year (int): Maximum year available in the data
    """
    
    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler
        self.gui = None
        self.directory = os.getcwd()

        self.current_df = None
        self.min_year = 0
        self.max_year = 0


    def set_gui(self, gui):
        """Store reference to the GUI component for later interactions."""
        self.gui = gui
    

    def on_open_clicked(self):
        """
        Handles the "Open File" button click event.
        Opens a file dialog, loads the selected CSV file, and updates the GUI
        with the loaded data.

        Throw InvalidFileFormatError if the file format is incorrect.
        """
        filename = self.gui.show_file_dialog(self.directory)

        if filename:
            self.directory = os.path.dirname(filename)
            self.gui.display_path_file(filename)
            
            try:
                self.data_handler.load_file(filename) 
            except InvalidFileFormatError as e:
                self.current_df = None
                self.gui.show_error(str(e))
                return

            self.min_year, self.max_year = self._min_max_years_boundary()
            
            self.gui.display_years(self.min_year, self.max_year)       
            self.gui.display_indicators(self.data_handler.get_indicators())
            
            # Display delta data for full year range with default indicator
            self.current_df = self.data_handler.get_delta_df(
                self.gui.indicators_cb.get(), 
                str(self.min_year), 
                str(self.max_year)
                )
            self.gui.display_datas(self.data_handler.get_country_col(), self.current_df)


    def on_indicator_selected(self, event=None):
         """
         Handles the event when an indicator is selected from the dropdown.
         Updates the tooltip text and refreshes the displayed data based on the new selection.
         """
         self.gui.set_indicator_ttp_text(self.gui.indicators_cb.get())

         self.gui.clear_selection()
         self.on_inputs_changed()


    def on_inputs_changed(self):
        """
        Handles changes in user inputs (indicator, start year, end year).
        Updates the displayed data accordingly.
        """
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
        
        # Recalculate delta data based on new indicator and year inputs
        self.current_df = self.data_handler.get_delta_df(indicator, start_year, end_year)

        # Apply country filter if user has selected specific countries
        if self.gui.get_selected_countries():
            self.current_df = self._filter(self.current_df)
        
        self.gui.display_datas(self.data_handler.get_country_col(), self.current_df)


    def on_filter_clicked(self):
        """
        Handles the "Filter" button click event.
        Filters the current DataFrame based on selected countries
        and updates the GUI display.
        """
        if self.current_df is None:
            return
        
        self.gui.clear_searchbar()

        if self.gui.get_selected_countries():
            self.current_df = self._filter(self.current_df) 
            self.gui.display_datas(self.data_handler.get_country_col(), self.current_df)


    def on_clear_clicked(self):
        """
        Handles the "Clear" button click event.
        Resets filters and displays the full data set based on current user inputs.
        """
        if self.current_df is None:
            return
        
        # Recalculate delta without any country filtering
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
        """
        Handles the event when a column heading is clicked.
        Sorts the current DataFrame based on the clicked column and updates the GUI display.
        """
        if self.current_df is None:
            return
        
        self.current_df = self.data_handler.toggle_sort(icol, self.current_df)
        self.gui.display_datas(self.data_handler.get_country_col(), self.current_df)


    def _get_user_values(self):
        """Retrieve current indicator and year range selections from GUI."""
        indicator = self.gui.indicators_cb.get()
        start_year = self.gui.start_year_spinbox.get()
        end_year = self.gui.end_year_spinbox.get()

        return indicator, start_year, end_year
    

    def _min_max_years_boundary(self):
        """Extract minimum and maximum available years from loaded data."""
        # Extract first and last year from dataframe columns
        years_columns = self.data_handler.get_years_columns()
        
        return int(years_columns[0]), int(years_columns[-1])
    

    def _validate_years_input_user(self, start_year, end_year) -> bool:
        """Validate that years are in correct format and within available range."""
        pattern = "^\d{4}$"
        # Verify that both inputs match the 4-digit year format
        if (re.match(pattern, start_year)) and (re.match(pattern, end_year)):
            start_year, end_year= int(start_year), int(end_year)

            # Check that years are within the available data range
            return ((self.min_year<=start_year<=self.max_year) and
                (self.min_year<=end_year<=self.max_year))
                        
        else:
            return False


    def _filter(self, df):
        """Filter DataFrame to include only selected countries."""
        selected_countries = self.gui.get_selected_countries()
        country_col = self.data_handler.get_country_col()
        
        # Filter DataFrame to only include rows with selected countries
        return df[df[country_col].isin(selected_countries)]
        



