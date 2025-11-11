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
'bextr', 'blendpd', 'blendps', 'blendvpd', 'blendvps', 'blsi', 'blsmsk', 'blsr', 'bndcl', 'bndcu', 'bndcn', 'bndldx', 'bndmk', 'bndmov', 'bndstx', 'bound',
'bsf', 'bsr', 'bswap', 'bt', 'btc', 'btr', 'bts', 'bzhi', 
'call', 'cbw', 'cwde', 'cdqe', 'clac', 'clc', 'cld', 'cldemote', 'clflush', 'clflushopt', 'cli', 'clrssbsy', 'clts', 'clui', 'clwb', 'cmc', 'cmov',
'cmp', 'cmpxadd', 'cmppd', 'cmpps', 'cmps', 'cmpsb', 'cmpsw', 'cmpsq', 'cmpsd', 'cmpss', 'cmpxchg', 'cmpxchgbb', 'cmpxchg16b', 'comisd', 'comiss', 'cpuid',
'crc32', 'cvtdq2pd', 'cvtdq2ps', 'cvtpd2dq', 'cvtpd2pi', 'cvtpd2ps', 'cvtpi2pd', 'cvtpi2ps', 'cvtps2dq', 'cvtps2pd', 'cvtps2pi', 'cvtsd2si', 'cvtsd2ss',
'cvtsi2sd', 'cvtsi2ss', 'cvtss2sd', 'cvtss2si', 'cvttpd2dq', 'cvttpd2pi', 'cvttps2dq', 'cvttps2pi', 'cvttsd2si', 'cvttss2si', 'cwd', 'cdq', 'cqo',
'daa', 'das', 'dec', 'div', 'divpd', 'divps', 'divsd', 'divss', 'dppd', 'dpps', 
'emms', 'encodekey128', 'encodekey256', 'endbr32', 'endbr64', 'enqcmd', 'enqcmds', 'enter', 'extractps', 
'f2xm1', 'fabs', 'fadd', 'faddp', 'fiadd', 'fbld', 'fbstp', 'fchs', 'fclex', 'fnclex', 'fcmov', 'fcom', 'fcomp', 'fcompp', 'fcomi', 'fcomip', 'fucomi', 'fucomip',
'fcos', 'fdecstp', 'fdiv', 'fdivp', 'fidiv', 'fdivr', 'fdivrp', 'fidivr', 'ffree', 'ficom', 'ficomp', 'fild', 'fincstp', 'finit', 'fninit', 'fist', 'fistp', 
'fisttp', 'fld', 'fld1', 'fld2t', 'fldpi', 'fldlg2', 'fldln2', 'fldz', 'fldcw', 'fldenv', 'fmul', 'fmulp', 'fimul', 'fnop', 'fpatan', 'fprem', 'fprem1', 
'fptan', 'frndint', 'frstor', 'fsave', 'fnsave', 'fscale', 'fsin', 'fsincos', 'fsqrt', 'fst', 'fstp', 'fstcw', 'fnstcw', 'fstenv', 'fnstenv', 'fstsw', 'fnstsw', 
'fsub', 'fsubp', 'fisub', 'fsubr', 'fsubrp', 'fisubr', 'ftst', 'fucom', 'fucomp', 'fucompp', 'fxam', 'fxch', 'fxrstor', 'fxsave', 'fxtract', 'fyl2x', 'fyl2xp1',
'gf2pbaffineinvqb', 'gf2pbaffineqb', 'gf2p8mulb', 
'haddpd', 'haddps', 'hlt', 'hreset', 'hsubpd', 'hsubps', 
'idiv', 'imul', 'in', 'inc', 'incsspd', 'incsspq', 'ins', 'insb', 'insw', 'insd', 'insertps', 'int', 'int0', 'int1', 'int3', 'invd', 'invlpg', 'invpcid', 
'iret', 'iretd', 'iretq',
'ja', 'jae', 'jb', 'jbe', 'jc', 'jcxz', 'jecxz', 'jrcxz', 'je', 'jg', 'jge', 'jl', 'jle', 'jna', 'jnae', 'jnb', 'jnbe', 'jnc', 'jne', 'jng', 'jnge', 'jnl',
'jnle', 'jno', 'jnp', 'jns', 'jnz', 'jo', 'jp', 'jpe', 'jpo', 'js', 'jz', 'jmp', 
'kaddw', 'kaddb', 'kaddq', 'kaddd', 'kandnw', 'kandnb', 'kandnq', 'kandnd', 'kandw', 'kandb', 'kandq', 'kandd', 'kmovw', 'kmovb', 'kmovq', 'kmovd', 'knotw', 
'knotb', 'knotq', 'knotd', 'kortestw', 'kortestb', 'kortestq', 'kortestd', 'korw', 'korb', 'korq', 'kord', 'kshiftw', 'kshiftb', 'kshiftq', 'kshiftld', 
'kshiftw', 'kshiftrb', 'kshiftrq', 'kshiftrd', 'ktestw', 'ktestb', 'ktestq', 'ktestd', 'kunpckbw', 'kunpckwd', 'kunpckdq', 'kxnorw', 'kxnorb', 'kxnorq', 'kxnord', 
'kxorw', 'kxorb', 'kxorq', 'kxord'
]


print("Instruction string test: ")
sstr = re.sub(' +',' ',input().strip())
test_inst = instruction_1_assembly(sstr)
if test_inst.mnemonic not in assembly_instruction_list:
	print('Not a vlaid instruction')
print('mnemonic: ' + test_inst.mnemonic)
print('operand 1: ' + test_inst.operand1)
print('operand 2: ' + test_inst.operand2)
print('operand 3: ' + test_inst.operand3)


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
