from cgi import test
import tkinter as tk 
from tkinter import ttk, filedialog, messagebox
from tkinter import *
from pathlib import Path
from datetime import datetime
from tkinter.filedialog import asksaveasfilename

import platform

# Allow code-completion tools to check Controller syntax
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pm.controller import Controller

proj_name = 'Password Manager'
HEADER = ['Title', 'Username', 'Password', 'URL', 'Last_Modified']

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
        self.label1 = ttk.Label(
            self, 
            font=("Arial",25), 
            text="Welcome"
            )
        self.label1.grid(row=0, column=0)
        #label1.place(relx=.5, y= 50, anchor=tk.CENTER)

        self.homebutton1 = ttk.Button(
            self, 
            text="New Database", 
            command = self.newbuttonclick
            )
        self.homebutton1.grid(row=1, column=0)
        #homebutton1.place(x=150, y= 200)

        self.homebutton2 = ttk.Button(
            self, 
            text="Open Database", 
            command= self.load_filepath
            )
        self.homebutton2.grid(row=1, column=1)
        #homebutton2.place(x =350, y=200)

    

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
            self.ctrl.load(ask_passwd=True)

        
            

    
    
    #Clears home page once database is chosen
    def clear_frame(self):
            for widgets in self.winfo_children():
                        widgets.destroy()
    


    #Creates the table view which will read data from the database file once decrypted for use
    def create_db_table(self, db):
        self.clear_frame()
        self.test_table = ttk.Treeview(self)
        self.test_table['columns'] = ('Title', 'Username', 'Password', 'URL', 'Last_Modified')
        self.test_table['show'] = 'headings'
        self.test_table.column("Title", anchor=tk.CENTER, width=50)
        self.test_table.column("Username", anchor=tk.CENTER, width=80)
        self.test_table.column("Password", anchor=tk.CENTER, width=80)
        self.test_table.column("URL", anchor=tk.CENTER, width=100)
        self.test_table.column("Last_Modified", anchor=tk.CENTER, width=100)
        self.test_table.heading("Title", text="Title", anchor=tk.CENTER)
        self.test_table.heading("Username", text="Username", anchor=tk.CENTER)
        self.test_table.heading("Password", text="Password", anchor=tk.CENTER)
        self.test_table.heading("URL", text="URL", anchor=tk.CENTER)
        self.test_table.heading("Last_Modified", text="Last_Modified", anchor=tk.CENTER)

        for key in db:
            entry = [
                db[key]['Title'],
                db[key]['Username'],
                db[key]['Password'],
                db[key]['URL'],
                db[key]['Last_Modified']
            ]
            if self.test_table.exists(key):
                self.test_table.delete(key)
            self.test_table.insert("", tk.END, iid=key, values=entry)

        toolbar = ttk.Frame(self)
        eimg = PhotoImage(file='plus.png')

        save_button = ttk.Button(
            toolbar, 
            text="Save", 
            width ="4",
            command= self.__save_database
            )
        save_button.grid(row=0, column=0)

        addButton = ttk.Button(toolbar, 
        text="Add", 
        image=eimg,
        width="3.5", 
        command=self.add_entry
        ) #Need a way to get "plus.png" to show to make it look nicer
        addButton.grid(row=0,column=1)

        editButton = ttk.Button(
            toolbar, 
            text="Edit",
            width="4", 
            command= self.edit_entry,
            state = DISABLED
            )
        editButton.grid(row=0, column=2)

        deleteButton = ttk.Button(
            toolbar, 
            text="Delete" ,
            width="6", 
            command= self.delete_entry,
            state=DISABLED
            )
        deleteButton.grid(row=0, column=3)

        def enable_editdelete(event):
            editButton['state'] = NORMAL
            deleteButton['state'] = NORMAL

        self.test_table.bind('<<TreeviewSelect>>', enable_editdelete)

        toolbar.grid(row=0,column=0)
        self.test_table.grid(row=1, column=0, padx=20, pady=20)
        

    

    #Initialize a new database and save to computer
    def newbuttonclick(self, *args):
        default = 'newDatabase.csv'
        filename = asksaveasfilename(initialfile=default,
            defaultextension = '.csv', filetypes = [("All Files","*.*")])
            
        if filename != None and filename != '':
            self.ctrl.new_database(filename)


    #Saves the database with the current values displayed
    def __save_database(self):
        '''Tell Controller to save the database to disk.'''
        self.__ctrl.save()


    #Adds a new entry to the database table using values inputted by the user
    #Needs some polishing on UI and cleanup in certain parts of function
    def add_entry(self):
        entry = EntryDialog(self, edit=False).get()
        if entry != None:
            self.ctrl.add_entry(entry)


    #Edits specified row from the table and update it with new values
    def edit_entry(self):
        iid = self.test_table.focus()
        if iid:
            old_values = self.ctrl.get_entry(iid)
            entry = EntryDialog(self, edit=True, old_entry=old_values).get()
            if entry != None:
                self.ctrl.edit_entry(iid, entry)


    #Deletes specified row from the table and removes its entry from the database
    def delete_entry(self):
        iid = self.test_table.focus()
        selected = self.test_table.item(iid)['values']

        confirm = messagebox.askyesno(
            title='Confirm',
            message = 'Are you sure you want to delete "{}" entry?'.format(selected[0])
        )

        if confirm:
            self.ctrl.delete_entry(iid)
        
            

   
    def show_error(self, message):
        '''Show an error message dialog.

        Params
            message: Message to display in the dialog.
        '''
        messagebox.showerror('Error', message)


    def show_info(self, message):
        '''Show an info dialog.

        Params
            message: Message to display in the dialog.
        '''
        messagebox.showinfo('Info', message)


    def show_password_dialog(self, message):
        return PasswordDialog(self, message).get()



