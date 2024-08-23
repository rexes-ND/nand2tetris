// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

@R1
D=M
@i
M=D // RAM[i] = RAM[1]

D=0
@sum
M=D // RAM[sum] = 0

(LOOP)
    @i
    D=M // D = RAM[i]
    @SAVE_SUM
    D;JEQ // if RAM[i] == 0, goto SAVE_TO_R2

    D=D-1
    @i
    M=D // RAM[i] = RAM[i] - 1

    @R0
    D=M
    @sum
    M=D+M // RAM[sum] = RAM[sum] + RAM[0]

    @LOOP
    0;JMP

(SAVE_SUM)
    @sum
    D=M
    @R2
    M=D // RAM[2] = RAM[sum]

(END)
    @END
    0;JMP


