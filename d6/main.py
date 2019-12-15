class Orbiter:
    def __init__(self, string):
        self.parent = None
        self.string = string
    def set_parent(self, parent):
        assert self.parent == None
        self.parent = parent

    def get_nof_orbits(self):
        return self.parent.get_nof_orbits if self.parent is not None else 0

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

nof_orbits = 0 
for key, obj in objects.items():
    nof_orbits += obj.get_nof_orbits()

print(nof_orbits)