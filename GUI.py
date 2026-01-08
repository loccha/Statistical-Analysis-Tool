import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from FileHandler import FileHandler
import sys
import os

class Interface:

    def __init__(self, root):
        self.path=""
        self.split_data=[]
        self.current_line=0
        self.delta_line=0

        self.root = root
        self.root.title("Stats reader")
        self.root.geometry('550x660')
        self.font1=('Bahnschrift', 11, 'normal')
        self.root.bind('<Return>', lambda event:self.read())

        self.entries_frame=tk.Frame()

        self.file_label = tk.Label(self.entries_frame, font=self.font1, text='File:')
        self.file_label.grid(sticky=tk.W, row=0, column=0)
        self.file_entry = tk.Entry(self.entries_frame, width=20)
        self.file_entry.grid(sticky=tk.W, row=0, column=1, padx=20)
        self.file_entry.focus()
        self.file_entry.bind('<Enter>', lambda event:self.enable())

        self.open_button = tk.Button(self.entries_frame, text="Open", command=self.open_file)
        self.open_button.grid(row=0, column=2, padx=40)

        self.current_label = tk.Label(self.entries_frame, font=self.font1, text='Current: ')
        self.current_label.grid(sticky=tk.W, row=1, column=0)
        self.current_entry = tk.Entry(self.entries_frame, width=20)
        self.current_entry.insert(tk.END, self.current_line)
        self.current_entry.grid(sticky=tk.W, row=1, column=1, padx=20)

        self.delta_label = tk.Label(self.entries_frame, font=self.font1, text='Delta: ')
        self.delta_label.grid(sticky=tk.W, row=2, column=0)
        self.delta_entry = tk.Entry(self.entries_frame, width=20)
        self.delta_entry.insert(tk.END, self.delta_line)
        self.delta_entry.grid(sticky=tk.W, row=2, column=1, padx=20)

        self.stats_tree_frame = tk.Frame()

        self.scroll_bar = tk.Scrollbar(self.stats_tree_frame)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.stats_tree = ttk.Treeview(self.stats_tree_frame, yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.stats_tree.yview)

        self.stats_tree.tag_configure("positive", foreground='green')
        self.stats_tree.tag_configure("negative", foreground='red')
        self.stats_tree['columns'] = ('data_names', 'current_value', 'delta_value')

        self.stats_tree.column("#0", width=0, stretch=tk.NO)
        self.stats_tree.column("data_names", anchor=tk.W, width=175)
        self.stats_tree.column("current_value", anchor=tk.W, width=100)
        self.stats_tree.column("delta_value", anchor=tk.W, width=100)

        self.stats_tree.heading("#0", text="", anchor=tk.CENTER)
        self.stats_tree.heading("data_names", text="", anchor=tk.CENTER)
        self.stats_tree.heading("current_value", text="Current", anchor=tk.CENTER)
        self.stats_tree.heading("delta_value", text="Delta", anchor=tk.CENTER)

        self.stats_tree.pack(expand=True, fill='y')
        
        self.button_frame = tk.Frame()
        self.button_p10 = tk.Button(self.button_frame, text="Prev10", command = self.prev10_button)
        self.button_p10.grid(row=4, column=0, padx=25)
        self.button_p = tk.Button(self.button_frame, text=" Prev ", command=self.prev_button)
        self.button_p.grid(row=4, column=1, padx=25)
        self.root.bind('<Left>', lambda event: self.prev_button())
        self.button_n = tk.Button(self.button_frame, text=" Next ", command=self.next_button)
        self.button_n.grid(row=4, column=2, padx=25)
        self.root.bind('<Right>', lambda event: self.next_button())
        self.button_n10 = tk.Button(self.button_frame, text="Next10", command=self.next10_button)
        self.button_n10.grid(row=4, column=3, padx=25)

        self.entries_frame.pack(pady=15)
        self.stats_tree_frame.pack(expand=True, fill='y')
        self.button_frame.pack(pady=20)

        self.directory = '/'

        if(len(sys.argv)==2):
          self.file_entry.insert(tk.END, sys.argv[1])
          self.directory = os.path.dirname(self.path)
          self.read()
    
    def open_file(self):
        '''To open a browser to select a file
        '''
        Interface.enable(self)
        self.file_entry.delete(0, tk.END)
        filename = filedialog.askopenfilename(
            initialdir=self.directory,
            title="Select a file",
            filetypes = (("CSV files", "*.csv*"), ("all files","*.*"))
            )
        self.file_entry.insert(0, filename)
        self.directory = os.path.dirname(self.path)


    def enable(self):
        '''Change the entry state from readonly to normal to change manualy the file
        '''
        self.file_entry.config(state="normal") 

    def dir_Button(self): 
        '''Applies to the direction buttons
        '''
        Interface.reset(self)
        Interface.boundaries(self)
        Interface.replace(self)
        Interface.display_frame(self)
        
    def reset(self):
        ''' Delete everything in self.stats(Treeview)
        '''
        for i in self.stats_tree.get_children():
            self.stats_tree.delete(i)
    
    def boundaries(self):
        '''Sets boundaries depending on the file's size (starts to 0-0, ends at the last line's file)
        '''
        if(self.current_line<=0 or self.delta_line<0):
           self.delta_line=0
           self.current_line=0
        elif(self.current_line>len(self.split_data)-1 or self.delta_line>len(self.split_data)-1):
            self.delta_line=len(self.split_data)-1
            self.current_line=len(self.split_data)-1
        else:
           self.delta_line=self.current_line-1

    def replace(self):
        '''For buttons: to iterate current and delta's line and display it
        '''
        self.current_entry.delete(0, tk.END)
        self.delta_entry.delete(0, tk.END)
        self.current_entry.insert(tk.END, self.current_line)
        self.delta_entry.insert(tk.END, self.delta_line)

    def display_frame(self):
        ''' Is displaying names, current values and delta values in the Treeview
        '''
        for i in range (len(self.split_data[self.current_line])):

            cell=FileHandler.cell_name(self, i)

            value = self.split_data[self.current_line][i]
            value = FileHandler.extract_value(self, value)

            delta = FileHandler.display_delta(self, self.current_line, self.delta_line, i)
            if (delta > 0):
                delta = "+"+str(delta)
                self.stats_tree.insert(parent='', index='end', iid=i, text='', values=((cell),(value), (delta),), tags=("positive"))
            elif (delta<0):
                self.stats_tree.insert(parent='', index='end', iid=i, text='', values=((cell),(value), (delta),), tags=("negative"))
            else:
                self.stats_tree.insert(parent='', index='end', iid=i, text='', values=((cell),(value), (delta)))


    def next_button(self):
        self.current_line+=1
        Interface.dir_Button(self)

    def prev_button(self):
        self.current_line-=1
        Interface.dir_Button(self)
       
    def next10_button(self):
        self.current_line+=10
        Interface.dir_Button(self)

    def prev10_button(self):
        self.current_line-=10
        Interface.dir_Button(self)

    def read(self):
        '''Command for 'read' button
        '''
        try:
          Interface.reset(self)
          Interface.get_entries(self) 
          Interface.split_path(self)
          Interface.display_frame(self)
          self.file_entry.config(state="readonly")
        except:
          Interface.error(self)
      

    def get_entries(self):
        '''Read content of path, current and delta
        '''
        self.path = self.file_entry.get()
        self.current_line = int(self.current_entry.get())
        self.delta_line = int(self.delta_entry.get())

    def error(self):
        '''Error message box if exception
        '''
        messagebox.showinfo("Stats reader", "Please enter valid information")

    def split_path(self):
        '''Is spliting file into a lines array
        '''
        self.split_data = FileHandler.open_file(self, self.path)         
    
if __name__=='__main__':
    root = tk.Tk()
    obj=Interface(root)
    root.mainloop()

