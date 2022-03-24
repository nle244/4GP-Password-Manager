import pytest 
from tkinter.ttk import Frame

from pm.controller import Controller
from pm import exceptions 

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from unittest.mock import Mock


@pytest.fixture
def mvc(mainwindow, storage):
    ctrl = Controller(mainwindow, storage)
    return storage, mainwindow, ctrl


class Test_Controller_save:
    def test_save_success(self, mainwindow, storage):
        controller = Controller(mainwindow, storage)

        # Controller.save() should call the following:
        #   - Storage.save() to save the file
        #   - MainWindow.show_info() to show success dialog.
        controller.save()
        storage.save.assert_called_once()
        mainwindow.show_info.assert_called_once()
    

    def test_save_fail(self, mainwindow, storage):
        controller = Controller(mainwindow, storage)
        storage.save.side_effect = Exception

        # Controller.save() failure process:
        #   - Storage.save() call throws an exception 
        #   - catch it, and call MainWindow.show_error()
        controller.save()
        storage.save.assert_called_once()
        mainwindow.show_error.assert_called_once()


class Test_Controller_load:
    def test_load_success(self, mainwindow, storage):
        controller = Controller(mainwindow, storage)

        # Controller.load() success process:
        #   - Storage.load() to load the file
        #   - MainWindow.create_db_table() to render the TreeView
        controller.load() 
        storage.load.assert_called_once()
        mainwindow.display_tree_page.assert_called_once()


    def test_load_fail_InvalidFileFormat(self, mvc):
        '''Check if load() properly handles InvalidFileFormat exception'''
        storage, mainwindow, controller = mvc
        
        storage.load.side_effect = exceptions.InvalidFileFormat
        controller.load()
        storage.load.assert_called_once()
        mainwindow.show_error.assert_called_once()
        

    def test_load_fail_FileNotFoundError(self, mvc):
        '''Check if load() properly handles FileNotFoundError exception'''
        storage, mainwindow, controller = mvc
        
        storage.load.side_effect = FileNotFoundError
        controller.load()
        storage.load.assert_called_once()
        mainwindow.show_error.assert_called_once()
