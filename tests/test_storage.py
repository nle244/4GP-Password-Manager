import pytest
import csv

from pm.storage import Storage, HEADER
from pm import exceptions

@pytest.fixture
def mvc(mainwindow, controller):
    storage = Storage()
    return storage, mainwindow, controller



class Test_Storage_filename:
    def test_filename(self, mvc, filename):
        storage, mainwindow, controller = mvc 

        storage.filename = filename
        assert storage.filename == filename


class Test_Storage_load:

    def test_load_fail(self, mvc, tmp_path, filename):
        '''Check if load() raises all the proper exceptions'''
        storage, mainwindow, controller = mvc 

        storage.filename = None
        with pytest.raises(FileNotFoundError):
            storage.load()
        
        storage.filename = tmp_path / filename
        with pytest.raises(FileNotFoundError):
            storage.load()


    def test_load_success(self, mvc, tmp_path, filename):
        storage, mainwindow, controller = mvc 

        # create and write a temporary database file
        db_path = tmp_path / filename
        db = []
        for i in range(10):
            db.append(dict())
            for header in HEADER:
                db[-1][header] = '{} test value'.format(header)
        with open(db_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=HEADER)
            writer.writeheader()
            for row in db:
                writer.writerow(row)
        
        storage.filename = db_path
        storage.load()
        assert storage.db == db


class Test_Storage_add_entry:
    correct = {header: '{} test value'.format(header) for header in HEADER}
    incorrect = {header + '_wrong': '{} test value'.format(header) for header in HEADER}

    def test_add_entry_fail(self, mvc):
        storage, mainwindow, controller = mvc

        with pytest.raises(exceptions.InvalidColumns):
            storage.add_entry(self.incorrect)


    def test_add_entry_success(self, mvc):
        storage, mainwindow, controller = mvc

        storage.add_entry(self.correct)
        assert storage.db[-1] == self.correct
