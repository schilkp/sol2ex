"""
sol2ex.py:
Convert code solutions to exercises.

Usage: python sol2ex.py solution_file.c exercise_file.c

Generates exercise_file.c from solution_file.c by removing all
solutions and uncommenting the exercises. Solutions and exercises
are delimited as follows:

    normal_code();

    //$ START EX
    // // TODO:  Find the correct function and call it.
    // _______();
    //$ END

    //$ START SOL
    correct_function();
    //$ END


sol2ex would convert the above snippet to the following:

    normal_code()

    // TODO:  Find the correct function and call it.
    _______();
"""

import re
from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class BlockType(Enum):
    NORM = 0
    SOL = 1
    EX = 2


@dataclass
class Block:
    block_type: BlockType
    lines: List[str]


@dataclass
class Sol2exException(Exception):
    msg: str
    line_no: int
    line: str


def main(solution_file: str, exercise_file: str):
    # Generate exercise_file from solution_file by:
    #  - Removing any solution blocks
    #  - Uncommenting any exercise blocks
    #
    # This is done by first seperating the input file into different blocks:
    # Normal text (NORM), solution text (SOL), or exercise text ((EX). These
    # blocks are then processed appropriately to generate the solutionf file.

    # Read input solution file:
    solution_lines = []
    try:
        with open(solution_file, 'r') as sfile:
            solution_lines.extend(sfile.readlines())
    except:
        print(f"SOL2EX ERROR: Failed to open {solution_file}!")
        return 1

    # Seperate into blocks:
    blocks = [Block(BlockType.NORM, [])]  # type: List[Block]
    try:
        for line_idx, line in enumerate(solution_lines):
            if line_is_block_start(line):
                # A new SOL or EX block is starting:
                block_type = extract_block_start(line, line_idx)
                blocks.append(Block(block_type, []))
            elif line_is_block_end(line):
                # A SOL or EX block is done. Return to normal text:
                blocks.append(Block(BlockType.NORM, []))
            elif line_is_inline_block(line):
                # Inline block.
                block_type, line = extract_inline_block(line, line_idx)
                blocks.append(Block(block_type, [line]))
                blocks.append(Block(blocks[-2].block_type, []))
            else:
                # A normal line. Add it to the current block:
                blocks[-1].lines.append(line)
    except Sol2exException as e:
        print(f"SOL2EX ERROR: {e.msg}")
        print(f"{solution_file}:{e.line_no}: {e.line}")
        return 1

    # Generate exercise file:
    try:
        with open(exercise_file, 'w') as efile:
            for block in blocks:
                if block.block_type == BlockType.NORM:
                    # Normal block. Included as-is in the output file:
                    efile.writelines(block.lines)
                elif block.block_type == BlockType.EX:
                    # Exercise block. Uncomment and include in output file:
                    lines = []
                    for line in block.lines:
                        lines.append(line.replace('// ', '', 1))
                    efile.writelines(lines)
                else:
                    # Soluion block. Do not include.
                    pass
    except:
        print(f"SOL2EX ERROR: Failed to open {exercise_file}!")
        return 1


def line_is_block_start(line: str) -> bool:
    return ("//$ START" in line)


def line_is_block_end(line: str) -> bool:
    return ("//$ END" in line)


def line_is_inline_block(line: str) -> bool:
    return line.rstrip().endswith("//$ SOL") or line.rstrip().endswith("//$ EX")


RE_BLOCK_START = re.compile(r'//\$ START ?(\w*)')


def extract_block_start(line: str, line_idx) -> BlockType:
    block_match = re.search(RE_BLOCK_START, line)
    if block_match:
        block_type = block_match.group(1)
        if block_type == "SOL":
            return BlockType.SOL
        elif block_type == "EX":
            return BlockType.EX
        else:
            raise Sol2exException(
                line_no=line_idx+1, msg=f"Invalid block type '{block_type}'.", line=line)
    else:
        raise Sol2exException(line_no=line_idx+1,
                              msg=f"Invalid start.", line=line)


def extract_inline_block(line: str, line_idx) -> Tuple[BlockType, str]:
    if "//$ SOL" in line:
        block_type = BlockType.SOL
        line = line.replace("//$ SOL", "")
        line = line.rstrip()
        line += "\n"
        return block_type, line
    elif "//$ EX" in line:
        block_type = BlockType.EX
        line = line.replace("//$ EX", "")
        line = line.rstrip()
        line += "\n"
        return block_type, line
    else:
        raise Sol2exException(line_no=line_idx+1,
                              msg=f"Invalid inline block.", line=line)


if __name__ == '__main__':
    parser = ArgumentParser(
        "sol2ex", description="Generate exercise_file from solution_file")
    parser.add_argument("solution_file")
    parser.add_argument("exercise_file")
    args = parser.parse_args()
    exit(main(args.solution_file, args.exercise_file))
