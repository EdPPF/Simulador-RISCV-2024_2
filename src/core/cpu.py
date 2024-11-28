"""
Módulo de inicialização do processador com banco de registradores e definição de variáveis globais.
"""

import numpy as np
from core.memory import Memory
from core.executor import Executor

class ProgramCounterOverflowError(Exception):
    """Exceção lançada quando o Program Counter excede o limite do segmento de código."""
    pass

class CPU(Executor):
    def __init__(self, code_path, data_path):
        self.PC = np.uint32(0)
        """Program Counter. Endereço da próxima instrução a ser executada."""
        self.xregs = np.zeros(32, dtype=np.uint32)
        """Banco de registradores. Cada registrador é um inteiro de 32 bits sem sinal."""

        memory = Memory()
        # Carregar os dados do programa na memória:
        memory.load_mem(code_path, data_path)
        super().__init__(self.xregs, memory, self.PC) # Inicializa o Executor com o banco de registradores e a memória

    def run(self):
        """
        Executa o programa até encontrar uma chamada de sistema para encerramento, ou até o pc ultrapassar o limite do segmento de código (2k words).
        """
        try:
            while True:
                self.step()
                # if self.PC >= 2048 * 4: # 2k words
                #     raise ProgramCounterOverflowError("Profram Counter ultrapassou o limite do segmento de código.")
        except ProgramCounterOverflowError as e:
            print(e)
        except SystemExit as e:
            print(f"System Exit: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")


"""
Os registradores pc e ri, e também os campos da instrução (opcode, rs1, rs2, rd,
shamt, funct3, funct7) são definidos como variáveis globais. pc e ri são do tipo
unsigned int (uint32_t), visto que não armazenam dados, apenas endereços e
instruções. Os registradores sp e gp fazem parte do banco de registradores, e
armazenam os endereços das áreas de memória de pilha e dados globais,
respectivamente
"""
