sequence = input("Enter genome sequence: ")
print(sequence)

if len(sequence) > 1000:
    print('Invalid sequence.')
else:
    counter = [0, 0, 0, 0]
    for c in sequence:
        if c == 'A' or c == 'a':
            counter[0] += 1
        elif c == 'C' or c == 'c':
            counter[1] += 1
        elif c == 'G' or c == 'g':
            counter[2] += 1
        elif c == 'T' or c == 't':
            counter[3] += 1
    print(counter[0], ' ', counter[1], ' ', counter[2], ' ', counter[3])
