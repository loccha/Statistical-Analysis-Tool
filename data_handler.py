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
   
   #calculate en percentage the value of changes in the datas
   def calculate_delta(self, country, f_df, start_year, end_year):
      v_end = f_df.loc[country, end_year]
      v_start = f_df.loc[country, start_year]

      if v_end is not None and v_start is not None:
        return round(((v_end - v_start) / v_start) * 100, 2)
      else:
        return None
   

   def get_delta_df(self, indicator: str, start_year: str, end_year: str):
      filtered_df = self.df.copy()
    
      #filtering df to get countries as index and remove indicator
      filtered_df = (
         self.df[self.df['INDICATOR'] == indicator]
              .sort_values(by='COUNTRY', ascending=True)
              .drop(columns=['INDICATOR'])
              .reset_index(drop=True)
      )

      countries = filtered_df['COUNTRY']

      # calculate delta between start year and end year for each country
      delta_df = pd.DataFrame({
        'COUNTRY': countries,
        f"{start_year}-{end_year}": [self.calculate_delta(country, filtered_df, start_year, end_year) for country in filtered_df.index]
      })

      return delta_df