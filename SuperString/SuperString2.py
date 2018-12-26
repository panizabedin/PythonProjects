import os
import sys
import numpy as np
import math

# Read .fa/.fasta files from user's provided directory
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

# Find overlaps for all pairs of sequences in the files
all_pair_overlap = np.zeros(shape=(len(file_lines), len(file_lines)))  # mXm matrix stores pairs overlap lengths
for index_sequence1, sequence1 in enumerate(file_lines):
    for index_sequence2, sequence2 in enumerate(file_lines):
        if index_sequence1 != index_sequence2:
            overlap_length = min(len(sequence1), len(sequence2))

            while overlap_length > int(min(len(sequence1), len(sequence2)) / 2):
                if sequence1[-overlap_length:] != sequence2[:overlap_length]:
                    overlap_length -= 1
                else:
                    break

            if overlap_length > int(min(len(sequence1), len(sequence2)) / 2):
                all_pair_overlap[index_sequence1][index_sequence2] = overlap_length

# Remove columns and rows associated to the max overlap value, merge the two sequences and add it to the file_lines,
# and finally calculate overlaps for the new merged sequence
output = ''
while len(file_lines) > 1:
    max_overlap_index = np.argmax(all_pair_overlap)
    row_index = math.floor(max_overlap_index / len(file_lines))
    column_index = max_overlap_index % len(file_lines)
    max_overlap_value = int(all_pair_overlap[row_index][column_index])
    # If the max overlap is 0 we can find the final sequence by concatenating remaining sequences
    if max_overlap_value == 0:
        for lines in file_lines:
            output += lines
        break
    else:
        # Deleting rows and columns of the two sequences with max overlap
        all_pair_overlap = np.delete(all_pair_overlap, (row_index, column_index), axis=0)
        all_pair_overlap = np.delete(all_pair_overlap, (column_index, row_index), axis=1)

        merged_sequences = file_lines[row_index][:-max_overlap_value] + file_lines[column_index]

        # Removing the two sequences with max overlap from file_lines
        indices = row_index, column_index
        for index in sorted(indices, reverse=True):
            del file_lines[index]

        # Finding overlaps between newly created sequence and other sequences and adding them to the all_pair_overlap
        row = np.zeros((1, all_pair_overlap.shape[0]))
        for sequence_index, sequence in enumerate(file_lines):
            overlap_length = min(len(merged_sequences), len(sequence))
            while overlap_length > int(min(len(merged_sequences), len(sequence)) / 2):
                if merged_sequences[-overlap_length:] != sequence[:overlap_length]:
                    overlap_length -= 1
                else:
                    break
            if overlap_length <= int(min(len(merged_sequences), len(sequence)) / 2):
                overlap_length = 0
            row[0][sequence_index] = overlap_length
        all_pair_overlap = np.concatenate((all_pair_overlap, row), axis=0)
        column = np.zeros((all_pair_overlap.shape[0], 1))
        for sequence_index, sequence in enumerate(file_lines):
            overlap_length = min(len(merged_sequences), len(sequence))
            while overlap_length > int(min(len(merged_sequences), len(sequence)) / 2):
                if sequence[-overlap_length:] != merged_sequences[:overlap_length]:
                    overlap_length -= 1
                else:
                    break
            if overlap_length <= int(min(len(merged_sequences), len(sequence)) / 2):
                overlap_length = 0
            column[sequence_index] = overlap_length
        all_pair_overlap = np.concatenate((all_pair_overlap, column), axis=1)
        file_lines.append(merged_sequences)

# Printing the super string
if len(file_lines) > 1:
    print(output)
else:
    print(file_lines[0])
