import pandas as pd
import re

class InvalidFileFormatError(Exception):
   """Exception raised when CSV file is not the right format"""
   pass


class DataHandler:
   """
   Model layer of the application (MVC pattern).

   Responsible for:
   - Loading and validating CSV data files
   - Calculating deltas for indicators over specified years by country
   - Providing data to the controller for GUI display

   Attributes:
         df (pd.DataFrame): Loaded data frame from the CSV file
         toggle (int): Toggle state for sorting (0: ascending, 1: descending)
         icol_prec (int): Previously clicked column index for sorting
         country_col (str): Expected name of the country column in the CSV
         indicator_col (str): Expected name of the indicator column in the CSV
   """
   
   def __init__(self):
      self.df = None

      self.toggle=0
      self.icol_prec=-1

      self.country_col = 'COUNTRY'
      self.indicator_col = 'INDICATOR'


   def load_file(self, csv_path: str):
      """
      Loads and validates the CSV file at the given path.
      Raises InvalidFileFormatError if the file format is incorrect.
      """
      self.df = pd.read_csv(csv_path).copy()
      # Remove leading/trailing whitespace from column names
      self.df.columns = self.df.columns.str.strip()

      required_columns = [self.country_col, self.indicator_col]
      if not set(required_columns).issubset(self.df.columns):
         self.df = None
         raise InvalidFileFormatError(f"The file must include {self.country_col} and {self.indicator_col}.")
      
      # Validate year columns (columns after first 2: COUNTRY and INDICATOR)
      for year in self.df.columns[2:]:
         # Accept years 1900 to 2099
         if not re.match("^(19|20)\d{2}$", year):
            self.df = None
            raise InvalidFileFormatError(
               f"Invalid year column: '{year}'. "
                "Year columns must be between 1900 and 2099."
               )

      for t in self.df.dtypes[:2]:
         if not pd.api.types.is_string_dtype(t):
            self.df = None
            raise InvalidFileFormatError(
               f"Column '{t}' must be of type text."
               )
         
      for t in self.df.dtypes[2:]:
         if not pd.api.types.is_numeric_dtype(t):
            self.df = None
            raise InvalidFileFormatError(
               f"Column '{t}' must be a numeric type."
               )
   

   def get_indicators (self) -> list:
      """returns a list of indicators"""
      return sorted(self.df[self.indicator_col].unique().tolist())
   

   def get_years_columns(self) -> list:
      """returns a list of years columns as strings"""
      return self.df.columns[2:]
      

   def get_delta_df(self, indicator: str, start_year: str, end_year: str) -> pd.DataFrame:
      """
      Returns a DataFrame with countries, start year, end year, and delta percentage
      for the specified indicator between the given years.
      """
      # Filter to get specified indicator data, sort countries alphabetically, remove indicator column
      filtered_df = (
         self.df[self.df[self.indicator_col] == indicator]
              .sort_values(by=self.country_col, ascending=True)
              .drop(columns=[self.indicator_col])
              .reset_index(drop=True)
      )

      # Create new df: Countries, start year value, end year value, and delta percentage
      delta_df = filtered_df.loc[:, [self.country_col, start_year, end_year]]
      delta_df['delta'] = round(((delta_df[end_year] - delta_df[start_year]) 
                                 / delta_df[start_year]) * 100, 3)

      return delta_df
   

   def get_country_col(self):
      return self.country_col

   
   def get_indicator_col(self):
      return self.indicator_col
   

   def toggle_sort(self, icol: int, df: pd.DataFrame) -> pd.DataFrame:
      """
      Toggles ascending sorting of the DataFrame based on the clicked column index.
      If the same column is clicked again, it reverses the sort order.
      """
      if self.icol_prec!=icol:
         self.toggle=0
      else :
         # Toggle between 0 and 1 to reverse sort order
         self.toggle=1-self.toggle

      self.icol_prec=icol

      if self.toggle==0:
         return df.sort_values(by=df.columns[icol], ascending=True)
      else :
         return df.sort_values(by=df.columns[icol], ascending=False)
      
 
