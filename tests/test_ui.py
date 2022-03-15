import pytest
import os
from unittest.mock import patch
from tkinter.ttk import Frame

from pm.ui import MainWindow


# workaround for github actions
try:
    disp = os.environ['DISPLAY']
except KeyError:
    os.system('Xvfb :1 -screen 0 1600x1200x16 &')
    os.environ['DISPLAY'] = ':1.0'


@pytest.fixture
def mvc(storage, controller):
    mainwindow = MainWindow(Frame())
    mainwindow.ctrl = controller
    return storage, mainwindow, controller


class Test_MainWindow_load_filepath:
    
    def test_load_filepath(self, mvc, filename):
        storage, mainwindow, controller = mvc 

        # Preventing filedialog.askopenfilename() from spawning a dialog
        # and force it to return 'test.csv'
        with patch('pm.ui.filedialog') as dialog:
            dialog.askopenfilename.return_value = filename
            mainwindow.load_filepath()

        controller.set_filename.assert_called_once_with(filename)
        controller.load.assert_called_once()


