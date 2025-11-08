'''
Instruction format for protected mode, real-address mode, and virtual-8086 mode (Ie-32 mode) (Intel manual vol 2 ch 2)
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
 7   6 5          3 2   0
 ===== ============ =====
| Mod | Reg/Opcode | R/M |
 ===== ============ =====

SiB field:
 7     6 5     3 2    0
 ======= ======= ======
| Scale | Index | Base |
 ======= ======= ======


Instruction format in Intel 64
Legacy Prefixes: as in Ie-32: group 1, group 2 or group 3 (optional)
REX Prefix (optional)
Opcode: 1-, 2-, or 3-byte opcode
ModR/M: 1 byte (if required)
SiB: 1 byte (if required)
Displacement: Address displacement of 1, 2, or 4 bytes
Immediate: Immediate data of 1, 2, or 4 bytes or none

 ================= ============ ======== ======== ===== ============== =========== 
| Legacy Prefixes | REX Prefix | Opcode | ModR/M | SiB | Displacement | Immediate |
 ================= ============ ======== ======== ===== ============== ===========

'''

import re

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
instruction_1_assembly is the class of assembly (not machine code) instruction for protected mode, real-address mode and virtual-8086 mode
'''

class instruction_1_assembly:
	def __init__(self, string):
		self.string = string
		self.instruction_token_list = self.string.split()
		if len(self.instruction_token_list)<4:
			for i in range(4-len(self.instruction_token_list)):
				self.instruction_token_list.append('')
		self.mnemonic = self.instruction_token_list[0]
		self.operand1 = self.instruction_token_list[1]
		self.operand2 = self.instruction_token_list[2]
		self.operand3 = self.instruction_token_list[3]
	def print(self):
		print(self.string)
	def print_tokens(self):
		for token in self.instruction_token_list:
			print(token)

assembly_instruction_list = [
'aaa','aad','aam','aas','adc','adcx','add','addpd','addps','addsd','addss','addsubpd','addsubps','adox','aesdec','aesdec128kl','aesdec256kl','aesdeclast','aesdecwide128kl',
'aesdecwide256kl','aesenc','aesenc128kl','aesenc256kl','aesenclast','aesencwide128kl','aesencwide256kl','aesimc','aeskeygenassist','and','andn','andnpd',
'andnps','andpd','andps','arpl',
]


print("Instruction string test: ")
sstr = re.sub(' +',' ',input().strip())
test_inst = instruction_1_assembly(sstr)
if test_inst.mnemonic not in assembly_instruction_list:
	print('Not a vlaid instruction')
test_inst.print()
test_inst.print_tokens()
print('mnemonic: ' + test_inst.mnemonic)
print('operand 1: ' + test_inst.operand1)
print('operand 2: ' + test_inst.operand2)
print('operand 3: ' + test_inst.operand3)

while True:
	print("Instruction: ")
	command = input()


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
