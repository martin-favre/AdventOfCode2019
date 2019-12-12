def add(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])

def mult(pos, factor):
    return (pos[0] * factor, pos[1]* factor)

class Wire:
    dirs = {
        'U':(0,1),
        'R':(1,0),
        'D':(0,-1),
        'L':(-1,0)
    }

    def __init__(self, parent, vector):
        self.dir = Wire.dirs[vector[0][0]]
        self.magn = int(vector[0][1:])
        self.parent = parent
        if parent is not None:
            self.A = parent.B
            self.steps = parent.steps + self.magn
        else:
            self.A = (0,0)
            self.steps = self.magn
        
        self.B = add(mult(self.dir, self.magn), self.A)
        self.child = Wire(self, vector[1:]) if len(vector) > 1 else None
    
    def get_parent_steps(self):
        return self.parent.steps if self.parent else 0

class GridPoint:
    def __init__(self, size):
        self.flags = [0]*size
        self.steps = 0
    
    def mark_point(self, index, steps):
        if self.flags[index] == 0:
            self.flags[index] = 1
            self.steps += steps

    def is_cross(self):
        return all(self.flags)

with open("input") as file:
    lines = file.readlines()
    wire1_indata = lines[0].split(",")
    wire2_indata = lines[1].split(",")

wires = [Wire(None, wire1_indata), Wire(None, wire2_indata)]
wiremap = {}

for index, wire in enumerate(wires):
    working_wire = wire
    while working_wire is not None:
        current_pos = working_wire.A
        for x in range(working_wire.magn):
            steps = working_wire.get_parent_steps() + x
            if current_pos not in wiremap:
                wiremap[current_pos] = GridPoint(len(wires))
            wiremap[current_pos].mark_point(index, steps)
            current_pos = add(current_pos, working_wire.dir)
        working_wire = working_wire.child

best_cross = 99999999
for pos, value in wiremap.items():
    if value.is_cross() and (pos[0] != 0 and pos[1] != 0):
        sum_steps = value.steps
        if sum_steps < best_cross:
            best_cross = sum_steps

print(best_cross)
