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