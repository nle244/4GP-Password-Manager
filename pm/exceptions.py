class QuickKeyException(Exception):
    '''Base exception class for this project.'''

class InvalidFileFormat(QuickKeyException):
    '''
    Raise this if the password database file is in invalid format.
    '''

class InvalidColumns(QuickKeyException):
    '''
    Raise this if an entry's columns (Title, Username, ...) are invalid.
    '''

class InvalidConfig(QuickKeyException):
    '''
    Raise this if the configuration is invalid.
    '''
