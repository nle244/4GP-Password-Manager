import os
import csv

from pm.exceptions import (
    InvalidFileFormat,
)


HEADER = ['Title', 'Username', 'Password', 'URL', 'Last_Modified']

class Storage:
    '''Represents the database file and provides function endpoints for interacting with it.'''

    def __init__(self, filename=None):
        self.filename = filename
        self.__db = []


    @property
    def filename(self):
        '''Name of the database file.'''
        return self.__filename


    @filename.setter
    def filename(self, filename):
        '''Name of the database file.'''
        self.__filename = filename


    @property
    def db(self):
        '''Dictionary containing all paswords.'''
        return self.__db


    def load(self):
        '''Load the password file.

        Raises
            FileNotFoundError if file is not found.
            InvalidFileFormat if the header values are invalid.
        '''
        if self.filename == None:
            raise FileNotFoundError('Filename not set.')

        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            if reader.fieldnames != HEADER:
                raise InvalidFileFormat('Unexpected database header values.')

            for row in reader:
                self.db.append(dict())
                for header in HEADER:
                    self.db[-1][header] = row[header]


    def save(self):
        '''Save the database to disk. Creates a new file if it doesn't exist already.'''
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=HEADER)

            writer.writeheader()
            for row in self.db:
                writer.writerow(row)
