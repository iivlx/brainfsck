#!/usr/bin/env python3

''' Main Window '''

import time
from math import floor
from tkinter import Tk, ttk, TclError, StringVar
from tkinter import PhotoImage
from tkinter import (Toplevel, Menu, Text)
from tkinter import filedialog
from tkinter.ttk import (Style, Frame, Label, PanedWindow, Button, Combobox, Entry, Separator)
from tkinter.constants import LEFT, SEL, INSERT, DISABLED, NORMAL, END, CENTER, YES, ACTIVE, SUNKEN, RIGHT, CURRENT

from interface import (__version__, loadIcon, IIVLXICO, About, MemoryView, SetExecutionDelay, SetMaximumCellValue)

class Brainfsck(Frame):
    ''' Main window of the application    
    '''
    WINDOW_TITLE = "Brainfsck - iivlxsoft"
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 700
    WINDOW_WIDTH_MIN = 500
    WINDOW_HEIGHT_MIN = 250
    WINDOW_WIDTH_OFFSET = 100
    WINDOW_HEIGHT_OFFSET = 100
    WINDOW_Y_MIN = 50
    WINDOW_RESIZABLE = (True, True)
    
    engine = None
    execution_delay = 1
    allow_illegal_characters = True
    input_buffer = []
    output_buffer = []
    _reset_modifed = False #sponge
    execution_time_start = 0
    execution_time_end = 0
    execution_time_total = 0
    breakpoints = []
    
    def __init__(self, master, **kw):
        Frame.__init__(self, master, **kw)
        self.style = Style()
        self.configure()
        
        loadIcon(self.master, self.master, IIVLXICO)
        self.master.title(self.WINDOW_TITLE)
        self.master.resizable(*self.WINDOW_RESIZABLE)
        x = self.master.winfo_pointerx() - self.WINDOW_WIDTH_OFFSET
        y = self.master.winfo_pointery() - self.WINDOW_HEIGHT_OFFSET
        y = y if y > self.WINDOW_Y_MIN else self.WINDOW_Y_MIN  
        self.master.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}')
        self.master.minsize(self.WINDOW_WIDTH_MIN, self.WINDOW_HEIGHT_MIN)
        # configure master grid
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        # place the window
        self.grid(row=0, column=0, sticky='news')
        #configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=2)
        # subwindows
        self.memoryview = None
        # draw the window
        self.createMenubar()
        self.createContextMenu()
        self.draw()
        self.setBinds()
        
    def setBinds(self):
        self.codeInput.bind("<Button-3>", self.showContextMenu)
        #self.textInput.bind("<<Modified>>", self.handleInput)
        self.textInput.bind("<Key>", self.handleKey)
    
    def draw(self):
        self.drawCode()
        self.drawIO()
        self.drawControls()
        self.drawStatusBar()
        
    def drawCode(self):
        ''' code'''
        self.codeInput = Text(self)
        self.codeInput.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='news')
    
    
    def drawIO(self):
        self.textOutput = Text(self)
        self.textOutput.configure(state=DISABLED)
        self.textOutput.grid(row=0, column=2, columnspan=2, sticky='news')
        self.textInput = Text(self)
        self.textInput.grid(row=1, column=2, columnspan=2, sticky='news')
        self.textInputModified = False
        self.textInputIndex = 0
        self.textInput.config(state=DISABLED)
    
    def drawControls(self):
        ''' main controls'''
        startStopButton = Button(self, text="Run")
        startStopButton.config(command = lambda : self.startStop())
        startStopButton.grid(row=2, column=0)
        stepButton = Button(self, text="Step", command = lambda : self.step())
        stepButton.grid(row=2, column=1)
        resetButton = Button(self, text="Reset/Load", command = lambda : self.reset())
        resetButton.grid(row=2, column=2)
        quitButton = Button(self, text="Quit")
        quitButton.config(command = lambda : self.close())
        quitButton.grid(row=2, column=3)
        
    def drawStatusBar(self):
        self.statusBar = Label(self, text='Instruction Pointer: 0, Memory Pointer: 0, Memory Value: 0')
        self.statusBar.grid(row=3,column=0, columnspan=4, sticky='ews')
        self.statusBar.config(relief=SUNKEN)
    
    def updateStatusBar(self):
        ip = self.engine.instruction_pointer
        mp = self.engine.memory_pointer
        #print(mp) #sponge
        value = self.engine.memory[mp]
        er = self.engine.running
        p = '' if self.running else ' (paused)'
        status_string = 'Running: %s%s, Instruction Pointer: %d, Memory Pointer: %d, Memory Value: %d' % (er, p, ip, mp, value)
        if self.execution_time_total:
            status_string += ', Execution Time: %f' % self.execution_time_total
        self.statusBar.config(text = status_string)
    
    def createMenubar(self):
        ''' Create and add the menubar
        The menubar consists of the following submenus:
        File
        Edit
        View
        About
        '''
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        # add submenus
        self.menubar.add_cascade(label='File', menu=self.createMenubarFile())
        self.menubar.add_cascade(label='Edit', menu=self.createMenubarEdit())
        self.menubar.add_cascade(label='View', menu=self.createMenubarView())
        self.menubar.add_cascade(label='Help', menu=self.createMenubarHelp())
        
    def createMenubarFile(self):
        ''' Create the File submenu '''
        self.menubar_file = Menu(self.menubar, tearoff=0)
        self.menubar_file.add_command(label='Load')
        self.menubar_file.add_command(label='Save')
        self.menubar_file.add_separator()
        self.menubar_file.add_command(label='Exit', command=self.quit)
        return self.menubar_file
    
    
    def createMenubarEdit(self):
        ''' Create the Edit submenu '''
        self.menubar_edit = Menu(self.menubar, tearoff=0)
        self.menubar_edit.add_command(label='Set exectuion delay', command=self.showSetExecutionDelay)
        self.menubar_edit.add_separator()
        self.menubar_edit.add_command(label='Remove non bf characters', command=self.stripIllegalCharacters)
        self.menubar_edit.add_command(label='Remove spaces', command=self.stripSpaces)
        self.menubar_edit.add_command(label='Remove newlines', command=self.stripNewlines)
        self.menubar_edit.add_separator()
        self.menubar_edit.add_command(label='Delete all breakpoints', command=self.clearAllBreakpoints)
        self.menubar_edit.add_separator()
        self.menubar_edit.add_command(label='Edit memory cell size')
        self.menubar_edit.add_command(label='Edit memory size')
        self.menubar_edit.add_command(label='Edit maximum memory cell value', command=self.showSetMaximumCellValue)
        return self.menubar_edit
    
    def createMenubarView(self):
        ''' Create the View submen '''
        self.menubar_view = Menu(self.menubar, tearoff=0)
        self.menubar_view.add_command(label='Memory Block', command=self.showMemoryBlock)
        self.menubar_view.add_command(label='Memory Linear', command=self.showMemoryLinear)
        return self.menubar_view                

    def createMenubarHelp(self):
        ''' Create the Help submenu '''
        self.menubar_about = Menu(self.menubar, tearoff=0)
        self.menubar_about.add_command(label='About', command=self.showAbout)
        return self.menubar_about
        
    def createContextMenu(self):
        ''' Right click context menu '''
        self.contextMenu = Menu(self, tearoff=0)
        self.contextMenu.add_command(label='Set Breakpoint', command=self.setBreakpoint)
        self.contextMenu.add_command(label='Clear Breakpoint', command=self.clearBreakpoint)
        return self.contextMenu
    
    def showContextMenu(self, event):
        try:
            self.contextMenu.tk_popup(event.x_root+50, event.y_root+10, 0)
        finally:
            self.contextMenu.grab_release()
        
    def showAbout(self):
        ''' Show the about dialog '''
        About(self)
        
    def showMemoryBlock(self):
        ''' Show memory viewer '''
        self.memoryview = MemoryView(self)
        
    def showMemoryLinear(self):
        ''' Show memory viewer '''
        self.memoryview = MemoryView(self)
        
    def stripCharacters(self, characters):
        ''' remove characters from code input '''
        # remember current cursor position
        cursor = self.codeInput.index(CURRENT)
        # strip the code of non legal brainfsck characters
        code = self.codeInput.get('1.0', END)        
        code = code.translate({ord(c): None for c in characters})
        # remove old code and insert stripped code and reset cursor
        self.codeInput.delete('1.0', END)
        self.codeInput.insert('1.0', code)
        self.codeInput.mark_set('insert', cursor)
        
    def stripIllegalCharacters(self):
        ''' Remove all non brainfsck characters from the code input'''
        # remember current cursor position
        cursor = self.codeInput.index(CURRENT)
        # strip the code of non legal brainfsck characters
        code = self.codeInput.get('1.0', END)        
        code = ''.join(filter(lambda x: x in ['\n', ' ', '.', ',', '+', '-', '>', '<', '[', ']'], code))
        # remove old code and insert stripped code and reset cursor
        self.codeInput.delete('1.0', END)
        self.codeInput.insert('1.0', code)
        self.codeInput.mark_set('insert', cursor)
    
    def stripSpaces(self):
        self.stripCharacters(' ')
        
    def stripNewlines(self):
        self.stripCharacters('\n')
        
        
    def checkBreakpoint(self):
        ''' Check to see if we hit a breakpoint'''
        if self.engine.instruction_pointer in self.breakpoints:
            self.pause()
    
    def setBreakpoint(self):
        ''' set a breakpoint at the current selection'''
        # check to see if something is selected
        if self.codeInput.tag_ranges('sel'):
            # add the selection to the breakpoint list
            
            for i in range(self.codeInput.count('sel.first', 'sel.last')[0]):
                count = self.codeInput.count('1.0', 'sel.first')
                if count is None: count = [0]
                bp = count[0]+i
                if bp not in self.breakpoints:
                    self.breakpoints.append(bp)
            # highlight breakpoints
            self.codeInput.tag_add('breakpoint', 'sel.first', 'sel.last')
            self.codeInput.tag_config('breakpoint', background='yellow', foreground='black')
            self.codeInput.tag_raise('sel')
        
    def clearBreakpoint(self):
        ''' clear the breakpoint at the cursor'''
        # check to see if anything is selected
        if self.codeInput.tag_ranges('sel'):
            # remove selection from breakpoint list
            for i in range(self.codeInput.count('sel.first', 'sel.last')[0]):
                count = self.codeInput.count('1.0', 'sel.first')
                if count is None: count = [0]
                bp = count[0]+i
                if bp in self.breakpoints:
                    self.breakpoints.remove(bp)
            
            # remove highlight
            self.codeInput.tag_remove('breakpoint', 'sel.first','sel.last')
            
    def clearAllBreakpoints(self):
        for tag in self.codeInput.tag_names():
            if tag == 'breakpoint':
                self.codeInput.tag_delete(tag)
        self.breakpoints = []
    
    def showSetExecutionDelay(self):
        ''' Open the SetExecutionDelay dialog and use the value returned to set
        the execution delay'''
        SetExecutionDelay(self)
    
    def showSetMaximumCellValue(self):
        ''' open the SetMaximumCellValue dialog and use the value returend to set the execution delay '''
        SetMaximumCellValue(self)
        
    def setMaximumCellValue(self, value):
        self.engine.memorymaxvalue = value
        
    def getCode(self):
        if self.codeInput:
            return self.codeInput.get('1.0', END)
        else:
            return ""
        
    def startStop(self):
        ''' Start or start the engine,
        If we stopped in the middle of the program we should just begin where we left off
        Otherwise if run_complete is true we want to restart from the beginning.'''
        if not self.engine.running:
            self.reset()
            self.engine.running = True
            self.updateStatusBar()
        
        if not self.execution_time_start:
            self.execution_time_start = time.time()
        
        
        if self.running:
            self.pause()
        else:
            self.running = True
            self.run()
    
    def pause(self):
        ''' Pause the execution '''
        self.running = False
        self.updateStatusBar()
        

    def run(self):
        ''' Step through the code one instruction at a time after a timeout until the program finishes.'''
        self.getOutput()
        self.updateStatusBar()
        if self.engine.running == True:
            self.tagCurrentInstruction()
            self.checkBreakpoint()
            self.engine.step()
            if self.memoryview:
                self.memoryview.refreshMemory()
            if self.running:
                    self.master.after(self.execution_delay,self.run)
                    #self.master.after_idle(self.run)
        else:
            self.execution_time_total = time.time() - self.execution_time_start
            self.updateStatusBar()
            return
                
    def step(self):
        self.getOutput()
        if self.engine.running == True:
            self.tagCurrentInstruction()
            self.engine.step()
            if self.memoryview:
                self.memoryview.refreshMemory()
            self.updateStatusBar()
        else:
            self.reset()
            self.engine.running = True
            self.updateStatusBar()
        
        
        
    def clearText(self):
        self.textOutput.config(state=NORMAL)
        self.textOutput.delete('1.0', END)
        self.textOutput.config(state=DISABLED)
        self.textInput.config(state=NORMAL)
        self.textInput.delete('1.0', END)
        self.textInput.config(state=DISABLED)
        #self.textInputIndex = 0
        
        
    def tagCurrentInstruction(self):
        for tag in self.codeInput.tag_names():
            if tag == 'current':
                self.codeInput.tag_delete(tag)
                
        current = self.engine.instruction_pointer
        s = self.codeInput.get('1.0', END)[0]
        if s.isspace():
            return # the code contains only whitespace
        self.codeInput.tag_add('current', '1.0+%dc' % current)
        self.codeInput.tag_config('current', background='red')
            
    def handleKey(self, event):
        ''' Handle a keypress on the text input window, we want to copy this character
        to the input buffer, and also display it on the text input.'''
        #print(event)
        if not event.char:
            return # special character we can ignore this
        if event.char == '\r':
            event.char = '\n'
        
        
        self.textInput.config(state=NORMAL)
        self.textInput.insert(END, event.char)
        self.textInput.config(state=DISABLED)
        
        self.input_buffer.append(event.char)
        
        
    def getOutput(self):
        if self.output_buffer:
            self.textOutput.config(state=NORMAL)
            self.textOutput.insert(END, self.output_buffer.pop(0))
            self.textOutput.config(state=DISABLED)
        
    def loadEngine(self, engine):
        self.engine = engine
        self.code = " "
        self.reset()
        
    def reset(self):
        self.clearText()
        self.engine.reset()
        self.engine.code = self.getCode()
        self.engine.getBrackets()
        self.engine.running = False
        self.running = False
        self.clearText()
        self.input_buffer = []
        self.output_buffer = []
        self.engine.output_buffer = self.output_buffer
        self.engine.input_buffer = self.input_buffer
        self.tagCurrentInstruction()
        self.execution_time_start = 0
        self.execution_time_end = 0
        self.execution_time_total = 0
            #self.engine.run(input = self.input_buffer, output = self.output_buffer)
        self.updateStatusBar()
        
    def close(self):
        ''' Close this window '''
        self.quit()






