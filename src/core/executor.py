from collections import defaultdict
from decoder import Decoder
from memory import Memory
from cpu import xregs

# Função execute() para executar instruções
# A função execute() executa a instrução que foi lida pela função fetch() e decodificada por decode()

class Executor:
    def __init__(self, registers, memory) -> None:
        self.xregs = registers
        self.memory = memory
        self.pc = 0 #0x0?
        self.decoder = Decoder()

    def fetch(self) -> str:
        '''Lê a instrução da memória e incrementa o PC.'''
        instruction: str = self.memory.lw(self.pc, 0) # 0 porque a área de .text do RARS começa em 0 na memória
        self.pc += 4
        return instruction

    def execute(self, ic):
        '''Executa a instrução de acordo com o formato'''

        # Dict dispatch pattern. Bem legal pra substituir if-elif-else, apesar de eu poder usar match case no Python 3.10:
        # funcs = defaultdict(lambda *args: lambda *a: ValueError(f"Formato de instrução não reconhecido: {ic['ins_format']}"), {
        #     'R_FORMAT': self.execute_r,
        #     'I_FORMAT': self.execute_i,
        #     'S_FORMAT': self.execute_s,
        #     'SB_FORMAT': self.execute_sb,
        #     'U_FORMAT': self.execute_u,
        #     'UJ_FORMAT': self.execute_uj
        # })
        # funcs[ic['ins_format']](ic)

        # match case pattern:
        match ic['ins_format']:
            case 'R_FORMAT':
                self.execute_r(ic)
            case 'I_FORMAT':
                self.execute_i(ic)
            case 'S_FORMAT':
                self.execute_s(ic)
            case 'SB_FORMAT':
                self.execute_sb(ic)
            case 'U_FORMAT':
                self.execute_u(ic)
            case 'UJ_FORMAT':
                self.execute_uj(ic)
            case _:
                raise ValueError(f"Formato de instrução não reconhecido: {ic['ins_format']}")

        # if ic['ins_format'] == 'R_FORMAT':
        #     self.execute_r(ic)
        # elif ic['ins_format'] == 'I_FORMAT':
        #     self.execute_i(ic)
        # elif ic['ins_format'] == 'S_FORMAT':
        #     self.execute_s(ic)
        # elif ic['ins_format'] == 'SB_FORMAT':
        #     self.execute_sb(ic)
        # elif ic['ins_format'] == 'U_FORMAT':
        #     self.execute_u(ic)
        # elif ic['ins_format'] == 'UJ_FORMAT':
        #     self.execute_uj(ic)
        # else:
        #     raise ValueError(f"Formato de instrução não reconhecido: {ic['ins_format']}")

    def step(self):
        '''Executa um ciclo de instrução'''
        instruction = self.fetch()
        ic = self.decoder.decode(instruction)
        self.execute(ic)

    def execute_r(self, ic):
        """Executa instruções do formato R"""
        # Implementar a lógica de execução para instruções do formato R
        pass

    def execute_i(self, ic):
        """Executa instruções do formato I"""
        # Implementar a lógica de execução para instruções do formato I
        pass

    def execute_s(self, ic):
        """Executa instruções do formato S"""
        # Implementar a lógica de execução para instruções do formato S
        pass

    def execute_sb(self, ic):
        """Executa instruções do formato SB"""
        # Implementar a lógica de execução para instruções do formato SB
        pass

    def execute_u(self, ic):
        """Executa instruções do formato U"""
        # Implementar a lógica de execução para instruções do formato U
        pass

    def execute_uj(self, ic):
        """Executa instruções do formato UJ"""
        # Implementar a lógica de execução para instruções do formato UJ
        pass
