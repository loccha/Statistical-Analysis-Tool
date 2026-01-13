import csv
import pandas as pd

#------Model------

class DataHandler:
   
   def __init__(self, csv_path):
      self.df = pd.read_csv(csv_path).copy()
      self.df.columns = self.df.columns.str.strip()
   
   #returns a list of categories in alphabetic order
   def get_categories (self) -> list:
      return sorted(self.df['INDICATOR'].unique().tolist())
   
   #calculate en percentage the value of changes in the datas
   def calculate_delta(self, country, f_df, start_year, end_year):
      v_end = f_df.loc[country, end_year]
      v_start = f_df.loc[country, start_year]

      if v_end is not None and v_start is not None:
        return round(((v_end - v_start) / v_start) * 100, 2)
      else:
        return None
   
   def get_delta_df(self, category: str, start_year: str, end_year: str):
      filtered_df = self.df.copy()
    
      #filtering df to get countries as index and remove indicator
      filtered_df = (
         self.df[self.df['INDICATOR'] == category]
              .sort_values(by='COUNTRY', ascending=True)
              .set_index('COUNTRY')
              .drop(columns=['INDICATOR'])
      )

      # calculate delta between start year and end year for each country
      delta_df = pd.DataFrame(
                [self.calculate_delta(country, filtered_df, start_year, end_year) for country in filtered_df.index],
                index=filtered_df.index,
                columns=[f"{start_year}-{end_year}"]  
            )

      return delta_df








# class FileHandler:
   
#    def __init__(self):
#       self.path = ""
#       self.split_data=""
#       self.current_line=0
#       self.delta_line=0
   
   
#    def open_file(self, path):
#      with open(self.path, newline='') as csvfile:
#           reader = csv.reader(csvfile, skipinitialspace=True, delimiter=',')
#           self.split_data = [row for row in reader]
#           return self.split_data

#    def cell_name(self, i):
#     cell=self.split_data[self.current_line][i]
#     if (cell.find(":") >= 0):
#         cell = cell.split(":", 1)[0]+" :"
#     return (cell)
  
#    def extract_value(slef, cell):  
#     try:
#         num=""
#         cell = cell.split(":", 1)[1]
#         for x in cell:
#             if (x.isdigit() or x=="."):
#                 num=num+x
#         return float(num)
#     except Exception:
#         return 0.0
    

#    def display_delta(self, line1, line2, i): 
#       cell1 = self.split_data[self.current_line][i]
#       cell2 = self.split_data[self.delta_line][i]

#       cell1_analyse = FileHandler.extract_value(self, cell1)
#       cell2_analyse = FileHandler.extract_value(self, cell2)
#       res = cell1_analyse - cell2_analyse

#       return res