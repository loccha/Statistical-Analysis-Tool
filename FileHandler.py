import csv
import re


class FileHandler:
   
   def __init__(self):
      self.path = ""
      self.split_data=""
      self.current_line=0
      self.delta_line=0
   
   
   def open_file(self, path):
     with open(self.path, newline='') as csvfile:
          reader = csv.reader(csvfile, skipinitialspace=True, delimiter=',')
          self.split_data = [row for row in reader]
          return self.split_data

   def cell_name(self, i):
    cell=self.split_data[self.current_line][i]
    if (cell.find(":") >= 0):
        cell = cell.split(":", 1)[0]+" :"
    return (cell)
  
   def extract_value(slef, cell):  
    try:
        num=""
        cell = cell.split(":", 1)[1]
        for x in cell:
            if (x.isdigit() or x=="."):
                num=num+x
        return float(num)
    except Exception:
        return 0.0
    

   def display_delta(self, line1, line2, i): 
      cell1 = self.split_data[self.current_line][i]
      cell2 = self.split_data[self.delta_line][i]

      cell1_analyse = FileHandler.extract_value(self, cell1)
      cell2_analyse = FileHandler.extract_value(self, cell2)
      res = cell1_analyse - cell2_analyse

      return res