import pandas as pd
import re

class InvalidFileFormatError(Exception):
   '''Exception raised when CSV file is not the right format'''
   pass


class DataHandler:
   
   def __init__(self):
      self.df = None

      self.toggle=0
      self.icol_prec=-1

      self.country_col = 'COUNTRY'
      self.indicator_col = 'INDICATOR'


   def load_file(self, csv_path: str):
      self.df = pd.read_csv(csv_path).copy()
      self.df.columns = self.df.columns.str.strip()

      required_columns = [self.country_col, self.indicator_col]
      if not set(required_columns).issubset(self.df.columns):
         self.df = None
         raise InvalidFileFormatError(f"The file must include {self.country_col} and {self.indicator_col}.")
      
      for year in self.df.columns[2:]:
         #Accept years 1900 to 2099
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
               f"Column '{t}' must be of type text (object)."
               )
         
      for t in self.df.dtypes[2:]:
         if not pd.api.types.is_numeric_dtype(t):
            self.df = None
            raise InvalidFileFormatError(
               f"Column '{t}' must be a numeric type."
               )
   

   def get_indicators (self) -> list:
      '''returns a list of categories in alphabetic order'''
      return sorted(self.df[self.indicator_col].unique().tolist())
   

   def get_years_columns(self) -> list:
      return self.df.columns[2:]
      

   def get_delta_df(self, indicator: str, start_year: str, end_year: str):    
      #filtering df to get data's indicator from countries in alphabetical order 
      filtered_df = (
         self.df[self.df[self.indicator_col] == indicator]
              .sort_values(by=self.country_col, ascending=True)
              .drop(columns=[self.indicator_col])
              .reset_index(drop=True)
      )

      #creating new df with Countries, start year, end year and delta (changing in % from start to end year)
      delta_df = filtered_df.loc[:, [self.country_col, start_year, end_year]]
      delta_df['delta'] = round(((delta_df[end_year] - delta_df[start_year]) 
                                 / delta_df[start_year]) * 100, 3)

      return delta_df
   

   def get_country_col(self):
      return self.country_col

   
   def get_indicator_col(self):
      return self.indicator_col
   

   def toggle_sort(self, icol, df):
      if self.icol_prec!=icol:
         self.toggle=0
      else :
         self.toggle=1-self.toggle  #flips 0<->1

      self.icol_prec=icol

      if self.toggle==0:
         return df.sort_values(by=df.columns[icol], ascending=True)
      else :
         return df.sort_values(by=df.columns[icol], ascending=False)
      
 