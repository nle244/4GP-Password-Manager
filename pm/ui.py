import tkinter as tk 
from tkinter import ttk, filedialog, messagebox
from tkinter import *
from pathlib import Path
from datetime import datetime
from tkinter.filedialog import asksaveasfilename

import csv

# Allow code-completion tools to check Controller syntax
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pm.controller import Controller

proj_name = 'Password Manager'

#Main window of Password Manager UI
class MainWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.__create_home_widgets()
        self.__ctrl = None

    
    @property
    def ctrl(self) -> 'Controller':
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

    def __create_table_widgets(self):
        toolbar = tk.Frame(self.master, bd=1)
        eimg = PhotoImage(file='plus.png')
        save_button = ttk.Button(toolbar, text="Save", width ="4",command= self.__save_database)
        save_button.grid(row=0, column=0)
        addButton = ttk.Button(toolbar, text="Add", image=eimg,width="3.5", command=self.add_entry) #Need a way to view icons to make it look nicer
        addButton.grid(row=0,column=1)
        editButton = ttk.Button(toolbar, text="Edit" ,width="4") # command= self.__ctrl.edit_entry())
        editButton.grid(row=0, column=2)
        deleteButton = ttk.Button(toolbar, text="Delete" ,width="6") # command= self.__ctrl.delete_entry()))
        deleteButton.grid(row=0, column=3)
        
        
        toolbar.place(x=0,y=0)
        
    

    #Asks for a file to use from user, in this case a database file
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
            self.__create_table_widgets()

        
            

    
    
    #Clears home page once database is chosen
    def clear_frame(self):
            for widgets in self.winfo_children():
                        widgets.destroy()
    


    #Creates the table view which will read data from the database file once decrypted for use
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
        



    #Initialize a new database and save to computer
    def newbuttonclick(self, *args):
        default = 'newDatabase.csv'
        filename = asksaveasfilename(initialfile=default,
            defaultextension = '.csv', filetypes = [("All Files","*.*")])
        self.clear_frame()
        self.ctrl.set_filename(filename)
        self.ctrl.save()
        self.ctrl.load()
        self.__create_table_widgets()

    #Saves the database with the current values displayed
    def __save_database(self):
        '''Tell Controller to save the database to disk.'''
        self.__ctrl.save()


    #Adds a new entry to the database table using values inputted by the user
    #Needs some polishing on UI and cleanup in certain parts of function
    #Table needs to be "refreshed" in order to properly reflect changes done; added data does not show on table immediately
    def add_entry(self):
        newwin = Toplevel(self)
        newwin.geometry("300x150")
        newwin.focus()
        form_fields = {
            "Title": "", 
            "Username": "", 
            "Password": "", 
            "URL": "", 
            "Last_Modified": ""
        }
        Label(newwin, text="Title").grid(row=0, column=0, padx=5)
        titleentry = Entry(newwin, width = 25)
        titleentry.grid(row=0, column=1, pady=5)
        Label(newwin, text="Username").grid(row=1, column=0, padx=5)
        userentry = Entry(newwin, width = 25)
        userentry.grid(row=1, column=1, pady=5)
        Label(newwin, text="Password").grid(row=2, column=0, padx=5)
        passentry = Entry(newwin, width = 25)
        passentry.grid(row=2, column=1, pady=5)
        Label(newwin, text="URL").grid(row=3, column=0, padx=5)
        urlentry = Entry(newwin, width = 25)
        urlentry.grid(row=3, column=1, pady=5)
        
        #Obtains the user input and stores the values into a Dictionary entry to pass to Controller add_entry
        def get_input():
            form_fields["Title"] = titleentry.get()
            form_fields["Username"] = userentry.get()
            form_fields["Password"] = passentry.get()
            form_fields["URL"] = urlentry.get()
            form_fields["Last_Modified"] = datetime.now()

        

        submitButton = ttk.Button(newwin, text="Submit", command= lambda:[get_input(),self.__ctrl.add_entry(form_fields), self.show_info('Entry has been added.'), newwin.destroy(), self.__ctrl.refresh_table()])
        submitButton.grid(row=5, column=0, pady= 5)

        cancelButton = ttk.Button(newwin, text="Cancel", command=lambda:[newwin.destroy()])
        cancelButton.grid(row=5, column=2, pady= 5)

   
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