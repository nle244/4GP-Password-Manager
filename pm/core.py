import tkinter as tk
import platform

from pm.ui import MainWindow
from pm.controller import Controller
from pm.storage import Storage


PROJ_NAME = 'Quick Key'

class QuickKey(tk.Tk):
    '''Encapsulates the main UI'''

    def __init__(self):
        super().__init__()

        self.__setup_ui()
        self.__setup_components()



    def __setup_ui(self):
        print('loading ui')
        self.title(PROJ_NAME)

        self.resizable(0,0)

        if platform.system() == 'Windows':
            self.attributes('-toolwindow', True)

        self.columnconfigure(0, weight=1)


    def __setup_components(self):
        # init main window
        main_window = MainWindow(self)
        main_window.grid(row=0, column=0)
        main_window['padding'] = (10, 10, 10, 10)

        # init storage
        storage = Storage()

        # init controller and connect it to ui and storage
        controller = Controller(main_window, storage)

        # connect ui to controller
        main_window.ctrl = controller
