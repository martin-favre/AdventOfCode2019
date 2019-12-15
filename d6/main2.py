import sys
class Orbiter:
    def __init__(self, string):
        self.parent = None
        self.string = string
    
    def set_parent(self, parent):
        assert self.parent == None
        self.parent = parent

    def get_nof_orbits(self):
        return self.parent.get_nof_orbits if self.parent is not None else 0

    def get_nof_orbits_to_parent(self, parent):
        if self == parent:
            return 0
        else:
            return self.parent.get_nof_orbits_to_parent(parent) + 1

with open("input") as file:
    input_lines = file.readlines()
    input_lines = [x.strip() for x in input_lines]

objects = {}
for line in input_lines:
    parent, child = line.split(")")
    if parent not in objects:
        objects[parent] = Orbiter(parent)
    if child not in objects:
        objects[child] = Orbiter(child)
    objects[child].set_parent(objects[parent])

me = objects["YOU"]
santa = objects["SAN"]
my_parent = me.parent
while my_parent is not None:
    santa_parent = santa.parent
    while santa_parent is not None:
        if my_parent == santa_parent:
            steps_to_common_parent_from_me = me.get_nof_orbits_to_parent(my_parent)
            steps_to_common_parent_from_santa = santa.get_nof_orbits_to_parent(my_parent)
            sum_steps = steps_to_common_parent_from_me + steps_to_common_parent_from_santa - 2
            print(sum_steps)
            sys.exit()
        else:
            santa_parent = santa_parent.parent
    my_parent = my_parent.parent
