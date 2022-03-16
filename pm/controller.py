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


    def add_entry(self, entry: dict):
        '''Tell Storage to add a new entry to the database in memory.
        Tell MainWindow to render an error message if column values are wrong.
        Params
            entry: Dictionary containing a new entry.
        '''
        try:
            self.__storage.add_entry(entry)
        except InvalidColumns as e:
            self.__ui.show_error(str(e))


    def edit_entry(self, old_entry: dict, new_entry: dict):
        '''Tell Storage to edit an existing entry.
        Params
            old_entry: Dictionary containing an existing entry.
            new_entry: Dictionary containing values to replace old_entry with.
        '''
        self.__storage.edit_entry(old_entry, new_entry)


    def save(self):
        '''Tell Storage to save the database to disk.'''
        try:
            self.__storage.save()
            self.__ui.show_info('Save successful.')
        except:
            self.__ui.show_error('Error while saving database!')


    def load(self):
        '''Tell Storage to load database from disk.'''
        try:
            self.__storage.load()
            self.__populate_table()
        except InvalidFileFormat as e:
            self.__ui.show_error(str(e))
        except FileNotFoundError as e:
            self.__ui.show_error(str(e))


    def __populate_table(self):
        '''Tell UI to populate its table view with the database.'''
        db = self.__storage.db
        self.__ui.create_db_table(db)


    def set_filename(self, fname):
        '''Tell Storage to set the filename.

        Params
            fname: Filename.
        '''
        self.__storage.filename = fname
