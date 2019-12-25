import math
class Pos:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def get_normalized(self):
        magn = self.get_magnitude()
        return Pos(self.x/magn, self.y/magn)

    def get_magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def __hash__(self):
        return hash((self.x,self.y))

    def __eq__(self, other):
        xok = math.isclose(self.x, other.x, rel_tol=0.00001)
        yok = math.isclose(self.y, other.y, rel_tol=0.00001)
        return xok and yok

def get_line_from_to(_from, to):
    return Pos(to.x - _from.x, to.y - _from.y)

with open("input") as file:
    spacemap = {}
    for y, row in enumerate(file.readlines()):
        row = row.strip()
        mapheight = y+1
        for x in range(len(row)):
            mapwidth = x+1
            spacemap[Pos(x,y)] = row[x]
asteroid_type = '#'
space_type = ' '

asteroid_positions = []
for y in range(mapheight):
    for x in range(mapwidth):
        pos = Pos(x,y)
        if spacemap[pos] == asteroid_type:
            asteroid_positions.append(pos)

max_seen_asteroids = 0
best_pos = None
for moon_base in asteroid_positions:
    seen_asteroids = []
    for asteroid in asteroid_positions:
        if moon_base == asteroid:
            continue
        og_line = get_line_from_to(moon_base, asteroid)
        og_direction = og_line.get_normalized()
        og_distance = og_line.get_magnitude()
        valid_asteroid = True
        for other_asteroid in asteroid_positions:
            if asteroid == other_asteroid:
                continue
            if moon_base == other_asteroid:
                continue
            other_line = get_line_from_to(moon_base, other_asteroid)
            other_direction = other_line.get_normalized()
            other_distance = other_line.get_magnitude()
            if other_direction == og_direction:
                if other_distance < og_distance:
                    valid_asteroid = False
                    break
        if valid_asteroid:
            seen_asteroids.append(asteroid)
    if len(seen_asteroids) > max_seen_asteroids:
        max_seen_asteroids = len(seen_asteroids)
        best_pos = moon_base

print(best_pos)
print(max_seen_asteroids) 
