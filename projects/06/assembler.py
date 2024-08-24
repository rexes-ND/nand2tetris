import os
import sys

from typing import List

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <file_name>.asm")
        sys.exit(1)

    file_name = sys.argv[1]
    file_root, file_ext = os.path.splitext(file_name)

    if file_ext != ".asm":
        print(f"File name must end with .asm. Found {file_ext}")
        sys.exit(1)

    output_file_name = file_root + ".hack"

    file = open(file_name, "r")

    lines: List[str] = []
    for line in file:
        # 1. Remove comments
        comment_start = line.find("//")
        if comment_start >= 0:
            line = line[:comment_start]

        # 2. Remove whitespaces
        line = line.strip()

        # 3. Only non-empty line
        if line:
            lines.append(line)

    SYMBOL_TABLE = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        **{f"R{i}": i for i in range(16)},
        "SCREEN": 16384,
        "KBD": 24576,
    }

    lines_with_labels = lines
    lines = []
    instr_num = 0
    for line in lines_with_labels:
        if not line.startswith("("):
            lines.append(line)
            instr_num += 1
            continue
        label = line[1:-1]
        if label not in SYMBOL_TABLE:
            SYMBOL_TABLE[label] = instr_num

    var_num = 16
    for line in lines:
        if not line.startswith("@"):
            continue
        var = line[1:]
        if var in SYMBOL_TABLE:
            continue
        try:
            int(var)
            continue
        except ValueError:
            pass
        SYMBOL_TABLE[var] = var_num
        var_num += 1

    output_file = open(output_file_name, "w")
    for line in lines:
        if line.startswith("@"):
            # A instruction
            line = line[1:]
            try:
                addr = int(line)
            except ValueError:
                addr = SYMBOL_TABLE[line]
            output_file.write(bin(addr)[2:].zfill(16) + "\n")
            continue
        # C instruction: 111accccccdddjjj
        # dest=comp;jump
        dest = ""
        jump = ""
        equal_start = line.find("=")
        if equal_start >= 0:
            dest = line[:equal_start]
            line = line[equal_start + 1 :]
        comp = line
        semicolon_start = line.find(";")
        if semicolon_start >= 0:
            comp = line[:semicolon_start]
            jump = line[semicolon_start + 1 :]

        comp_to_str = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "M": "1110000",
            "!D": "0001101",
            "!A": "0110001",
            "!M": "1110001",
            "-D": "0001111",
            "-A": "0110011",
            "-M": "1110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "M+1": "1110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "M-1": "1110010",
            "D+A": "0000010",
            "D+M": "1000010",
            "D-A": "0010011",
            "D-M": "1010011",
            "A-D": "0000111",
            "M-D": "1000111",
            "D&A": "0000000",
            "D&M": "1000000",
            "D|A": "0010101",
            "D|M": "1010101",
        }

        dest_to_str = {
            "": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111",
        }

        jump_to_str = {
            "": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",
        }

        output_file.write("111")
        output_file.write(comp_to_str[comp])
        output_file.write(dest_to_str[dest])
        output_file.write(jump_to_str[jump])
        output_file.write("\n")
