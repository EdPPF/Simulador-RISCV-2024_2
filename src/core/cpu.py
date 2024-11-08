"""
Módulo de inicialização do processador com banco de registradores e definição de variáveis globais.
"""

import numpy as np
from memory import Memory
from executor import Executor

class ProgramCounterOverflowError(Exception):
    """Exceção lançada quando o Program Counter excede o limite do segmento de código."""
    pass

class CPU(Executor):
    def __init__(self, code_path, data_path):
        xregs = np.zeros(32, dtype=np.uint32) # yeah
        """Banco de registradores. Cada registrador é um inteiro de 32 bits sem sinal."""
        memory = Memory()
        # Carregar os dados do programa na memória:
        memory.load_mem(code_path, data_path)
        super().__init__(xregs, memory) # Inicializa o Executor com o banco de registradores e a memória

    def run(self):
        """
        Executa o programa até encontrar uma chamada de sistema para encerramento, ou até o pc ultrapassar o limite do segmento de código (2k words).
        """
        while True:
            self.step()
            if self.regs[32] >= 2048 * 4: # 2k words
                raise ProgramCounterOverflowError("PC ultrapassou o limite do segmento de código.")


"""
Os registradores pc e ri, e também os campos da instrução (opcode, rs1, rs2, rd,
shamt, funct3, funct7) são definidos como variáveis globais. pc e ri são do tipo
unsigned int (uint32_t), visto que não armazenam dados, apenas endereços e
instruções. Os registradores sp e gp fazem parte do banco de registradores, e
armazenam os endereços das áreas de memória de pilha e dados globais,
respectivamente
"""

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
