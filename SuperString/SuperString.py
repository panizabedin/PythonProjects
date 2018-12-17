import os
import sys

file_lines = []

directory_path = sys.argv[1]
for filename in os.listdir(directory_path):
    if filename.endswith(".fa") or filename.endswith(".fasta"):
        file_object = open(directory_path + filename, 'r')
        lines = file_object.readlines()

        for entry in lines:
            entry = entry.strip()
            if entry != '' and entry.startswith(('A', 'C', 'G', 'T')):
                file_lines.append(entry)
print(file_lines)

j = 0
max_pair1 = -1
max_pair2 = -1
index_1 = -1
index_2 = -1

output = ''
while len(file_lines) > 1:
    global_max_overlap = 0
    for index_sequence1, sequence1 in enumerate(file_lines):
        for index_sequence2, sequence2 in enumerate(file_lines):
            if index_sequence1 != index_sequence2:
                # if sequence2 != sequence1:
                overlap_length = min(len(sequence1), len(sequence2))

                while overlap_length > int(min(len(sequence1), len(sequence2))/2):
                    if sequence1[-overlap_length:] != sequence2[:overlap_length]:
                        overlap_length -= 1
                    else:
                        break

                if overlap_length <= int(min(len(sequence1), len(sequence2)) / 2):
                    overlap_length = 0

                if overlap_length > global_max_overlap:
                    max_pair1 = sequence1
                    max_pair2 = sequence2
                    index_1 = index_sequence1
                    index_2 = index_sequence2
                    global_max_overlap = overlap_length

    if global_max_overlap == 0:
        for lines in file_lines:
            output += lines
        break
    else:
        indices = index_1, index_2
        file_lines = [i for j, i in enumerate(file_lines) if j not in indices]
        max_pair1 = max_pair1[:-global_max_overlap]
        merged_sequences = max_pair1 + max_pair2
        file_lines.append(merged_sequences)

if len(file_lines) > 1:
    print(output)
else:
    print(file_lines[0])
