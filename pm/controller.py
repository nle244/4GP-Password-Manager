from pm.ui import MainWindow
from pm.storage import Storage
from pm.exceptions import (
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
