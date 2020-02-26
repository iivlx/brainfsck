from tkinter import (Toplevel, Text)
from tkinter.ttk import (Style, Frame, Label, PanedWindow, Button, Combobox, Entry, Separator)
from tkinter.constants import LEFT, SEL, INSERT, DISABLED, NORMAL, END, CENTER, YES, ACTIVE, SUNKEN, RIGHT

from interface import (loadIcon, IIVLXICO, __version__)

from interface.setmaximumcellvalue import SetMaximumCellValue

     
class MemoryView(Toplevel):
    '''
    '''
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 400
    WINDOW_WIDTH_MIN = 300
    WINDOW_HEIGHT_MIN = 200
    WINDOW_WIDTH_OFFSET = 40
    WINDOW_HEIGHT_OFFSET = 20
    WINDOW_TITLE = "Brainfsck - Memory View"
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
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        #self.wait_visibility()
        #self.transient(self.master)
        #self.focus_set()
        #self.grab_set()
        self.deiconify()
        # configure memory
        self.engine = self.master.engine
        # draw this window
        self.configureStyles()
        self.draw()
        # wait for the window to close and return to master
        #self.wait_window()
        
    def configureStyles(self):
        self.style.configure('Memory.TButton', font='Segoe 8', anchor='center', height=0, width=10, padding=2)
        self.style.configure('Memory.TLabel', font='Segoe 10')
        self.style.configure('MemoryBold.TLabel', font='Segoe 14 bold', anchor='center')
        self.style.configure('MemoryBoldMed.TLabel', font='Segoe 11 bold', anchor='center')

        
    def setBinds(self):
        pass
        #self.bindall("<Button-3>", self.showContextMenu)
    
    def draw(self):
        self.drawMemory()
        self.loadMemory()
        self.drawStatusBar()
        
    
    def drawStatusBar(self):
        self.statusBar = Label(self, text=f'Memory Pointer: {self.engine.memory_pointer}, Memory Value: 0')
        self.statusBar.grid(row=1,column=0, columnspan=1, sticky='ews')
        self.statusBar.config(relief=SUNKEN)
    
    def drawMemory(self):
        self.textMemory = Text(self)
        #self.textMemory.insert(END, '')
        self.textMemory.config(state=DISABLED)
        self.textMemory.grid(row=0, column=0, columnspan=1, sticky='news')
        
    def refreshMemory(self):
        self.deleteMemory()
        self.loadMemory()

    def loadMemory(self, index=0, size=80):
        ''' Display the size in bytes memory at the current index
        '''
        self.textMemory.config(state=NORMAL)
        self.deleteCurrentTag()
        for cell in range(size):
            value = format(self.engine.memory[cell], '02X')
            if index+cell == self.engine.memory_pointer:
                self.textMemory.insert(END, value, 'current') # memory is pointing here
            else:
                self.textMemory.insert(END, value)
            self.textMemory.insert(END, ' ')
        
        self.textMemory.config(state=DISABLED)
        self.textMemory.tag_config('current', background='red')
        #self.codeInput.tag_add('current', '1.0+%dc' % current)
        
    def deleteMemory(self):
        self.textMemory.config(state=NORMAL)
        self.textMemory.delete('1.0', END)
        self.textMemory.config(state=DISABLED)
               
   
   
   
    def deleteCurrentTag(self):
        for tag in self.textMemory.tag_names():
            if tag == 'current':
                self.textMemory.tag_delete(tag)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        