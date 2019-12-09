import copy

def try_calculate(orig_data):
    for noun in range(0,100):
        for verb in range(0,100):
            data = copy.deepcopy(orig_data)
            data[1] = noun
            data[2] = verb
            out = calculate(data, 0)
            if out == 19690720:
                return 100*noun+verb
    raise AssertionError()

def calculate(data, pc):
    in1 = data[pc+1]
    in2 = data[pc+2]
    out = data[pc+3]
    if data[pc] == 1:
        data[out] = data[in1] + data[in2]
    elif data[pc] == 2:
        data[out] = data[in1] * data[in2]
    else:
        raise AssertionError()
    pc += 4
    return data[0] if data[pc] == 99 else calculate(data, pc)

indata = [int(x, 0) for x in open("input").read().split(',')]

out = try_calculate(indata)
print(out)
