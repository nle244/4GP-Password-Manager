import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from tkinter.filedialog import asksaveasfile
import csv
import platform

proj_name = 'Password Manager'

#Main window of Password Manager UI
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__(className=proj_name)

        self.title(proj_name) 
        self.geometry("600x300")
        self.resizable(0,0)
        if platform.system() == 'Windows':
            self.attributes('-toolwindow', True)
        self._file_path = tk.StringVar()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.__create_home_widgets()
    

    

    #Initial layout just to get started; may need to organize into frames later on
    def __create_home_widgets(self):
        label1 = tk.Label(self, font=("Arial",25), text="Welcome")
        label1.place(relx=.5, y= 50, anchor=tk.CENTER)

        homebutton1 = tk.Button(self, text="New Database", command = self.newbuttonclick)
        homebutton1.place(x=150, y= 200)

        homebutton2 = tk.Button(self, text="Open Database", command= self.load_filepath)
        homebutton2.place(x =350, y=200)

    

    #Asks for a file to use from user, in this case a database file
    #For test purposes, text files are currently being used
    def load_filepath(self, *args):

        filetypes = (
            ('Database files', '*.csv'),
            ('All files', '.*')
        )

        filename = filedialog.askopenfilename(
            title='Choose a file.',
            initialdir=Path.home(),
            filetypes=filetypes
        )
        if (filename!= ''):
            self._file_path.set(filename)
            self._create_db_table()
        else:
            return

        
            

    
    
    #Clears home page once database is chosen
    def clear_frame(self):
            for widgets in self.winfo_children():
                        widgets.destroy()
    


    #Create a table which will read data from the database file once decrypted for use
    def _create_db_table(self):
        self.clear_frame()
        test_table = ttk.Treeview(self)
        test_table.grid(row=1, column=1, padx=20, pady=20)
        test_table['columns'] = ('Title', 'Username', 'Password', 'URL', 'Last_Modified')
        test_table['show'] = 'headings'
        test_table.column("Title", anchor=tk.CENTER, width=50)
        test_table.column("Username", anchor=tk.CENTER, width=80)
        test_table.column("Password", anchor=tk.CENTER, width=80)
        test_table.column("URL", anchor=tk.CENTER, width=100)
        test_table.column("Last_Modified", anchor=tk.CENTER, width=100)
        test_table.heading("Title", text="Title", anchor=tk.CENTER)
        test_table.heading("Username", text="Username", anchor=tk.CENTER)
        test_table.heading("Password", text="Password", anchor=tk.CENTER)
        test_table.heading("URL", text="URL", anchor=tk.CENTER)
        test_table.heading("Last_Modified", text="Last_Modified", anchor=tk.CENTER)
        try:
         with open(self._file_path.get(), "r") as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                title = row['Title']
                username = row['Username']
                password = row['Password']
                url = row['URL']
                last_modified = row['Last_Modified']
                test_table.insert("", tk.END, values=(title, username, password, url, last_modified))
        except:
            messagebox.showerror('Error', 'File is either corrupted or in an invalid format.')
            test_table.destroy()
            self.__create_home_widgets()
            return None
        test_table.place(x= 100, y=40)


    #Initialize a new database and save to computer
    def newbuttonclick(self, *args):
        f = asksaveasfile(initialfile = 'newDatabase.txt', 
            defaultextension = '.txt', filetypes = [("All Files","*.*")])
        #self._file_path.set(filename)
        self.clear_frame()
        self._create_db_table()


    #def addEntry(self, *args):


    #def editEntry(self, *args):
