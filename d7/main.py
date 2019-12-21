from inspect import signature
from copy import deepcopy
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

def take_input(data, pc, modes, invals):
    in1 = invals[0]
    out = data[pc+1]
    data[out] = in1
    return pc+2, invals[1:]

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

def calculate(data, invals, pc = 0, outval = None):
    full_opcode = str(data[pc])
    full_opcode = full_opcode.zfill(10)
    operation = int(full_opcode[-2:])
    modes = [int(x) for x in list(full_opcode[:-2])]
    if operations[operation] == take_input:
        pc, invals = take_input(data, pc, modes, invals)
    elif  operations[operation] == print_output:
        pc, retval = print_output(data, pc, modes)
        assert outval == None
        outval = retval
    else:
        pc = operations[operation](data, pc, modes)    
    if data[pc] == 99:
        return outval
    else:
        return calculate(data, invals, pc, outval)

def increment(numberlist, index = 0):
    if index >= len(numberlist):
        return
    numberlist[index] += 1
    if numberlist[index] > 4:
        numberlist[index] = 0
        increment(numberlist, index+1)


with open("input") as file:
    indata_operations = [int(x) for x in file.read().split(',')]
    settings = [0,0,0,0,0]
    max_outdata = 0
    while True:
        outdata = 0
        if len(set(settings)) == len(settings):
            for setting in settings:
                indata = [setting, outdata]
                indata_operations_copy = deepcopy(indata_operations)
                outdata = calculate(indata_operations_copy, indata)
            if outdata > max_outdata:
                max_outdata = outdata
        increment(settings)
        if settings == [4,4,4,4,4]:
            break 
    print(max_outdata)