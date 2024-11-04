from collections import defaultdict
from instruction_set import InstructionSet
from decoder import Decoder
from memory import Memory
from cpu import xregs

# Função execute() para executar instruções
# A função execute() executa a instrução que foi lida pela função fetch() e decodificada por decode()

class Executor:
    def __init__(self, registers, memory) -> None:
        self.xregs = registers
        self.memory = memory
        self.pc = 0 # 0x0?
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

    def step(self):
        '''Executa um ciclo de instrução'''
        instruction = self.fetch()
        ic = self.decoder.decode(instruction)
        self.execute(ic)

    def execute_r(self, ic):
        """
        Executa instruções do formato R - Registrador para Registrador\n
        Lê os registradores `rs1` e `rs2`como fonte dos operadores e escreve o resultado no registrador `rd`.\n
        Os campos `funct7` e `funct3` selecionam o tipo da operação.\n
        ```
        funct7  rs2  rs1  funct3        rd  opcode
        7       5    5    3             5   7
        0000000 src2 src1 ADD/SLT/SLTU dest OP
        0000000 src2 src1 AND/OR/XOR   dest OP
        0000000 src2 src1 SLL/SRL      dest OP     SLL e SRL não implementadas!
        0100000 src2 src1 SUB/SRA      dest OP     SRA não implementada!
        ```
        """
        fields = Decoder().decode(ic)
        rs1 = self.xregs[fields['rs1']]
        rs2 = self.xregs[fields['rs2']]
        rd = fields['rd']
        funct3 = fields['funct3']
        funct7 = fields['funct7']
        opcode = fields['opcode']
        match funct7:
            case 0: # 0000000
                match funct3:
                    # ADD
                    case 0: # 000
                        InstructionSet().add(rd, rs1, rs2)
                    # SLT
                    case 1: # 001
                        InstructionSet().slt(rd, rs1, rs2)
                    # SLTU
                    case 2: # 010
                        InstructionSet().sltu(rd, rs1, rs2)
                    # AND
                    case 3: # 011
                        InstructionSet().sand(rd, rs1, rs2)
                    # OR
                    case 4: # 011
                        InstructionSet().sor(rd, rs1, rs2)
                    # XOR
                    case 5: # 100
                        InstructionSet().xor(rd, rs1, rs2)
                    # SLL
                    case 6: # 101
                        raise NotImplementedError("Instrução SLL não implementada neste projeto!")
                    # SRL
                    case 7: # 110
                        raise NotImplementedError("Instrução SRL não implementada neste projeto!")
                    case _:
                        raise ValueError(f"funct3 não reconhecido: {funct3}")
            case 32: # 0100000
                match funct3:
                    # SUB
                    case 0: # 000
                        InstructionSet().sub(rd, rs1, rs2)
                    # SRA
                    case 5: # 101
                        raise NotImplementedError("Instrução SRA não implementada neste projeto!")
                    case _:
                        raise ValueError(f"funct3 não reconhecido: {funct3}")

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
