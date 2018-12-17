import os
import sys

file_lines = []
directory_path = input("Enter the directory path of the folder including Fasta files")
for filename in os.listdir(directory_path):
    if filename.endswith(".fa") or filename.endswith(".fasta"):
        file_object = open(directory_path + filename, 'r')
        lines = file_object.readlines()
        for entry in lines:
            entry = entry.strip()
            # entry = entry.replace('\n', '')
            if entry != '':
                file_lines.append(entry)

sequences = [None] * int(len(file_lines) / 2)
j = 0
for i, k in zip(file_lines[0::2], file_lines[1::2]):
    sequences[j] = [i, k]
    j += 1

for name, seq in sequences:
    for name2, seq2 in sequences:
        if seq[-3:] == seq2[0:3] and name != name2:
            print(name, name2)
