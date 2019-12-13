
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

def take_input(data, pc, modes):
    in1 = int(input("Input please:"))
    out = data[pc+1]
    data[out] = in1
    return pc+2

def print_output(data, pc, modes):
    in1 = get_parameter(data, pc+1, modes[-1])
    print(in1)
    return pc+2

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

def calculate(data, pc):
    full_opcode = str(data[pc])
    full_opcode = full_opcode.zfill(10)
    operation = int(full_opcode[-2:])
    modes = [int(x) for x in list(full_opcode[:-2])]
    sliced = data[pc:pc+4]
    pc = operations[operation](data, pc, modes)    
    
    return data[0] if data[pc] == 99 else calculate(data, pc)

with open("input") as file:
    indata = [int(x) for x in file.read().split(',')]
    calculate(indata, 0)