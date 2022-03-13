class QuickKeyException(Exception):
    '''Base exception class for this project.'''

class InvalidFileFormat(QuickKeyException):
    '''
    Raise this if the password database file is in invalid format.
    '''

class InvalidConfig(QuickKeyException):
    '''
    Raise this if the configuration is invalid.
    '''
