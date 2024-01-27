import sys
import re


class Block:
    def __init__(self, block_type):
        self.block_type = block_type
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)


if len(sys.argv) != 3:
    print("Incorrect args!")
    sys.exit(-1)

# Open Solution File and parse blocks
blocks = [Block('')]

re_block_start = r'//\$ START ?(\w*)'
re_block_end = r'//\$ END'

with open(sys.argv[1], 'r') as sol_file:
    for i, line in enumerate(sol_file):
        # Check if the line is a block start:
        block_match = re.search(re_block_start, line)
        if block_match:
            # Make sure the start block has a valid block type:
            block_type = block_match.group(1)
            if block_type != 'SOL' and block_type != 'EX':
                print('Error on line '+str(i+1)+": Invalid Block type \'" + str(block_type) + "\'!")
                sys.exit(-1)

            # Create a new block:
            blocks.append(Block(block_type))
            continue

        # Check if the line is a block end:
        if re.search(re_block_end, line):
            # Make sure we currently are inside a block:
            if blocks[-1].block_type == '':
                print('Error on line '+str(i+1)+": Attempted to end block, but currently not in a block!")
                sys.exit(-1)

            # Go to next standard block:
            blocks.append(Block(''))
            continue

        # Add line to current block.
        blocks[-1].add_line(line)

# Uncomment all EX blocks:
for block in blocks:
    if block.block_type == 'EX':
        for i, line in enumerate(block.lines):
            block.lines[i] = line.replace('// ', '', 1)

# Generate exercise file:
with open(sys.argv[2], 'w') as ex_file:
    for block in blocks:
        if block.block_type != 'SOL':
            for line in block.lines:
                ex_file.write(line)
