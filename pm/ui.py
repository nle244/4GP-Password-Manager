import tkinter as tk 
from tkinter import ttk
from tkinter.filedialog import asksaveasfile


proj_name = 'Password Manager'

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__(className=proj_name)

        self.title(proj_name) 
        self.geometry("600x300")
        self.resizable(0,0)
        self.attributes('-toolwindow', True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()
   
#Initial layout just to get started; may need to organize into frames later on
    def __create_widgets(self):
        label1 = tk.Label(self, font=("Arial",25), text="Welcome")
        label1.place(relx=.5, y= 50, anchor=tk.CENTER)

        homebutton1 = tk.Button(self, text="New Database", command = newbuttonclick)
        homebutton1.place(x=150, y= 200)

        homebutton2 = tk.Button(self, text="Open Database")
        homebutton2.place(x =350, y=200)

#UI Functions
def newbuttonclick():
    f = asksaveasfile(initialfile = 'newDatabase.txt', 
        defaultextension = '.txt', filetypes = [("All Files","*.*")])