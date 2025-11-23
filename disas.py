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

		if self.mnemonic == 'aaa' and self.zero_operand(): #only in 32-bit mode
			self.opcode = 37
		else: self.opcode = ''

	def print(self):
		print(self.string)
	def print_tokens(self):
		for token in self.instruction_token_list:
			print(token)
	def print_opcode(self):
			print(self.opcode)
	def zero_operand(self):
		return self.operand1 == '' and self.operand2 == '' and self.operand3 == ''

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
'kxorw', 'kxorb', 'kxorq', 'kxord',
'lahf', 'lar', 'lddqu', 'ldmxcsr', 'lds', 'les', 'lfs', 'lgs', 'lss', 'ldtilecfg', 'lea', 'leave', 'lfence', 'lgdt', 'lidt', 'lldt', 'lmsw', 'loadiwkey',
'lock', 'lods', 'lodsb', 'lodsw', 'lodsd', 'lodsq', 'loop', 'loopcc', 'lsl', 'ltr', 'lzcnt',
'maskmovdqu', 'maskmovq', 'maxpd', 'maxps', 'maxsd', 'maxss', 'mfence', 'minpd', 'minps', 'minsd', 'minss', 'monitor', 'mov', 'movapd', 'movaps', 'movbe',
'movddup', 'movdir648', 'movdiri', 'movd', 'movq', 'movdq2q', 'movdqa', 'vmovdqa32', 'vmovdqa64', 'movdqu', 'vmovdqu8', 'vmovdqu16', 'vmovdqu32', 'vmovdqu64',
'movhlps', 'movhpd', 'movhps', 'movlhps', 'movlpd', 'movlps', 'movmskpd', 'movmskps', 'movntdq', 'movntdqa', 'movntdi', 'movntpd', 'movntps', 'movntq', 
'movq', 'movq2dq', 'movsd', 'movshdup', 'movsldup', 'movs', 'movsb', 'movsw', 'movsd', 'movsq', 'movss', 'movsx', 'movsxd', 'movupd', 'movups', 'movzx',
'mpsadbw', 'mul', 'mulpd', 'mulps', 'mulsd', 'mulss', 'mulx', 'mwait',
'neg', 'nop', 'not', 
'or', 'orpd', 'orps', 'out', 'outs', 'outsb', 'outsw', 'outsd', 
'pabsb', 'pabsw', 'pabsd', 'pabsq', 'packsswb', 'packssdw', 'packusdw', 'packuswb', 'paddb', 'paddw', 'paddd', 'paddq', 'paddsb', 'paddsw', 'paddusb', 
'paddusw', 'palignr', 'pand', 'pandn', 'pause', 'pavgb', 'pavgw', 'pblendvb', 'pblendw', 'pclmulqdq', 'pcmpeqb', 'pcmpeqw', 'pcmpeqd', 'pcmpeqq', 'pcmpestri',
'pcmpestrm', 'pcmpgtb', 'pcmpgtw', 'pcmpgtd', 'pcmpgtq', 'pcmpistri', 'pcmpistrm', 'pconfig', 'pdep', 'pext', 'pextrb', 'pextrd', 'pextrq', 'pextrw', 'phaddsw',
'phaddw', 'phaddd', 'phminposuw', 'phsubsw', 'phsubw', 'phsubd', 'pinsrb', 'pinsrd', 'pinsrq', 'pinsrw', 'pmaddubsw', 'pmaddwd', 'pmaxsb', 'pmaxsw', 'pmaxsd',
'pmaxsq', 'pmaxub', 'pmaxuw', 'pmaxud', 'pmaxuq', 'pminsb', 'pminsw', 'pminsd', 'pminsq', 'pminub', 'pminuw', 'pminud', 'pminuq', 'pmovmskb', 'pmovsx', 'pmovzx',
'pmuldq', 'pmulhrsw', 'pmulhuw', 'pmulhw', 'pmulld', 'pmullq', 'pmullw', 'pmulldq', 'pop', 'popa', 'popad', 'popcnt', 'popf', 'popfd', 'popfq', 'por', 
'prefetchh', 'prefetchw', 'psadbw', 'pshufb', 'pshufd', 'pshufhw', 'pshuflw', 'pshufw', 'psignb', 'psignw', 'psignd', 'pslldq', 'psllw', 'pslld', 'psllq', 
'psraw', 'psrad', 'psraq', 'psrldq', 'psrlw', 'psrld', 'psrlq', 'psubb', 'psubw', 'psubd', 'psubq', 'psubsb', 'psubsw', 'psubusb', 'psubusw', 'ptest', 
'ptwrite', 'punpckhbw', 'punpckhwd', 'punpckhdq', 'punpckhqdq', 'punpcklbw', 'punpcklwd', 'punpckldq', 'punpcklqdq', 'push', 'pusha', 'pushad', 'pushf',
'pushfd', 'pushfq', 'pxor', 
'rcl', 'rcr', 'rol', 'ror', 'rcpps', 'rcpss', 'rdfsbase', 'rdgsbase', 'rdmsr', 'rdmsrlist', 'rdpid', 'rdpkru', 'rdpmc', 'rdrand', 'rdseed', 'rdsspd', 
'rdsspq', 'rdtscp', 'rdtsc', 'rep', 'repe', 'repz', 'repne', 'repnz', 'ret', 'rorx', 'roundpd', 'roundps', 'roundsd', 'roundss', 'rsm', 'rsqrtps', 'rsqrtss',
'rstorssp', 
'sahf', 'sal', 'sar', 'shl', 'shr', 'sarx', 'shlx', 'shrx', 'saveprevssp', 'sbb', 'scas', 'scasb', 'scasw', 'scasd', 'senduipi', 'serialize', 'setcc',
'setssbsy', 'sfence', 'sgdt', 'sha1msg1', 'sha1msg2', 'sha1nexte', 'sha1rnds4', 'sha256msg1', 'sha256msg2', 'sha256rnds2', 'shld', 'shrd', 'shufpd', 
'shufps', 'sidt', 'sldt', 'smsw', 'sqrtpd', 'sqrtps', 'sqrtsd', 'sqrtss', 'stac', 'stc', 'std', 'sti', 'stmxcsr', 'stos', 'stosb', 'stosw', 'stosd',
'stosq', 'str', 'sttilecfg', 'stui', 'sub', 'subpd', 'subps', 'subsd', 'subss', 'swapgs', 'syscall', 'sysenter', 'sysexit', 'sysret', 
'tdpbf16ps', 'tdpbssd', 'tdbsud', 'tdpbusd', 'tdpbuud', 'tdpfp16ps', 'test', 'testui', 'tileloadd', 'tileloaddt1', 'tilerelease', 'tilestored', 'tilezero',
'tpause', 'tzcnt', 
'ucomisd', 'ucomiss', 'ud', 'uiret', 'umonitor', 'umwait', 'unpckhpd', 'unpckhps', 'unpcklpd', 'unpcklps',
'vaddph', 'vaddsh', 'valignd', 'valignq', 'vbcstnebf162ps', 'vbcstnesh2ps', 'vblendmpd', 'vblendmps', 'vbroadcast', 'vcmpph', 'vcmpsh', 'vcomish', 'vcompresspd',
'vcompressps', 'vcvtdq2ph', 'vcvtne2ps2bf16', 'vcvtneebf162ps', 'vcvtneeph2ps', 'vcvtneobf162ps', 'vcvtneoph2ps', 'vcvtneps2bf16', 'vcvtpd2ph', 'vcvtpd2qq',
'vcvtpd2udq', 'vcvtpd2uqq', 'vcvtph2dq', 'vcvtph2pd', 'vcvtph2ps', 'vcvtph2psx', 'vcvtph2qq', 'vcvtph2udq', 'vcvtph2uqq', 'vcvtph2uw', 'vcvtph2w', 
'vcvtps2ph', 'vcvtps2phx', 'vcvtps2qq', 'vcvtps2udq', 'vcvtps2uqq', 'vcvtqq2pd', 'vcvtqq2ph', 'vcvtqq2ps', 'vcvtsd2sh', 'vcvtsd2usi', 'vcvtsh2sd', 
'vcvtsh2si', 'vcvtsh2ss', 'vcvtsh2usi', 'vcvtsi2sh', 'vcvtss2sh', 'vcvtss2usi', 'vcvttpd2qq', 'vcvttpd2udq', 'vcvttpd2uqq', 'vcvttph2dq', 'vcvttph2qq',
'vcvttph2udq', 'vcvttph2uqq', 'vcvttph2uw', 'vcvttph2w', 'vcvttps2qq', 'vcvttps2udq', 'vcvttps2uqq', 'vcvttsd2usi', 'vcvttsh2si', 'vcvttsh2usi', 'vcvttss2usi',
'vcvtudq2pd', 'vcvtudq2ph', 'vcvtudq2ps', 'vcvtuqq2pd', 'vcvtuqq2ph', 'vcvtuqq2ps', 'vcvtusi2sd', 'vcvtusi2sh', 'vcvtusi2ss', 'vcvtuw2ph', 'vcvtw2ph', 
'vdbpsadbw', 'vdivph', 'vdivsh', 'vdpbf16ps', 'verr', 'verw', 'vexpandpd', 'vexpandps', 'vextractf128', 'vextractf32x4', 'vextractf64x2', 'vextractf32x8',
'vextractf64x4', 'vextracti128', 'vextracti32x4', 'vextracti64x2', 'vextracti32x8', 'vextracti64x4', 'vfcmaddcph', 'vfmaddcph', 'vfcmaddcph', 'vfmaddcph', 
'vfcmaddcsh', 'vfmaddcsh', 'vfcmulcph', 'vfmulcph', 'vfcmulcsh', 'vfmulcsh', 'vfixupimmpd', 'vfixupimmps', 'vfixupimmsd', 'vfixupimmss', 'vfmadd132pd', 
'vfmadd213pd', 'vfmadd231pd', 'vf[,N]madd[132,213,231]ph', 'vfmadd132ps', 'vfmadd213ps', 'vfmadd231ps', 'vfmadd132sd', 'vfmadd213sd', 'vfmadd231sd',
'vf[,n]madd[132,213,231]sh', 'vfmadd132ss', 'vfmadd213ss', 'vfmadd231ss', 'vfmaddsub132pd', 'vfmaddsub213pd', 'vfmaddsub231pd', 'vfmaddsub132ph', 'vfmaddsub213ph',
'vfmaddsub231ph', 'vfmaddsub132ps', 'vfmaddsub213ps', 'vfmaddsub231ps', 'vfmsub132pd', 'vfmsub213pd', 'vfmsub231pd', 'vf[,n]msub[132,213,231]ph', 'vfmsub132ps',
'vfmsub213ps', 'vfmsub231ps', 'vfmsub132sd', 'vfmsub213sd', 'vfmsub231sd', 'vf[,n]msub[132,213,231]sh', 'vfmsub132ss', 'vfmsub213ss', 'vfmsub231ss', 
'vfmsubadd132pd', 'vfmsubadd213pd', 'vfmsubadd231pd', 'vfmsubadd132ph', 'vfmsubadd213ph', 'vfmsubadd231ph', 'vfmsubadd132ps', 'vfmsubadd213ps', 'vfmsubadd231ps',
'vfnmadd132pd', 'vfnmadd213pd', 'vfnmadd231pd', 'vfnmadd132ps', 'vfnmadd213ps', 'vfnmadd231ps', 'vfnmadd132sd', 'vfnmadd213sd', 'vfnmadd231sd', 
'vfnmadd132ss', 'vfnmadd213ss', 'vfnmadd231ss', 'vfnmsub132pd', 'vfnmsub213pd', 'vfnmsub231pd', 'vfnmsub132ps', 'vfnmsub213ps', 'vfnmsub231ps', 
'vfnmsub132sd', 'vfnmsub213sd', 'vfnmsub231sd', 'vfnmsub132ss', 'vfnmsub213ss', 'vfnmsub231ss', 'vfpclasspd', 'vfpclassph', 'vfpclassps', 'vfpclasssd', 'vfpclasssh',
'vfpclassss', 'vgatherdpd', 'vgatherqpd', 'vgatherdps', 'vgatherdpd', 'vgatherdps', 'vgatherqps', 'vgatherqps', 'vgatherqpd', 'vgetexppd', 'vgetexpph', 'vgetexpps',
'vgetexpsd', 'vgetexpsh', 'vgetexpss', 'vgetmantpd', 'vgetmantph', 'vgetmantps', 'vgetmantsd', 'vgetmantsh', 'vgetmantss', 'vinsertf128', 'vinsertf32x4', 'vinsertf64x2',
'vinsertf32x8', 'vinsertf64x4', 'vinserti128', 'vinserti32x4', 'vinserti64x2', 'vinserti32x8', 'vinserti64x4', 'vmaskmov', 'vmaxph', 'vmaxsh', 'vminph', 'vminsh',
'vmovsh', 'vmovw', 'vmulph', 'vmulsh', 'vp2intersectd', 'vp2intersectq', 'vpblendd', 'vpblendmb', 'vpblendmw', 'vpblendmd', 'vpblendmq', 'vpbroadcast', 'vpbroadcastb',
'vpbroadcastw', 'vpbroadcastd', 'vpbroadcastq', 'vpbroadcastm', 'vpcmpb', 'vpcmpub', 'vpcmpd', 'vpcmpud', 'vpcmpq', 'vpcmpuq', 'vpcmpw', 'vpcmpuw', 'vpcompressb',
'vcompressw', 'vpcompressd', 'vpcompressq', 'vpconflictd', 'vpconflictq', 'vpdpb[su,uu,ss]d[,s]', 'vpdpbusd', 'vpdpbusds', 'vpdpwssd', 'vpdpwssds', 'vpdpw[su,us,uu]d[,s]',
'vperm2f128', 'vperm2i128', 'vperm8', 'vpermd', 'vpermw', 'vpermi2b', 'vpermi2w', 'vpermi2d', 'vpermi2q', 'vpermi2ps', 'vpermi2pd', 'vpermilpd', 'vpermilps', 
'vpermpd', 'vpermps', 'vpermq', 'vpermt2b', 'vpermt2w', 'vpermt2d', 'vpermt2q', 'vpermt2ps', 'vpermt2pd', 'vpexpandb', 'vpexpandw', 'vpexpandd', 'vpexpandq',
'vpgatherdd', 'vpgatherdq', 'vpgatherdd', 'vpgatherqd', 'vpgatherdq', 'vpgatherqq', 'vpgatherqd', 'vpgatherqq', 'vplzcntd', 'vplzcntq', 'vpmadd52huq',
'vpmadd52luq', 'vpmaskmov', 'vpmovb2m', 'vpmovw2m', 'vpmovd2m', 'vpmovq2m', 'vpmovdb', 'vpmovsdb', 'vpmovusdb', 'vpmovdw', 'vpmovsdw', 'vpmovusdw', 'vpmovm2b',
'vpmovm2w', 'vpmovm2d', 'vpmovm2q', 'vpmovqb', 'vpmovsqb', 'vpmovusqb', 'vpmovqd', 'vpmovsqd', 'vpmovusqd', 'vpmovqw', 'vpmovsqw', 'vpmovusqw', 'vpmovwb',
'vpmovswb', 'vpmovuswb', 'vpmultishiftqb', 'vpopcnt', 'vprold', 'vprolvd', 'vprolq', 'vprolvq', 'vprord', 'vprorvd', 'vprorq', 'vprorvq', 'vpscatterdd', 'vpscatterdq',
'vpscatterqd', 'vpscatterqq', 'vpshld', 'vpshldv', 'vpshrd', 'vpshrdv', 'vpshufbitqmb', 'vpsllvw', 'vpsllvd', 'vpsllvq', 'vpsravw', 'vpsravd', 'vpsravq',
'vpsrlvw', 'vpsrlvd', 'vpsrlvq', 'vpternlogd', 'vpternlogq', 'vptestmb', 'vptestmw', 'vptestmd', 'vptestmq', 'vptestnmb', 'vptestnmw', 'vptestmd', 'vptestnmq',
'vrangepd', 'vrangeps', 'vrangesd', 'vrangess', 'vrcp14pd', 'vrcp14ps', 'vrcp14sd', 'vrcp14ss', 'vrcpph', 'vrcpsh', 'vreducepd', 'vreduceph', 'vreduceps', 
'vreducesd', 'vreducesh', 'vreducess', 'vrndscalepd', 'vrndscaleph', 'vrndscaleps', 'vrndscalesd', 'vrndscalesh', 'vrndscaless', 'vrsqrt14pd', 'vrsqrt14ps',
'vrsqrt14sd', 'vrsqrt14ss', 'vrsqrtph', 'vrsqrtsh', 'vscalefpd', 'vscalefph', 'vscalefps', 'vscalefsd', 'vscalefsh', 'vscalefss', 'vscatterdps', 'vscatterdpd',
'vscatterqps', 'vscatterqpd', 'vsha512msg1', 'vsha512msg2', 'vsha512rnds2', 'vshuff32x4', 'vshuff64x2', 'vshufi32x4', 'vshufi64x2', 'vsm3msg1', 'vsm3msg2', 
'vsm3rnds2', 'vsm4key4', 'vsm4rnds4', 'vsqrtph', 'vsqrtsh', 'vsubph', 'vsubsh', 'vtestpd', 'vtestps', 'vucomish', 'vzeroall', 'vzeroupper',
'wait', 'fwait', 'wbinvd', 'wbnoinvd', 'wrfsbase', 'wrgsbase', 'wrmsr', 'wrmsrlist', 'wrmsrns', 'wrpkru', 'wrssd', 'wrssq', 'wrussd', 'wrussq', 
'xabort', 'xacquire', 'xrelease', 'xadd', 'xbegin', 'xchg', 'xend', 'xgetbv', 'xlat', 'xlatb', 'xor', 'xorpd', 'xorps', 'xresldtrk', 'xrstor', 'xrstors', 
'xsave', 'xsavec', 'xsaveopt', 'xsaves', 'xsetbv', 'xsusldtrk', 'xtest'
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
print('opcode: ',end='')
test_inst.print_opcode()


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
