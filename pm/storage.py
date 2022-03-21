import os
import pickle
import gc

from pm.cryptography import Cryptography
from pm.exceptions import (
    InvalidColumns,
    InvalidFileFormat,
)


HEADER = ['Title', 'Username', 'Password', 'URL', 'Last_Modified']





class Storage:
    '''Represents the database file and provides function endpoints for interacting with it.'''

    def __init__(self, filename=None):
        self.filename = filename
        self.__plaintext_db = []            # populated only with @encryption
        self.__crypto = Cryptography()
        self.__db = b''


    def encryption(func):
        '''Decorator for functions that need a plaintext database to work, such as adding, modifying, etc.
        '''
        def decrypt_then_encrypt(self, *args, **kwargs):
            # decrypt database
            plaintext_bytes = self.__crypto.decrypt(self.__db)
            self.__plaintext_db = pickle.loads(plaintext_bytes)

            # run func
            result = func(self, *args, **kwargs)   # type: ignore

            # encrypt database
            plaintext_bytes = pickle.dumps(self.__plaintext_db)
            self.__db = self.__crypto.encrypt(plaintext_bytes)

            # destroy plaintext
            del plaintext_bytes, self.__plaintext_db
            gc.collect()

            return result
        return decrypt_then_encrypt


    @property
    def filename(self):
        '''Name of the database file.'''
        return self.__filename


    @filename.setter
    def filename(self, filename):
        '''Name of the database file.'''
        self.__filename = filename


    @property
    @encryption
    def db(self):
        '''Dictionary containing all passwords.'''
        return self.__plaintext_db


    @encryption
    def add_entry(self, entry: dict):
        '''Add a new entry to the database in memory.
        Params
            entry: Dictionary object containing a new entry.
        Raises
            InvalidColumns if the column values are wrong.
        '''
        if sorted(entry.keys()) == sorted(HEADER):
            self.__plaintext_db.append(entry)
        else:
            msg = ' '.join(entry.keys())
            raise InvalidColumns('Invalid column values: {}'.format(msg))


    @encryption
    def delete_entry(self, entry: dict):
        '''Delete an existing entry from the database in memory.
        Params
            entry: Dictionary containing the entry to delete.
        '''
        self.__plaintext_db.remove(entry)


    @encryption
    def edit_entry(self, old_entry: dict, new_entry: dict):
        '''Edit an existing entry.

        Params
            old_entry: Dictionary containing an existing entry.
            new_entry: Dictionary containing values to replace old_entry with.
        '''
        idx = self.__plaintext_db.index(old_entry)
        self.__plaintext_db[idx] = new_entry


    def load(self):
        '''Load the password file.

        Raises
            FileNotFoundError if file is not found.
            InvalidFileFormat if the header values are invalid.
        '''
        if self.filename == None:
            raise FileNotFoundError('Filename not set.')

        with open(self.filename, 'rb') as f:
            raw_bytes = f.read()

        # configure crypto object with cryptographic params from file
        offset = self.__crypto.parse_params(raw_bytes)

        # set payload portion as encrypted database
        self.__db = raw_bytes[offset:]

        # ensure that headers are intact
        self.__check_header()


    def save(self):
        '''Save the database to disk. Creates a new file if it doesn't exist already.'''
        # saving for the first time?
        if self.__db == b'':
            self.__db = self.__crypto.encrypt(pickle.dumps([]))

        # just write it as raw bytes
        with open(self.filename, 'wb') as f:
            f.write(self.__crypto.params + self.__db)


    def set_password(self, passwd):
        '''Configure Cryptography object with user's master password.

        Params
            passwd: string containing user's password.
        '''
        self.__crypto.set_password(passwd)


    @encryption
    def __check_header(self):
        if len(self.__db) > 0:
            keys = [row.keys() for row in self.__plaintext_db]
            for key in keys:
                if sorted(key) != sorted(HEADER):
                    raise InvalidFileFormat('Unexpected database header values.')
