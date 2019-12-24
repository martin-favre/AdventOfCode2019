with open("input") as file:
    input_digits = list(map(int, file.read().strip()))

img_width = 25
img_height = 6
black = 0
white = 1
transp = 2

def split_to_sublists(inlist, chunksize):
    nof_sublists = int(len(inlist)/chunksize)
    return [inlist[x*chunksize:x*chunksize + chunksize] for x in range(nof_sublists)]

def get_pixel(prev_pixel, next_pixel):
    return prev_pixel if next_pixel == transp else next_pixel

pixels = [[[] for y in range(img_width)] for x in range(img_height)]

for indx, pix in enumerate(input_digits):
    indx_in_pic = indx % (img_width*img_height)
    indx_row = int(indx_in_pic / img_width)
    indx_column = indx_in_pic % img_width
    pixels[indx_row][indx_column].insert(0,pix)

picture = [[2 for y in range(img_width)] for x in range(img_height)]
for row_indx, row in enumerate(pixels):
    for col_indx, pixelvals in enumerate(row):
        for value in pixelvals:
            old_pix = picture[row_indx][col_indx]
            picture[row_indx][col_indx] = get_pixel(old_pix, value)

for row in picture:    
    print(''.join(['#' if x == white else ' ' for x in row]))
