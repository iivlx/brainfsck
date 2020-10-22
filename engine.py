#!/usr/bin/env python3

''' Brainfsck interpreter '''

MEMORYSIZE = 65536
DEFAULTCELLSIZE = 255

class BrainfsckEngine:
    ''' '''
    def __init__(self):
        self.memory = [0 for i in range(MEMORYSIZE)] # memory
        self.memorymaxvalue = DEFAULTCELLSIZE
        self.memorysize = MEMORYSIZE
        self.memory_pointer = 0 # memory pointer
        self.instruction_pointer = 0 # instruction pointer
        self.code = ""
        self.brackets = {}
        self.output_buffer = None # 
        self.input_buffer = None #
        self.running = False
    
    def reset(self):
        self.instruction_pointer = 0
        self.memory = [0 for i in range(MEMORYSIZE)]
        self.memory_pointer = 0
        self.running = False
    
    def run(self, in_buffer = None, out_buffer = None, instruction_start = 0):
        self.input_buffer = in_buffer
        self.output_buffer = out_buffer
        self.instruction_pointer = 0
        self.getBrackets()
        
        self.running = True
        while self.instruction_pointer < len(self.code):
            #self.step()
            instruction = self.code[self.instruction_pointer]
            self.executeInstruction(instruction)
            self.instruction_pointer += 1
        self.running = False
        
    def step(self):
        if self.instruction_pointer == len(self.code):
            self.running = False
        else:
            instruction = self.code[self.instruction_pointer]
            self.executeInstruction(instruction)
            self.instruction_pointer += 1
        
    def executeInstruction(self, instruction):
        if instruction == '>':
            self.memory_pointer += 1
            if self.memory_pointer >= self.memorysize:
                self.memory_pointer = 0
        elif instruction == '<':
            self.memory_pointer -= 1
            if self.memory_pointer < 0:
                self.memory_pointer = self.memorysize-1
        elif instruction == '+':
            self.memory[self.memory_pointer] += 1
            if self.memory[self.memory_pointer] > self.memorymaxvalue:
                self.memory[self.memory_pointer] = 0
        elif instruction == '-':
            self.memory[self.memory_pointer] -= 1
            if self.memory[self.memory_pointer] < 0:
                self.memory[self.memory_pointer] = self.memorymaxvalue
        elif instruction == '.':
            self.output(self.memory[self.memory_pointer])
        elif instruction == ',':
            b = self.getInput()
            if b:
                self.memory[self.memory_pointer] = b
            else:
                self.instruction_pointer -= 1
        elif instruction == '[':
            if self.memory[self.memory_pointer] == 0:
                self.instruction_pointer = self.brackets[self.instruction_pointer]
        elif instruction == ']':
            if self.memory[self.memory_pointer] != 0:
                self.instruction_pointer = self.brackets[self.instruction_pointer]
        else:
            # we can ignore this character
            pass
        
    def output(self, character):
        if self.output_buffer == None:
            if character == 10:
                print('\n',end='')
            else:
                print(chr(character),end='')
        else:
            self.output_buffer.append(chr(character)) # add the character to the end of the buffer
        
    def getInput(self):
        if self.input_buffer == None:
            return ord(input())
        else:
            if self.input_buffer:
                return ord(self.input_buffer.pop(0)) # read the first character of the input buffer
            else:
                # we can't read a byte
                return None
        
    def getBrackets(self):
        ''' create a list of corresponding opening and closing brackets '''
        self.brackets = {}
        brackets_start = []
        for position, command in enumerate(self.code):
            if command == '[':
                brackets_start.append(position)
            elif command == ']':
                start = brackets_start.pop()
                self.brackets[start] = position
                self.brackets[position] = start
        
if __name__ == '__main__':
    bf = BrainfsckEngine()
    bf.code = ",------------------------------------------------[->+++++[->+<]<]>>." # times by 5
    bf.run()