"""
Módulo para decodificar instruções do conjunto RV32I.\n
A partir da instrução em binário, extrai os campos da instrução e determina seu formato.\n
O retorno é no padrão:
```python
{
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
```
"""

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
        funct3 = (instruction >> 12) & 0x7
        funct7 = (instruction >> 25)

        if opcode in [0x33, 0x3B]:  # R-type
            ins_format = 'R_FORMAT'
            return {
                'opcode': opcode,
                'funct7': funct7,
                'rs2': rs2,
                'rs1': rs1,
                'funct3': funct3,
                'rd': rd,
                'ins_format': ins_format,
            }
        elif opcode in [0x13, 0x67, 0x03, 0x73]:  # I-type
            ins_format = 'I_FORMAT'
            imm12_i = np.int32(instruction) >> 20
            return {
                'opcode': opcode,
                'funct7': funct7,
                'imm12_i': imm12_i,
                'rs1': rs1,
                'funct3': funct3,
                'rd': rd,
                'ins_format': ins_format,
            }
        elif opcode in [0x23]:  # S-type
            ins_format = 'S_FORMAT'
            imm12_s = ((np.int32(instruction) >> 25) << 5) | ((instruction >> 7) & 0x1F)
            return {
                'opcode': opcode,
                'imm12_s': imm12_s,
                'rs2': rs2,
                'rs1': rs1,
                'funct3': funct3,
                'ins_format': ins_format,
            }
        elif opcode in [0x63]: # B-type
            ins_format = 'B_FORMAT'
            imm13 = ((np.int32(instruction) >> 31) << 12) | (((instruction >> 25) & 0x3F) << 5) | (((instruction >> 8) & 0xF) << 1) | ((instruction >> 7) & 0x1)
            return {
                'opcode': opcode,
                'imm13': imm13,
                'rs2': rs2,
                'rs1': rs1,
                'funct3': funct3,
                'ins_format': ins_format,
            }
        elif opcode in [0x37, 0x17]:  # U-type
            ins_format = 'U_FORMAT'
            imm20_u = instruction >> 12 #& 0xFFFFF000
            return {
                'opcode': opcode,
                'imm20_u': imm20_u,
                'rd': rd,
                'ins_format': ins_format,
            }
        elif opcode in [0x6F]:  # J-type
            ins_format = 'J_FORMAT'
            imm21 = ((instruction >> 31) << 20) | (((instruction >> 12) & 0xFF) << 12) | (((instruction >> 20) & 0x1) << 11) | (((instruction >> 21) & 0x3FF) << 1)
            return {
                'opcode': opcode,
                'imm21': imm21,
                'rs1': rs1,
                'rd': rd,
                'ins_format': ins_format,
            }
        else:
            raise ValueError(f"Opcode não reconhecido: {bin(opcode)}")
