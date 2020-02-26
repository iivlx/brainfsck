from tkinter import (Toplevel)
from tkinter.ttk import (Style, Label, Button, Entry)
from tkinter.messagebox import showerror
from interface import (loadIcon, IIVLXICO)

class SetMaximumCellValue(Toplevel):
    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 80
    WINDOW_RESIZABLE = (False, False)
    WINDOW_TITLE = "Set maximum cell value"
    def __init__(self, master, **kw):
        Toplevel.__init__(self, master, **kw)
        self.style = Style()
        self.withdraw()
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty()
        loadIcon(self.tk, self, IIVLXICO)
        self.title(self.WINDOW_TITLE)
        self.resizable(*self.WINDOW_RESIZABLE)
        self.geometry('{0:d}x{1:d}+{2:d}+{3:d}'.format(
                      self.WINDOW_WIDTH, self.WINDOW_HEIGHT, x,y))
        # grid configure
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        # set window as transient and display
        self.transient(self.master)
        self.focus_set()
        self.grab_set()
        self.deiconify()   
        # draw the window\
        self.configureStyles()
        self.draw()
        # wait for the window to close and return to master
        self.wait_window()
    def configureStyles(self):
        self.style.configure('SetExecutionDelay.TButton', font='Segoe 8', height=3, width=10, anchor='center', padding=2)
        self.style.configure('SetExecutionDelay.TLabel', font='Segoe 8')
        self.style.configure('SetExecutionDelay.TEntry', font='Segoe 10')
    
    def draw(self):
        ''' draw the SetMaximumCellValue window widgets '''
        self.input_label = Label(self, text="Maximum Cell Value:", style='SetExecutionDelay.TLabel')
        self.input_label.grid(row=0, column=0, columnspan=3, padx=5, sticky='nws')
        self.input_entry = Entry(self, style='SetExecutionDelay.TEntry')
        self.input_entry.grid(row=1, column=0, columnspan=3, padx=5, sticky='news') 
        self.cancel_button = Button(self, text="Cancel", style='SetExecutionDelay.TButton', command=self.close)
        self.cancel_button.grid(row=3,column=1, sticky='news', pady=5, padx=5)
        self.accept_button = Button(self, text="Accept", style='SetExecutionDelay.TButton', command=self.accept)
        self.accept_button.grid(row=3,column=2, sticky='news', pady=5, padx=5)
        
    def accept(self):
        '''Verify and change the maximum cell value'''
        value = self.input_entry.get()
        if(value.isnumeric()):
            value = int(value)
            if value > 0:
                self.master.setMaximumCellValue(value)
                self.close()
                return
        showerror("Invalid entry", "Please enter an integer value greater than 0.")
            
        
    def close(self):
        ''' Close this dialog and return to parent window '''
        self.master.focus_set()
        self.destroy()
