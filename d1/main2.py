def get_fuel(module):
    fuel = int(module/3)-2 
    return 0 if fuel <= 0 else fuel + get_fuel(fuel)

print(sum([get_fuel(int(line, 0)) for line in open("input").readlines()]))