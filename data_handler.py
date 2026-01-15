import pandas as pd

class DataHandler:
   
   def __init__(self):
      self.df = None

   def load_file(self, csv_path):
      self.df = pd.read_csv(csv_path).copy()
      self.df.columns = self.df.columns.str.strip()         #cleans the columns
   
   #returns a list of categories in alphabetic order
   def get_indicators (self) -> list:
      return sorted(self.df['INDICATOR'].unique().tolist())
   

   def get_delta_df(self, indicator: str, start_year: str, end_year: str):
      filtered_df = self.df.copy()
    
      #filtering df to get data's indicator from countries in alphabetical order 
      filtered_df = (
         self.df[self.df['INDICATOR'] == indicator]
              .sort_values(by='COUNTRY', ascending=True)
              .drop(columns=['INDICATOR'])
              .reset_index(drop=True)
      )

      #creating new df with Countries, start year, end year and delta (changing in % from start to end year)
      delta_df = filtered_df.loc[:, ['COUNTRY', start_year, end_year]]
      delta_df['delta'] = round(((delta_df[end_year] - delta_df[start_year]) / delta_df[start_year]) * 100, 3)

      return delta_df