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
        match funct7:
            case 0x00: # 0000000
                match funct3:
                    case 0x00: # 000 ADD
                        InstructionSet().add(rd, rs1, rs2)
                    case 0x01: # 001 SLL
                        raise NotImplementedError("Instrução SLL não implementada neste projeto!")
                    case 0x02: # 010 SLT
                        InstructionSet().slt(rd, rs1, rs2)
                    case 0x03: # 011 SLTU
                        InstructionSet().sltu(rd, rs1, rs2)
                    case 0x05: # 100 XOR
                        InstructionSet().xor(rd, rs1, rs2)
                    case 0x04: # 101 SRL
                        raise NotImplementedError("Instrução SRL não implementada neste projeto!")
                    case 0x06: # 110 OR
                        InstructionSet().sor(rd, rs1, rs2)
                    case 0x07: # 111 AND
                        InstructionSet().sand(rd, rs1, rs2)
                    case _:
                        raise ValueError(f"funct3 não reconhecido: {funct3}")
            case 0x20: # 0100000
                match funct3:
                    case 0x00: # 000 SUB
                        InstructionSet().sub(rd, rs1, rs2)
                    case 0x05: # 101 SRA
                        raise NotImplementedError("Instrução SRA não implementada neste projeto!")
                    case _:
                        raise ValueError(f"funct3 não reconhecido: {funct3}")

    def execute_i(self, ic):
        """
        Executa instruções do formato I - Registrador para Registrador com Imediato\n
        O campo `funct3` seleciona o tipo da operação.\n
        The immediate opcode OP-IMM==7'b001_0011. When opcode==OP-IMM==7'b001_0011,
        it proves that the instruction is an I-type instruction, and the specific behavior of this instruction is determined by the value of funct3.
        ```
        imm[11:0]         rs1 funct3        rd   opcode
        12                5   3             5    7
        I-immediate[11:0] src ADDI/SLTI[U]  dest OP-IMM    SLTI[U] não implementada!
        I-immediate[11:0] src ANDI/ORI/XORI dest OP-IMM    XORI não implementada!
        ```
        Instruções de shift:
        ```
        imm[11:5] imm[4:0]   rs1 funct3 rd   opcode
        7         5          5   3      5    7
        0000000   shamt[4:0] src SLLI   dest OP-IMM
        0000000   shamt[4:0] src SRLI   dest OP-IMM
        0100000   shamt[4:0] src SRAI   dest OP-IMM
        ```
        """
        fields = Decoder().decode(ic)
        rs1 = self.xregs[fields['rs1']]
        rd = fields['rd']
        imm = fields['imm12_i']
        funct3 = fields['funct3']
        funct7 = fields['funct7']
        match funct3:
            case 0x00: # 000 ADDI
                InstructionSet().addi(rd, rs1, imm)
            case 0x02: # 010 SLTI
                raise NotImplementedError("Instrução SLTI não implementada neste projeto!")
            case 0x03: # 011 SLTIU
                raise NotImplementedError("Instrução SLTIU não implementada neste projeto!")
            case 0x07: # 111 ANDI
                InstructionSet().andi(rd, rs1, imm)
            case 0x06: # 110 ORI
                InstructionSet().ori(rd, rs1, imm)
            case 0x04: # 100 XORI
                raise NotImplementedError("Instrução XORI não implementada neste projeto!")
            case 0x01: # 001 SLLI
                InstructionSet().slli(rd, rs1, imm)
            case 0x05: # 101 SRLI/SRAI
                if funct7 == 0x00:
                    InstructionSet().srli(rd, rs1, imm)
                elif funct7 == 0x20:
                    InstructionSet().srai(rd, rs1, imm)
                else:
                    raise ValueError(f"funct7 não reconhecido: {funct7}")
            case _:
                raise ValueError(f"funct3 não reconhecido: {funct3}")

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
