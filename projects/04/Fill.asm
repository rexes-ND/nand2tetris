// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

@dirty
M=0 // RAM[dirty] = 0

(LOOP)
    @dirty
    D=M 
    @notdirty
    M=!D // RAM[notdirty] = !RAM[dirty]

    @KBD
    D=M
    @notkey
    M=!D // RAM[notkey] = !RAM[KBD]

    @notkey
    D=M
    @notkey_dirty
    M=D
    @dirty
    D=M
    @notkey_dirty
    M=D&M // RAM[notkey_dirty] = RAM[notkey] & RAM[dirty]
    D=M
    @CLEAR
    D;JNE // if RAM[notkey_dirty], goto CLEAR

    @KBD
    D=M
    @key_notdirty
    M=D
    @notdirty
    D=M
    @key_notdirty
    M=D&M // RAM[key_notdirty] = RAM[KBD] & RAM[notdirty]
    D=M
    @FILL
    D;JNE // if RAM[key_notdirty], goto FILL

    @LOOP
    0;JEQ

(CLEAR)
    @dirty
    M=0

    @8191
    D=A
    @i
    M=D // RAM[i] = 8191

(CLEAR_LOOP)
    @i
    D=M
    @LOOP
    D;JLT

    // RAM[SCREEN+RAM[i]] = 0
    @SCREEN
    D=A
    @i
    A=D+M
    M=0
    
    @i
    M=M-1

    @CLEAR_LOOP
    0;JEQ

(FILL)
    @dirty
    M=1

    @8191
    D=A
    @i
    M=D // RAM[i] = 8191

(FILL_LOOP)
    @i
    D=M
    @LOOP
    D;JLT

    // RAM[SCREEN+RAM[i]] = -1
    @SCREEN
    D=A
    @i
    A=D+M
    M=-1

    @i
    M=M-1

    @FILL_LOOP
    0;JEQ

