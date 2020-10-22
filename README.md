# iivlx.brainfsck

Interactive brainfsck interpreter with several features.

---

## Features

- Interactive debugging of brainfsck code allowing you to pause the program at any point and step through commands.
- Breakpoints that will pause the operation of the program at a set point, the program can be resumed normally afterwards.
- Status bar showing status of the program, the current instruction, and the current memory cell and value.
- Dynamic view of memory cells with real time changes.
- Allows arbitrary size of total memory and of individual memory cells ( default 64 kilobytes of memory with each memory cell 1 byte )

## Interface and Usage

The interface consists of 3 main panels:
- The left panel contains the brainfsck code.
- The right panels contain input and output, output being on the top, and input on the bottom.

After brainfsck code has been entered, the *Reset/Load* button will load the code.
The *Run* button will allow the code to execute normally, *Step* will execute a single instruction at a time.
If the brainfsck code requires user input you can click on the input panel to capture keyboard input.
The memory viewer can be accessed by using the menubar under *View*.