class PasswordDialog(Toplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.__passwd = StringVar()
        self.__msg = message
        self.__submit = False

        self.__render()


    def __render(self):
        self.title('Master Password')
        if platform.system() == 'Windows':
            self.attributes('-toolwindow', True)
        self.columnconfigure(0, weight=1)
        self.resizable(width=False, height=False)

        self.__view = ttk.Frame(self)
        self.__view.grid(row=0, column=0)
        self.__view['padding'] = (10, 10, 10, 10)
        ttk.Label(
            self.__view, text=self.__msg
        ).grid(row=0, column=0)
        ttk.Entry(
            self.__view, show='*', textvariable=self.__passwd
        ).grid(row=1, column=0)

        self.__button_frame = ttk.Frame(self.__view)
        self.__button_frame.grid(row=2, column=0)
        ttk.Button(
            self.__button_frame, text='Submit', command=self.__submit_callback
        ).grid(row=0, column=0)
        ttk.Button(
            self.__button_frame, text='Cancel', command=self.__cancel_callback
        ).grid(row=0, column=1)


    def __submit_callback(self):
        self.__submit = True
        self.destroy()


    def __cancel_callback(self):
        self.destroy()


    def get(self):
        '''Get user's input.

        Returns
            A str variable containing user's input, or None if user clicked 'Cancel'.
        '''
        self.wait_window(self)
        if self.__submit:
            return self.__passwd.get()
        return None



class EntryDialog(Toplevel):

    def __init__(self, parent, edit=True, old_entry=None):
        super().__init__(parent)
        self.__fields = dict()
        self.__submit = False
        for header in HEADER:
            if old_entry == None:
                self.__fields[header] = StringVar(self)
            else:
                self.__fields[header] = StringVar(self, old_entry[header])

        self.__setup_root(edit)
        self.__setup_view()
        self.__setup_widgets(old_entry)


    def __setup_view(self):
        self.__view = ttk.Frame(self)
        self.__view.grid(row=0, column=0)


    def __setup_root(self, edit):
        self.focus()
        self.resizable(width=False, height=False)
        self.columnconfigure(0, weight=1)

        if platform.system() == 'Windows':
            self.attributes('-toolwindow', True)

        if edit:
            self.title('Edit Entry')
        else:
            self.title('New Password Entry')


    def __setup_widgets(self, old_entry):
        width = 25
        pad = 5

        # setup fields grouping
        fields_frame = ttk.Frame(self.__view, padding=(10,10,10,10))
        fields_frame.grid(row=0, column=0)

        for row in range(len(HEADER[:-1])):
            header = HEADER[row]
            ttk.Label(
                fields_frame, text=header.replace('_', ' ')
            ).grid(row=row, column=0, padx=pad, sticky='e')
            ttk.Entry(
                fields_frame, textvariable=self.__fields[header], width=width
            ).grid(row=row, column=1, padx=pad)

        # setup button grouping
        button_frame = ttk.Frame(self.__view, padding=(10,10,10,10))
        button_frame.grid(row=1, column=0, sticky='we')
        button_frame.columnconfigure(1, weight=2)

        ttk.Button(
            button_frame, text='Submit', command=self.__submit_callback
        ).grid(row=0, column=0, sticky='w')
        ttk.Frame(button_frame).grid(row=0,column=1)
        ttk.Button(
            button_frame, text='Cancel', command=self.__cancel_callback
        ).grid(row=0, column=2, sticky='e')


    def __submit_callback(self):
        self.__submit = True
        self.destroy()


    def __cancel_callback(self):
        self.destroy()


    def get(self):
        '''Get user's input.

        Returns
            A dict containing user's input, or None if cancelled.
        '''
        self.wait_window(self)
        if self.__submit:
            result = {
                key: self.__fields[key].get() for key in HEADER
            }
            result[HEADER[-1]] = str(datetime.now()).split('.')[0]
            return result
        return None
