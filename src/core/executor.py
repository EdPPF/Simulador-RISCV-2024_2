# Função execute() para executar instruções

"""
def decode(instruction_context_st& ic):
    '''Extrai todos os campos da instrução'''
    int32_t tmp
    opcode	= ri & 0x7F
    rs2		= (ri >> 20) & 0x1F
    rs1		= (ri >> 15) & 0x1F
    rd		= (ri >> 7)  & 0x1F
    shamt	= (ri >> 20) & 0x1F
    funct3	= (ri >> 12) & 0x7
    funct7  = (ri >> 25)
    imm12_i = ((int32_t)ri) >> 20
    tmp     = get_field(ri, 7, 0x1f)
    imm12_s = set_field(imm12_i, 0, 0x1f, tmp)
    imm13   = imm12_s
    imm13 = set_bit(imm13, 11, imm12_s&1)
    imm13 = imm13 & ~1
    imm20_u = ri & (~0xFFF)
    # mais aborrecido...
    imm21 = (int32_t)ri >> 11			# estende sinal
    tmp = get_field(ri, 12, 0xFF)		# le campo 19:12
    imm21 = set_field(imm21, 12, 0xFF, tmp)	# escreve campo em imm21
    tmp = get_bit(ri, 20)				# le o bit 11 em ri(20)
    imm21 = set_bit(imm21, 11, tmp)			# posiciona bit 11
    tmp = get_field(ri, 21, 0x3FF)
    imm21 = set_field(imm21, 1, 0x3FF, tmp)
    imm21 = imm21 & ~1					# zero bit 0
    ic.ins_code = get_instr_code(opcode, funct3, funct7)
    ic.ins_format = get_i_format(opcode, funct3, funct7)
    ic.rs1 = (REGISTERS)rs1
    ic.rs2 = (REGISTERS)rs2
    ic.rd = (REGISTERS)rd
    ic.shamt = shamt
    ic.imm12_i = imm12_i
    ic.imm12_s = imm12_s
    ic.imm13 = imm13
    ic.imm21 = imm21
    ic.imm20_u = imm20_u
"""
