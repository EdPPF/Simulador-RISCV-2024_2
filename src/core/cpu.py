# Implementação da CPU (registradores, ciclo de execução)
import numpy as np

"""
Os registradores pc e ri, e também os campos da instrução (opcode, rs1, rs2, rd,
shamt, funct3, funct7) são definidos como variáveis globais. pc e ri são do tipo
unsigned int (uint32_t), visto que não armazenam dados, apenas endereços e
instruções. Os registradores sp e gp fazem parte do banco de registradores, e
armazenam os endereços das áreas de memória de pilha e dados globais,
respectivamente
"""

xregs = np.zeros(32, dtype=np.uint32) # yeah
"""Banco de registradores. Cada registrador é um inteiro de 32 bits sem sinal."""

# Campos da instrução
'''opcode = np.uint32(0)
rs1 = np.uint32(0)
rs2 = np.uint32(0)
rd = np.uint32(0)
shamt = np.uint32(0)
funct3 = np.uint32(0)
funct7 = np.uint32(0)
imm12_i = np.uint32(0)
imm12_s = np.uint32(0)
imm13 = np.uint32(0)
imm21 = np.uint32(0)
imm20_u = np.uint32(0)'''
