'''
Instruction format for protected mode, real-address mode, and virtual-8086 mode (Intel manual vol 2 ch 2)
Instruction prefixes: prefixes of 1 byte each, in arbitrary order
Opcode: 1-, 2-, or 3-byte opcode
ModR/M: 1 byte (if required)
SiB: 1 byte (if required)
Displacement: Address displacement of 1, 2, or 4 bytes or none
Immediate: Immediate data of 1, 2, or 4 bytes or none

 ====================== ======== ======== ===== ============== ===========
| Instruction prefixes | Opcode | ModR/M | SiB | Displacement | Immediate |
 ====================== ======== ======== ===== ============== ===========

ModR/M field:
7    6 5          3 2   0
 ===== ============ =====
| Mod | Reg/Opcode | R/M |
 ===== ============ =====

SiB field:
 7     6 5     3 2    0
 ======= ======= ======
| Scale | Index | Base |
 ======= ======= ======

'''

opcode_dict={
	'37':'aaa',
	'd5 0a':'aad',
	'd5 ib':'aad imm8',
	'd4 0a':'aam',
	'd4 ib':'aam imm8',
	'3f':'aas',
	'14 ib':'adc al, imm8',
	'15 iw':'adc ax, imm16',
	'15 id':'adc eax, imm32',
	'rex.w + 15 id':'adc rax, imm32'
}

group1_prefix_dict={
	'f0h':'lock',
	'f2h':'repne/repz',
	'f3h':'rep/repe/repz',
	'f2h':'bnd' #with specific conditions
}

group2_prefix_dict={
	'2eh':'CS segment override',
	'36h':'SS segment override',
	'3eh':'DS segment override',
	'26h':'ES segment override',
	'64h':'FS segment override',
	'65h':'GS segment override',
	'2Eh':'Branch not taken', #used only with Jcc instructions
	'3eh':'Branch taken' #used only with Jcc instructions
}

group3_prefix_dict={
	'66h':'Operand-size override'
}

group4_prefix_dict={
	'67h':'Address-size override prefix'
}

'''
Opcodes:
One-byte opcode
Two-byte opcode formats:
-An escape opcode byte 0fH as the primary opcode and a second opcode byte
-A mandatory prefix (66H, f2H or f3H), an escape opcode byte, plus two additional opcode bytes (same as previous bullet).
Three-byte opcode formats:
-An escape opcode byte 0fH as the primary opcode, plus two additional opcode bytes
-a mandatory prefix (66H, f2H, or f3H), an escape opcode byte, plus two additional opcode bytes (same as previous bullet).
'''
