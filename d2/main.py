def calculate(data, pc):
    data[data[pc+3]] = data[data[pc+2]] + data[data[pc+1]] if data[pc] == 1 else data[data[pc+2]] * data[data[pc+1]]
    pc += 4
    return data[0] if data[pc] == 99 else calculate(data, pc)
print(calculate([12 if indx == 1 else 2 if indx == 2 else int(x, 0) for indx, x in enumerate (open("input").read().split(','))], 0))
