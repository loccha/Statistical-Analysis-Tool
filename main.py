from data_handler import DataHandler
from gui import GUI
from controller import AppController


def main():
   try:
      data_handler = DataHandler()
      controller = AppController(data_handler)
      gui = GUI(controller)
      
      controller.set_gui(gui)
      gui.run()


   except Exception as e:
      print("Error: ", e)


if __name__ == "__main__":
   main()
