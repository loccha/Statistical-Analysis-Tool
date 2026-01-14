import os

class AppController:
    
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.gui = None
        self.directory = os.getcwd()


        self.start_year = ''
        self.end_year = ''

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
            self.gui.display_indicators(self.data_handler.get_indicators())

    def on_enter_pressed(self):
        indicator = self.gui.indicators_cb.get()
        start_year = self.gui.start_year_spinbox.get()
        end_year = self.gui.end_year_spinbox.get()

        df = self.data_handler.get_delta_df(indicator, start_year, end_year)
        self.gui.display_datas(df)


