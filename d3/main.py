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

    def __init__(self, parent_pos, vector):
        self.dir = Wire.dirs[vector[0][0]]
        self.magn = int(vector[0][1:])
        self.A = parent_pos
        B = add(mult(self.dir, self.magn), parent_pos)
        if len(vector) > 1:
            self.child = Wire(B, vector[1:])
        else:
            self.child = None

with open("input") as file:
    lines = file.readlines()
    wire1_indata = lines[0].split(",")
    wire2_indata = lines[1].split(",")

wires = [Wire((0,0), wire1_indata), Wire((0,0), wire2_indata)]
wiremap = {}

for index, wire in enumerate(wires):
    working_wire = wire
    while working_wire is not None:
        current_pos = working_wire.A
        for x in range(working_wire.magn):
            value = [0]*len(wires)
            if current_pos in wiremap:
                wiremap[current_pos][index] = 1
            else:
                value[index] = 1
                wiremap[current_pos] = value 
            current_pos = add(current_pos, working_wire.dir)
        working_wire = working_wire.child

closest_cross = 99999999
for pos, value in wiremap.items():
    if all(value) and (pos[0] != 0 and pos[1] != 0):
        distance = abs(pos[0]) + abs(pos[1])
        if distance < closest_cross:
            closest_cross = distance

print(closest_cross)