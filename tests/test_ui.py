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
