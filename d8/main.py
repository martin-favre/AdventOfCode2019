with open("input") as file:
    input_digits = list(map(int, file.read().strip()))

img_width = 25
img_height = 6

def split_to_sublists(inlist, chunksize):
    nof_sublists = int(len(inlist)/chunksize)
    return [inlist[x*chunksize:x*chunksize + chunksize] for x in range(nof_sublists)]

def get_nof_number_in_list(inlist, number):
    return sum([x == number for x in inlist])

rows = split_to_sublists(input_digits, img_width)
layers = split_to_sublists(rows, img_height)
min_nof_zeroes = 9999999999
target_layer_index = 0
for layer in layers:
    nof_zeroes = sum([get_nof_number_in_list(row, 0) for row in layer])
    if nof_zeroes < min_nof_zeroes:
        min_nof_zeroes = nof_zeroes
        target_layer_index = layers.index(layer)

target_layer = layers[target_layer_index]
nof_ones = sum(get_nof_number_in_list(row, 1) for row in target_layer)
nof_twos = sum(get_nof_number_in_list(row, 2) for row in target_layer)
print(nof_ones*nof_twos)
