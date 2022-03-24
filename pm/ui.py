from cgi import test
import tkinter as tk 
from tkinter import ttk, filedialog, messagebox
from tkinter import *
from pathlib import Path
from datetime import datetime

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
        self.__ctrl = None

    @property
    def ctrl(self) -> 'Controller':
        '''Controller.'''
        return self.__ctrl


    @ctrl.setter
    def ctrl(self, controller):
        '''Controller.'''
        self.__ctrl = controller

        self.__tree_page = TreePage(self, controller)
        self.__tree_page.grid(row=0, column=0, sticky='nsew')

        self.__home_page = HomePage(self, controller)
        self.__home_page.grid(row=0, column=0, sticky='nsew')

        self.display_home_page()


    def display_home_page(self):
        '''Display the home page'''
        self.__tree_page.grid_remove()
        self.__home_page.grid()


    def display_tree_page(self, db):
        '''Display the tree page
        Params
            db: dictionary of entries to show.
        '''
        self.__home_page.grid_remove()
        self.__tree_page.grid()
        self.__tree_page.refresh_treeview(db)


    def get_iid(self):
        '''Return the IID of the currently selected item in Treeview.'''
        return self.__tree_page.get_iid()


    def show_confirm(self, message):
        '''Show yes/no confirm dialog.
        Params
            message: message to show.
        Returns
            True if user clicks Yes, False otherwise.
        '''
        return messagebox.askyesno(title='Confirm', message=message)

   
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


    def show_entry_dialog(self, old_values=None):
        '''Show an entry input dialog.
        Params
            old_values=None: dictionary containing old values
        '''
        if old_values:
            return EntryDialog(self, edit=True, old_entry=old_values).get()
        return EntryDialog(self, edit=False).get()


    def show_load_dialog(self):
        filetypes = (
            ('CSV files', '*.csv'),
            ('Quick Key database files', '*.qk'),
            ('All files', '.*')
        )
        filename = filedialog.askopenfilename(
            title='Choose a file.',
            initialdir=Path.home(),
            filetypes=filetypes
        )
        return filename


    def show_password_dialog(self, message):
        return PasswordDialog(self, message).get()


    def show_save_dialog(self):
        default = 'newDatabase.qk'
        filename = filedialog.asksaveasfilename(initialfile=default,
            defaultextension = '.qk', filetypes = [("All Files","*.*")])
        return filename



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
        self.__setup_widgets()


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


    def __setup_widgets(self):
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



class Page(ttk.Frame):
    def __init__(self, parent, ctrl):
        super().__init__(parent)
        self.__ctrl = ctrl

    @property
    def ctrl(self) -> 'Controller':
        return self.__ctrl


    @ctrl.setter
    def ctrl(self, other):
        self.__ctrl = other


    def show(self):
        self.tkraise()



class HomePage(Page):
    def __init__(self, parent, ctrl=None):
        super().__init__(parent, ctrl)
        self.__setup_banner()
        self.__setup_buttons()


    def __setup_banner(self):
        ttk.Label(
            self, font=("Arial",25), text="Quick Key"
        ).grid(row=0, column=0)


    def __setup_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, sticky='we')
        button_frame.columnconfigure(1, weight=2)

        ttk.Button(
            button_frame, text="New Database", command=self.ctrl.new_database
        ).grid(row=0, column=0)
        ttk.Frame(button_frame).grid(row=0, column=1)
        ttk.Button(
            button_frame, text="Open Database",
            command=lambda: self.ctrl.load(ask_passwd=True)
        ).grid(row=0, column=2)



class TreePage(Page):
    def __init__(self, parent, ctrl=None):
        super().__init__(parent, ctrl)

        self.__setup_treeview()
        self.__setup_toolbar()


    def __setup_treeview(self):
        self.__tree = ttk.Treeview(self, columns=HEADER, show='headings')
        self.__tree.grid(row=1, column=0)

        def enable_edit_and_delete(event):
            if self.__tree.focus():
                self.__toolbar.children['edit']['state'] = NORMAL
                self.__toolbar.children['delete']['state'] = NORMAL
            else:
                self.__toolbar.children['edit']['state'] = DISABLED
                self.__toolbar.children['delete']['state'] = DISABLED

        self.__tree.bind('<<TreeviewSelect>>', enable_edit_and_delete)

        for header in HEADER:
            self.__tree.column(
                header, width=80, anchor=tk.CENTER
            )
            self.__tree.heading(
                header, text=header.replace('_', ' '), anchor=tk.CENTER
            )


    def __setup_toolbar(self):
        # setup toolbar
        self.__toolbar = ttk.Frame(self, padding=(10,10,10,10))
        self.__toolbar.grid(row=0, column=0, sticky='we')
        self.__toolbar.columnconfigure(1, weight=2)
        eimg = PhotoImage(file='plus.png')
        pad = 5
        width = 8

        ttk.Button(
            self.__toolbar, text="Save", width=width,
            command=self.ctrl.save
        ).grid(row=0, column=0, padx=pad)

        ttk.Frame(self.__toolbar).grid(row=0, column=1)

        ttk.Button(
            self.__toolbar, text="Add", image=eimg, width=width,
            command=self.ctrl.add_entry
        ).grid(row=0, column=2, padx=pad)

        ttk.Button(
            self.__toolbar, text="Edit", name='edit', width=width,
            command=self.ctrl.edit_entry, state = DISABLED
        ).grid(row=0, column=3, padx=pad)

        ttk.Button(
            self.__toolbar, text="Delete", name='delete', width=width,
            command=self.ctrl.delete_entry, state=DISABLED
        ).grid(row=0, column=4, padx=pad)


    def get_iid(self):
        return self.__tree.focus()


    def refresh_treeview(self, db: dict):
        self.__tree.delete(*self.__tree.get_children())
        for key in db:
            entry = list(db[key].values())
            self.__tree.insert("", tk.END, iid=key, values=entry)
            del entry
