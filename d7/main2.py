from inspect import signature
from copy import deepcopy
from queue import Queue

def get_immediate(data, index):
    if index < 0:
        raise AssertionError()
    return data[index]

def get_position(data, index):
    if index < 0:
        raise AssertionError()
    return data[data[index]]

def get_parameter(data, index, mode):
    parameter_mode = 0
    return get_position(data, index) if mode == parameter_mode else get_immediate(data, index) 

def add(data, pc, modes):
    in1 = get_parameter(data, pc+1, modes[-1])
    in2 = get_parameter(data, pc+2, modes[-2])
    out = data[pc+3]
    data[out] = in1+in2
    return pc +4

def mult(data, pc, modes):
    in1 = get_parameter(data, pc+1, modes[-1])
    in2 = get_parameter(data, pc+2, modes[-2])
    out = data[pc+3]
    data[out] = in1*in2
    return pc +4

def take_input(data, pc, modes, value):
    out = data[pc+1]
    data[out] = value
    return pc+2

def print_output(data, pc, modes):
    in1 = get_parameter(data, pc+1, modes[-1])
    return pc+2, in1

def jump_if_true(data, pc, modes):
    in1 = get_parameter(data, pc+1, modes[-1])
    in2 = get_parameter(data, pc+2, modes[-2])
    return in2 if in1 else pc+3

def jump_if_false(data, pc, modes):
    in1 = get_parameter(data, pc+1, modes[-1])
    in2 = get_parameter(data, pc+2, modes[-2])
    return in2 if in1 == 0 else pc+3

def less_than(data, pc, modes):
    in1 = get_parameter(data, pc+1, modes[-1])
    in2 = get_parameter(data, pc+2, modes[-2])
    out = data[pc+3]
    data[out] = 1 if in1 < in2 else 0
    return pc+4

def equals(data, pc, modes):
    in1 = get_parameter(data, pc+1, modes[-1])
    in2 = get_parameter(data, pc+2, modes[-2])
    out = data[pc+3]
    data[out] = 1 if in1 == in2 else 0
    return pc+4

operations = {
    1: add,
    2: mult,
    3: take_input,
    4: print_output,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals
}

def increment(numberlist, index = 0):
    if index >= len(numberlist):
        return
    numberlist[index] += 1
    if numberlist[index] > 9:
        numberlist[index] = 5
        increment(numberlist, index+1)

class AmpState:
    def __init__(self, operations):
        self.pc = 0
        self.operations = deepcopy(operations)
        self.indata = Queue()
        self.outdata = Queue()

    def is_done(self):
        return self.operations[self.pc] == 99

    def calculate(self):
        if self.is_done():
            return
        full_opcode = str(self.operations[self.pc])
        full_opcode = full_opcode.zfill(10)
        operation = int(full_opcode[-2:])
        modes = [int(x) for x in list(full_opcode[:-2])]
        if operations[operation] == take_input:
            if self.indata.empty():
                return
            self.pc = take_input(self.operations, self.pc, modes, self.indata.get())
        elif operations[operation] == print_output:
            self.pc, retval = print_output(self.operations, self.pc, modes)
            self.outdata.put(retval)
        else:
            self.pc = operations[operation](self.operations, self.pc, modes)    

        self.calculate()

with open("input") as file:
    indata_operations = [int(x) for x in file.read().split(',')]

settings = [5,5,5,5,5]
max_THRUST = 0
while True:
    if len(set(settings)) == len(settings):
        amps = [AmpState(indata_operations) for x in range(len(settings))] 
        for x in range(len(settings)):
            amps[x].indata.put(settings[x])
        amps[0].indata.put(0)
                
        working_amp_index = 0
        while True:
            amps[working_amp_index].calculate()
            next_index = working_amp_index +1 if working_amp_index < len(amps) -1 else 0

            if amps[working_amp_index].is_done():
                thrust = amps[working_amp_index].outdata.get()
                if thrust > max_THRUST:
                    max_THRUST = thrust
                break

            while not amps[working_amp_index].outdata.empty():
                amps[next_index].indata.put(amps[working_amp_index].outdata.get())
            working_amp_index = next_index

    if settings == [9,9,9,9,9]:
        break
    else:
        increment(settings)

print(max_THRUST)
