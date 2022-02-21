import tkinter as tk 

proj_name = 'Password Manager'

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__(className=proj_name)

        self.title(proj_name) 
        self.geometry("800x600")
