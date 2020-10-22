#!/usr/bin/env python3

''' Interface Dialog '''

from tkinter import (Toplevel)
from tkinter.ttk import (Style, Frame, Label, PanedWindow, Button, Combobox, Entry, Separator)
from tkinter.constants import LEFT, SEL, INSERT, DISABLED, NORMAL, END, CENTER, YES, ACTIVE, SUNKEN, RIGHT
from tkinter.messagebox import showerror

from interface import (loadIcon, IIVLXICO, __version__)
from interface.setexecutiondelay import SetExecutionDelay
from interface.setmaximumcellvalue import SetMaximumCellValue
        
class About(Toplevel):
    ''' The About dialog
    Shows information about this application
    '''
    WINDOW_WIDTH = 350
    WINDOW_HEIGHT = 120
    WINDOW_WIDTH_MIN = 350
    WINDOW_HEIGHT_MIN = 100
    WINDOW_WIDTH_OFFSET = 40
    WINDOW_HEIGHT_OFFSET = 20
    WINDOW_TITLE = "Brainfsck - About"
    def __init__(self, master, **kw):
        Toplevel.__init__(self, master, **kw)
        self.style = Style()
        self.withdraw()
        x = self.master.winfo_rootx() + self.WINDOW_WIDTH_OFFSET
        y = self.master.winfo_rooty() + self.WINDOW_HEIGHT_OFFSET
        loadIcon(self.tk, self, IIVLXICO)
        self.title(self.WINDOW_TITLE)
        self.geometry('{0:d}x{1:d}+{2:d}+{3:d}'.format(
            self.WINDOW_WIDTH, self.WINDOW_HEIGHT, x,y))
        self.resizable(False, False)
        self.minsize(self.WINDOW_WIDTH_MIN, self.WINDOW_HEIGHT_MIN)
        #grid configure
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)
        # grab the current window     
        #self.wait_visibility()
        self.transient(self.master)
        self.focus_set()
        self.grab_set()
        self.deiconify()   
        # draw this window
        self.configureStyles()
        self.draw()
        # wait for the window to close and return to master
        self.wait_window()
        
    def configureStyles(self):
        self.style.configure('About.TButton', font='Segoe 8', anchor='center', height=0, width=10, padding=2)
        self.style.configure('About.TLabel', font='Segoe 10')
        self.style.configure('AboutBold.TLabel', font='Segoe 14 bold', anchor='center')
        self.style.configure('AboutBoldMed.TLabel', font='Segoe 11 bold', anchor='center')

    def draw(self):
        ''' Draw the About window '''
        
        
        
        self.title_label = Label(self,
                                 text = "Brainfsck",
                                 justify=CENTER,
                                 style=  'AboutBold.TLabel')
        self.title_label.grid(row=0, column=0, columnspan=2, sticky='news')
        
        
        self.title_label_sub = Label(self,
                                     text = "Brainfsck Interpreter",
                                     style = "AboutBoldMed.TLabel")
        self.title_label_sub.grid(row=1, column=0, columnspan=2, sticky='news')

        self.about_label = Label(self,
                                 text = "Created by iivlx - iivlx@iivlx.com",
                                 style = "About.TLabel")
        self.about_label.grid(row=2, column=0, columnspan=2, padx=10, sticky='news')
        
        self.version_label = Label(self,
                                   text = "Version: {0:s}".format('.'.join(str(v) for v in __version__)),
                                   style = "About.TLabel")
        self.version_label.grid(row=3, column=0, columnspan=2, padx=10, sticky='news')

        self.close_button = Button(self,
                                   text = "Close",
                                   style = "About.TButton",
                                   command = lambda: self.close())
        self.close_button.grid(row=4, column=1, padx=4, pady=4, sticky='nes')
        self.close_button.focus_set()

        
    def close(self):
        ''' Close this dialog and return to parent window '''
        self.master.focus_set()
        self.destroy()