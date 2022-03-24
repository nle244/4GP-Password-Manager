from pm.ui import MainWindow
from pm.storage import Storage
from pm.storage import HEADER
from pm.exceptions import (
    InvalidColumns,
    InvalidFileFormat,
)

class Controller:
    '''Provides database-related function endpoints for the UI to use.'''

    def __init__(self, ui: MainWindow, storage: Storage):
        '''Constructor.

        Params
            ui: Reference to the user interface.
            storage: Reference to the Storage class.
        '''
        self.__ui = ui
        self.__storage = storage


    def add_entry(self):
        '''Tell Storage to add a new entry to the database in memory.
        Tell MainWindow to render an error message if column values are wrong.
        Params
            entry: Dictionary containing a new entry.
        '''
        entry = self.__ui.show_entry_dialog()
        if entry:
            try:
                self.__storage.add_entry(entry)
                self.__populate_table()
            except InvalidColumns as e:
                self.__ui.show_error(str(e))


    def delete_entry(self):
        '''Tell Storage to delete an existing entry.
        Params
            entry: Dictionary containing the entry to delete.
        '''
        iid = self.__ui.get_iid()
        if iid:
            title = self.__storage.get_entry(iid)['Title']
            confirm = self.__ui.show_confirm('Delete "{}" entry?'.format(title))
            if confirm:
                self.__storage.delete_entry(iid)
                self.__populate_table()


    def edit_entry(self):
        '''Tell Storage to edit an existing entry.
        Params
            old_entry: Dictionary containing an existing entry.
            new_entry: Dictionary containing values to replace old_entry with.
        '''
        iid = self.__ui.get_iid()
        if iid:
            old_entry = self.__storage.get_entry(iid)
            new_entry = self.__ui.show_entry_dialog(old_values=old_entry)
            if new_entry:
                self.__storage.edit_entry(iid, new_entry)
                self.__populate_table()


    def get_entry(self, iid: str):
        '''Tell storage to fetch an entry with the matching ID.

        Params
            iid: ID of the entry to look for.
        '''
        try:
            return self.__storage.get_entry(iid)
        except KeyError:
            self.__ui.show_error('Internal error: ID {} was not found!'.format(iid))


    def save(self):
        '''Tell Storage to save the database to disk.'''
        try:
            self.__storage.save()
            self.__ui.show_info('Save successful.')
        except:
            self.__ui.show_error('Error while saving database!')


    def load(self, ask_passwd=True):
        '''Tell Storage to load database from disk.

        Params
            ask_passwd: if True, ask the user for their master password.
        '''
        filename = self.__ui.show_load_dialog()
        if filename:
            if ask_passwd:
                if not self.__get_password('Enter your master password.'):
                    return
            self.__storage.filename = filename
            try:
                self.__storage.load()
                self.__populate_table()
            except InvalidFileFormat as e:
                self.__ui.show_error(str(e))
            except FileNotFoundError as e:
                self.__ui.show_error(str(e))
            except ValueError as e:
                self.__ui.show_error(str(e))


    def new_database(self):
        '''Ask for user's password and tell Storage to create a new database.

        Params
            filename: str object containing the database file name.
        '''
        filename = self.__ui.show_save_dialog()
        if filename:
            password_set = self.__get_password(
                'Enter your master password.\nDo not forget this!'
            )
            if password_set:
                self.__storage.filename = filename
                self.save()
                self.__populate_table()


    def __get_password(self, message: str):
        '''Display a password dialog to get user's master password.

        Returns
            True if successful, False otherwise.
        '''
        passwd = self.__ui.show_password_dialog(message)
        if passwd == None:
            return False
        self.__storage.set_password(passwd)
        return True


    def __populate_table(self):
        '''Tell UI to populate its table view with the database.'''
        db = self.__storage.db
        self.__ui.display_tree_page(db)
