#!/usr/bin/env python3
''' brainfsck
Brainfsck interpreter
 
Written in Python3 with the tkinter library
'''

__author__ = "iivlx - iivlx@iivlx.com"
__date__ = (22,10,2019) #d,Wm,y
__version__ = (0,0,1) #0.0.1

from tkinter import Tk
from interface import Brainfsck
from engine import BrainfsckEngine

def main():
    ''' Main entry point of application
    '''
    root = Tk()
    root.withdraw()
    brainfsck = Brainfsck(root)
    engine = BrainfsckEngine()
    brainfsck.loadEngine(engine)
    
    root.deiconify()
    brainfsck.master.mainloop()

if __name__ == "__main__":
    main()
    