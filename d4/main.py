
def increment(numberlist, index = -1):
    if index >= len(numberlist):
        return
    numberlist[index] += 1
    if numberlist[index] > 9:
        numberlist[index] = 0
        increment(numberlist, index-1)

def get_if_two_equals(numberlist):
    equals = []
    for digit in numberlist:
        if len(equals) > 0:
            if equals[-1] == digit:
                equals.append(digit)
            elif len(equals) == 2:
                return True
            else:
                equals.clear()
                equals.append(digit)
        else:
            equals.append(digit)
    return len(equals) == 2

minval = "130254"
maxval = "678275"
start_digits = [int(x) for x in minval]

valid_numbers = 0
numbers = int(maxval) - int(minval)
number_so_far = 0 
while True:
    number_so_far += 1
    if number_so_far % 1000 == 0:
        progress = number_so_far/numbers
        print(str(int(progress*100)) + '%', end='\r')

    increment(start_digits)

    previous_digit = None
    two_equal = get_if_two_equals(start_digits)
    always_greater = True
    for digit in start_digits:
        if previous_digit is not None:
            if digit < previous_digit:
                always_greater = False
                break
        previous_digit = digit
    if two_equal and always_greater:
        valid_numbers += 1

    working_number_real = num = int(''.join(map(str,start_digits)))
    if working_number_real > int(maxval):
        break
print("\n" + str(valid_numbers))

        

