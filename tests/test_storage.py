import pytest
from unittest.mock import patch

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
    temp_db = [
        {header: '{} test value {}'.format(header, i) for header in HEADER}
        for i in range(5)
    ]

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

        # set passwd and initialize
        storage.filename = tmp_path / filename
        storage.set_password('very secure')
        storage.save()
        storage.load()

        # add test entries
        for entry in self.temp_db:
            storage.add_entry(entry)

        # write it to disk
        storage.save()

        # load it
        storage.load()

        # check it
        for entry in storage.db:
            assert storage.db[entry] in self.temp_db


class Test_Storage_add_entry:
    correct = {header: '{} test value'.format(header) for header in HEADER}
    incorrect = {header + '_wrong': '{} test value'.format(header) for header in HEADER}

    def test_add_entry_fail(self, mvc, tmp_path, filename):
        storage, mainwindow, controller = mvc

        # set passwd and initialize
        storage.filename = tmp_path / filename
        storage.set_password('extremely secure')
        storage.save()
        storage.load()

        # this should be caught
        with pytest.raises(exceptions.InvalidColumns):
            storage.add_entry(self.incorrect)


    def test_add_entry_success(self, mvc, tmp_path, filename):
        storage, mainwindow, controller = mvc

        # set passwd and initialize
        storage.filename = tmp_path / filename
        storage.set_password('cheese grater')
        storage.save()
        storage.load()

        # shouldn't raise any exceptions
        storage.add_entry(self.correct)
        for key in storage.db:
            assert storage.db[key] == self.correct

class Test_Storage_delete_entry:
    new = {header: '{} test value'.format(header) for header in HEADER}

    def test_delete_entry_success(self,mvc, tmp_path, filename):
        storage, mainwindow, controller = mvc

        # set passwd and initialize
        storage.filename = tmp_path / filename
        storage.set_password('anime waifu')
        storage.save()
        storage.load()

        storage.add_entry(self.new)                         #add an entry
        storage.delete_entry(list(storage.db.keys())[0])    #delete the entry
        assert len(storage.db) == 0                         #dict should be empty




