import numpy as np

class Decoder:
    """Classe para decodificar instruções do conjunto RV32I."""

    def __init__(self) -> None:
        pass

    def decode(self, instruction):
        """Extrai os campos da instrução e determina seu formato."""

        # Extrai os campos da instrução:
        opcode = instruction & 0x7F
        rs2 = (instruction >> 20) & 0x1F
        rs1 = (instruction >> 15) & 0x1F
        rd = (instruction >> 7) & 0x1F
        shamt = (instruction >> 20) & 0x1F
        funct3 = (instruction >> 12) & 0x7
        funct7 = (instruction >> 25)
        imm12_i = np.int32(instruction) >> 20
        imm12_s = ((np.int32(instruction) >> 25) << 5) | ((instruction >> 7) & 0x1F)
        imm13 = ((np.int32(instruction) >> 31) << 12) | (((instruction >> 25) & 0x3F) << 5) | (((instruction >> 8) & 0xF) << 1) | ((instruction >> 7) & 0x1)
        imm21 = ((np.int32(instruction) >> 31) << 20) | (((instruction >> 12) & 0xFF) << 12) | (((instruction >> 20) & 0x1) << 11) | (((instruction >> 21) & 0x3FF) << 1)
        imm20_u = instruction & 0xFFFFF000

        # Determina o formato da instrução:
        if opcode in [0x33, 0x3B]:  # R-type
            ins_format = 'R_FORMAT'
        elif opcode in [0x13, 0x1B, 0x67, 0x03]:  # I-type
            ins_format = 'I_FORMAT'
        elif opcode in [0x23]:  # S-type
            ins_format = 'S_FORMAT'
        elif opcode in [0x63]:  # SB-type
            ins_format = 'SB_FORMAT'
        elif opcode in [0x37, 0x17]:  # U-type
            ins_format = 'U_FORMAT'
        elif opcode in [0x6F]:  # UJ-type
            ins_format = 'UJ_FORMAT'
        else:
            raise ValueError(f"Opcode não reconhecido: {opcode}")

        return {
            'opcode': opcode,
            'rs1': rs1,
            'rs2': rs2,
            'rd': rd,
            'shamt': shamt,
            'funct3': funct3,
            'funct7': funct7,
            'imm12_i': imm12_i,
            'imm12_s': imm12_s,
            'imm13': imm13,
            'imm21': imm21,
            'imm20_u': imm20_u,
            'ins_format': ins_format
        }

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
