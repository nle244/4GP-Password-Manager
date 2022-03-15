import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from tkinter.filedialog import asksaveasfilename
import csv


proj_name = 'Password Manager'

#Main window of Password Manager UI
class MainWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.__create_home_widgets()
        self.__ctrl = None

    
    @property
    def ctrl(self):
        '''Controller.'''
        return self.__ctrl


    @ctrl.setter
    def ctrl(self, controller):
        '''Controller.'''
        self.__ctrl = controller
    

    #Initial layout just to get started; may need to organize into frames later on
    def __create_home_widgets(self):
        self.label1 = ttk.Label(self, font=("Arial",25), text="Welcome")
        self.label1.grid(row=0, column=0)
        #label1.place(relx=.5, y= 50, anchor=tk.CENTER)

        self.homebutton1 = ttk.Button(self, text="New Database", command = self.newbuttonclick)
        self.homebutton1.grid(row=1, column=0)
        #homebutton1.place(x=150, y= 200)

        self.homebutton2 = ttk.Button(self, text="Open Database", command= self.load_filepath)
        self.homebutton2.grid(row=1, column=1)
        #homebutton2.place(x =350, y=200)

    

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

        if filename != None and filename != '':
            self.__ctrl.set_filename(filename)
            self.__ctrl.load()

        
            

    
    
    #Clears home page once database is chosen
    def clear_frame(self):
            for widgets in self.winfo_children():
                        widgets.destroy()
    


    #Create a table which will read data from the database file once decrypted for use
    def create_db_table(self, db):
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

        for row in db:
            title = row['Title']
            username = row['Username']
            password = row['Password']
            url = row['URL']
            last_modified = row['Last_Modified']
            test_table.insert("", tk.END, values=(title, username, password, url, last_modified))

        test_table.grid(row=0, column=0)
        save_button = ttk.Button(self, text="Save Database", command= self.__save_database)
        save_button.grid(row=1, column=0)



    #Initialize a new database and save to computer
    def newbuttonclick(self, *args):
        default = 'newDatabase.csv'
        filename = asksaveasfilename(initialfile=default,
            defaultextension = '.csv', filetypes = [("All Files","*.*")])
        self.clear_frame()
        self.ctrl.set_filename(filename)
        self.ctrl.save()
        self.ctrl.load()


    def __save_database(self):
        '''Tell Controller to save the database to disk.'''
        self.__ctrl.save()


    def show_error(self, message):
        '''Show an error message dialog.

        Params
            message: Message to display in the dialog.
        '''
        messagebox.showerror('Error', message)


    def show_info(self, message):
        '''Show an info dialog.

        Params
            message: Message to dispaly in the dialog.
        '''
        messagebox.showinfo('Info', message)


    #def addEntry(self, *args):


    #def editEntry(self, *args):
