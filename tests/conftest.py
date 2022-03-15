import pytest
from unittest.mock import Mock

from pm.storage import Storage
from pm.controller import Controller
from pm.ui import MainWindow

@pytest.fixture
def mainwindow():
    return Mock(spec=MainWindow)


@pytest.fixture
def storage():
    return Mock(spec=Storage)


@pytest.fixture
def controller():
    return Mock(spec=Controller)


@pytest.fixture
def filename():
    return 'test.csv'
