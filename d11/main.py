relative_base = 0

def expand_container(data, index):
    if len(data) <= index:
        data.extend([0]*(1 + index - len(data)))

def get_from_data(data, index):
    expand_container(data, index)
    return data[index]

def get_immediate(data, index):
    return get_from_data(data, index)

def get_position(data, index):
    return get_from_data(data, data[index])

def get_relative(data, index):
    global relative_base
    return get_from_data(data, relative_base+data[index])

def get_parameter(data, index, mode):
    parameter_mode = 0
    immediate_mode = 1
    relative_mode = 2
    if mode == parameter_mode:
        return get_position(data, index)
    elif mode == immediate_mode:
        return get_immediate(data, index)
    elif mode == relative_mode:
        return get_relative(data, index)
    else:
        raise AssertionError()

def set_parameter(data, index, mode, value):
    global relative_base
    parameter_mode = 0
    relative_mode = 2
    if mode == parameter_mode:
        expand_container(data, index)
        data[index] = value
    elif mode == relative_mode:
        expand_container(data, index+relative_base)
        data[index+relative_base] = value
    else:
        raise AssertionError()


def add(data, pc, modes):
    in1 = get_parameter(data, pc+1, modes[-1])
    in2 = get_parameter(data, pc+2, modes[-2])
    out = get_from_data(data, pc+3)
    expand_container(data, out)
    set_parameter(data, out, modes[-3], in1+in2)
    return pc +4

def mult(data, pc, modes):
    in1 = get_parameter(data, pc+1, modes[-1])
    in2 = get_parameter(data, pc+2, modes[-2])
    out = get_from_data(data, pc+3)
    expand_container(data, out)
    set_parameter(data, out, modes[-3], in1*in2)
    return pc +4

def take_input(data, pc, modes, inval):
    out = get_from_data(data, pc+1)
    expand_container(data, out)
    set_parameter(data, out, modes[-1], inval)
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
    out = get_from_data(data, pc+3)
    expand_container(data, out)
    set_parameter(data, out, modes[-3], 1 if in1 < in2 else 0)
    return pc+4

def equals(data, pc, modes):
    in1 = get_parameter(data, pc+1, modes[-1])
    in2 = get_parameter(data, pc+2, modes[-2])
    out = get_from_data(data, pc+3)
    expand_container(data, out)
    set_parameter(data, out, modes[-3], 1 if in1 == in2 else 0)
    return pc+4

def adjust_rel(data, pc, modes):
    global relative_base
    in1 = get_parameter(data, pc+1, modes[-1])
    relative_base += in1
    return pc+2

operations = {
    1: add,
    2: mult,
    3: take_input,
    4: print_output,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
    9: adjust_rel
}

class Pos:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def get_rotated(self, clockwise = True):
        if clockwise:
            return Pos(self.y, -self.x)
        else:
            return Pos(-self.y, self.x)

    def get_tuple(self):
        return (self.x, self.y)

with open("input") as file:
    indata = [int(x) for x in file.read().split(',')]
pc = 0
hull = {}
out = []
robot_pos = Pos(0,0)
robot_dir = Pos(0,1)
black = 0
white = 1
hull[robot_pos.get_tuple()] = white
while indata[pc] != 99:
    full_opcode = str(indata[pc])
    full_opcode = full_opcode.zfill(10)
    operation_code = int(full_opcode[-2:])
    modes = [int(x) for x in list(full_opcode[:-2])]
    operation = operations[operation_code]
    if operation == print_output:
        pc, retval = print_output(indata, pc, modes)
        out.append(retval)
    elif operation == take_input:
        color = hull[robot_pos.get_tuple()] if robot_pos.get_tuple() in hull else black
        pc = take_input(indata, pc, modes, color)
    else:
        pc = operation(indata, pc, modes)
    if len(out) == 2:
        color = out[0]
        clockwise = out[1] == 1
        hull[robot_pos.get_tuple()] = color
        
        robot_dir = robot_dir.get_rotated(clockwise)
        robot_pos.x += robot_dir.x
        robot_pos.y += robot_dir.y
        out = []
print(len(hull))

for key in hull:
    print(key)

with open("out", 'w+') as file:
    for y in reversed(range(-50, 50)):
        outstr = ""
        for x in range(-50, 50):
            if (x,y) in hull:
                outstr += '#' if hull[(x,y)] == white else '.'
            else:
                outstr += '.'
        outstr += '\n'
        file.write(outstr)