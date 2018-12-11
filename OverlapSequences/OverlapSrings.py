import os

file_lines = []
sequences = []
directory_path = '/Users/paniz/Documents/Fasta_files/'

for filename in os.listdir(directory_path):
    if filename.endswith(".txt"):
        file_object = open(directory_path + filename, 'r')
        lines = file_object.readlines()
        for entry in lines:
            entry = entry.replace('\n', '')
            if entry != '':
                file_lines.append(entry)

for i, k in zip(file_lines[0::2], file_lines[1::2]):
    sequences.append([i, k])
print(sequences)
for name, seq in sequences:
    for name2, seq2 in sequences:
        if seq[-3:] == seq2[0:3] and name != name2:
            print(name, name2)
