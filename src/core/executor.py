"""
Módulo de execução das instruções do RISC-V.\n
É responsável por:
- Buscar a instrução na memória;
- Decodificar a instrução por meio do módulo `Decoder`;
- Executar a instrução de acordo com o formato.
"""

from core.instruction_set import InstructionSet
from core.decoder import Decoder
import numpy as np

class Executor:
    """
    Função execute(): executa a instrução que foi lida pela função `fetch()` e decodificada por `Decoder.decode()`.
    """
    def __init__(self, registers, memory, pc) -> None:
        self.global_counter = 0
        self.ins_flag = ''
        self.xregs = registers
        self.memory = memory
        self.pc = pc
        self.decoder = Decoder()
        self.instruction_set = InstructionSet(self.xregs, self.memory)

    def fetch(self):
        '''Lê a instrução da memória e incrementa o PC.'''
        instruction = self.memory.lw((self.pc + 0)) # 0 porque a área de .text do RARS começa em 0 na memória
        self.pc += 4
        return instruction

    def execute(self, ic: dict[str]):
        '''
        Executa a instrução de acordo com o formato.\n
        `ic` é a instrução decodificada, que contém os campos da instrução e seu formato.
        '''
        match ic['ins_format']:
            case 'R_FORMAT':
                self.ins_flag = 'R_FORMAT'
                self.execute_r(ic)
            case 'I_FORMAT':
                self.ins_flag = 'I_FORMAT'
                self.execute_i(ic)
            case 'S_FORMAT':
                self.ins_flag = 'S_FORMAT'
                self.execute_s(ic)
            case 'B_FORMAT':
                self.ins_flag = 'B_FORMAT'
                self.execute_b(ic)
            case 'U_FORMAT':
                self.ins_flag = 'U_FORMAT'
                self.execute_u(ic)
            case 'J_FORMAT':
                self.ins_flag = 'J_FORMAT'
                self.execute_j(ic)
            case _:
                raise ValueError(f"Formato de instrução não reconhecido: {ic['ins_format']}")

    def step(self):
        '''Executa um ciclo de instrução'''
        instruction = self.fetch()                            # Lê a instrução da memória
        ic = self.decoder.decode(np.uint32(int(instruction))) # Retorna os campos da instrução e seu formato
        self.execute(ic)                                      # Executa a instrução
        self.global_counter += 1

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
        rs1 = ic['rs1']
        rs2 = ic['rs2']
        rd = ic['rd']
        funct3 = ic['funct3']
        funct7 = ic['funct7']
        match funct7:
            case 0x00: # 0000000
                match funct3:
                    case 0x00: # 000 ADD
                        # print("Executando ADD...")
                        self.instruction_set.add(rd, rs1, rs2)
                    case 0x01: # 001 SLL
                        raise NotImplementedError("Instrução SLL não implementada neste projeto!")
                    case 0x02: # 010 SLT
                        # print("Executando SLT...")
                        self.instruction_set.slt(rd, rs1, rs2)
                    case 0x03: # 011 SLTU
                        # print("Executando SLTU...")
                        self.instruction_set.sltu(rd, rs1, rs2)
                    case 0x04: # 100 XOR
                        # print("Executando XOR...")
                        self.instruction_set.xor(rd, rs1, rs2)
                    case 0x05: # 101 SRL
                        raise NotImplementedError("Instrução SRL não implementada neste projeto!")
                    case 0x06: # 110 OR
                        # print("Executando OR...")
                        self.instruction_set.or_(rd, rs1, rs2)
                    case 0x07: # 111 AND
                        # print("Executando AND...")
                        self.instruction_set.and_(rd, rs1, rs2)
                    case _:
                        raise ValueError(f"funct3 não reconhecido: {funct3}")
            case 0x20: # 0100000
                match funct3:
                    case 0x00: # 000 SUB
                        # print("Executando SUB...")
                        self.instruction_set.sub(rd, rs1, rs2)
                    case 0x05: # 101 SRA
                        raise NotImplementedError("Instrução SRA não implementada neste projeto!")
                    case _:
                        raise ValueError(f"funct3 não reconhecido: {funct3}")

    def execute_i(self, ic):
        # The immediate opcode OP-IMM==7'b001_0011. When opcode==OP-IMM==7'b001_0011,
        # it proves that the instruction is an I-type instruction, and the specific behavior of this instruction is determined by the value of funct3.
        """
        Executa instruções do formato I - Registrador para Registrador com Imediato\n
        O campo `funct3` seleciona o tipo da operação.\n
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
        ECALL:
        ```
        funct12 rs1 funct3 rd opcode
        12      5   3      5  7
        ECALL   0   PRIV   0  SYSTEM
        ```
        """
        rs1 = ic['rs1']
        rd = ic['rd']
        imm = ic['imm12_i']
        funct3 = ic['funct3']
        funct7 = ic['funct7']
        opcode = ic['opcode']

        if opcode == 0x73: # System opcode for ECALL
            if imm == 0x00:
                self.instruction_set.ecall()
            else:
                raise ValueError(f"Imediato não reconhecido: {imm}")
            return

        match opcode:
            case 0x03: # 0010011 -> lb, lw, lbu
                match funct3:
                    case 0x00: # 000 LB
                        # print("Executando LB...")
                        self.instruction_set.lb(rd, rs1, imm)
                    case 0x02: # 010 LW
                        # print("Executando LW...")
                        self.instruction_set.lw(rd, rs1, imm)
                    case 0x04: # 100 LBU
                        # print("Executando LBU...")
                        self.instruction_set.lbu(rd, rs1, imm)
                    case _: # LH, LHU
                        raise NotImplementedError("Instruções não implementadas neste projeto: LH, LHU")
            case 0x13: # 0010011 -> ADDI, SLTI, SLTIU, XORI, ORI, ANDI, SLLI, SRLI/SRAI
                match funct3:
                    case 0x00: # 000 ADDI
                        # print("Executando ADDI...")
                        self.instruction_set.addi(rd, rs1, imm)
                    case 0x02: # 010 SLTI
                        raise NotImplementedError("Instrução SLTI não implementada neste projeto!")
                    case 0x03: # 011 SLTIU
                        raise NotImplementedError("Instrução SLTIU não implementada neste projeto!")
                    case 0x07: # 111 ANDI
                        # print("Executando ANDI...")
                        self.instruction_set.andi(rd, rs1, imm)
                    case 0x06: # 110 ORI
                        # print("Executando ORI...")
                        self.instruction_set.ori(rd, rs1, imm)
                    case 0x04: # 100 XORI
                        raise NotImplementedError("Instrução XORI não implementada neste projeto!")
                    case 0x01: # 001 SLLI
                        # print("Executando SLLI...")
                        self.instruction_set.slli(rd, rs1, imm)
                    case 0x05: # 101 SRLI/SRAI
                        if funct7 == 0x00:
                            # print("Executando SRLI...")
                            self.instruction_set.srli(rd, rs1, imm)
                        elif funct7 == 0x20:
                            # print("Executando SRAI...")
                            self.instruction_set.srai(rd, rs1, imm)
                        else:
                            raise ValueError(f"funct7 não reconhecido: {funct7}")
                    case _:
                        raise ValueError(f"funct3 não reconhecido: {funct3}")
            case 0x23: # 0100011 -> sb, sw
                match funct3:
                    case 0x00: # 000 SB
                        # print("Executando SB...")
                        self.instruction_set.sb(rs1, imm, rd)
                    case 0x10: # 010 SW
                        # print("Executando SW...")
                        self.instruction_set.sw(rs1, imm, rd)
                    case _: # SH
                        raise NotImplementedError("Instrução SH não implementada neste projeto!")
            case 0x67: # 110111 JALR
                match funct3:
                    case 0x00: # 1100111 JALR
                        # print("Executando JALR...")
                        self.pc = self.instruction_set.jalr(rd, rs1, imm, self.pc)
                    case _:
                        raise ValueError(f"funct3 não reconhecido: {funct3}")

    def execute_s(self, ic):
        """
        Executa instruções do formato S - Store.\n
        Lê os registradores `rs1` e `rs2` como fonte dos operadores e escreve o resultado no registrador `rd`.\n
        Os campos `funct3` e `funct7` selecionam o tipo da operação.\n
        ```
        imm[11:5]    rs2 rs1  funct3 imm[4:0]    opcode
        7            5   5    3      5           7
        offset[11:5] src base width  offset[4:0] STORE
        ```
        """
        rs1 = ic['rs1']
        rs2 = ic['rs2']
        imm = ic['imm12_s']
        funct3 = ic['funct3']
        match funct3:
            case 0x00: # 000 SB
                # print("Executando SB...")
                self.instruction_set.sb(rs1, imm, rs2)
            case 0x01: # 001 SH
                raise NotImplementedError("Instrução SH não implementada neste projeto!")
            case 0x02: # 010 SW
                # print(f"Executando SW...")
                self.instruction_set.sw(rs1, imm, rs2)
            case _:
                raise ValueError(f"funct3 não reconhecido: {funct3}")

    def execute_b(self, ic):
        """
        Executa instruções do formato B - Branch.\n
        ```
        imm[12] imm[10:5] rs2  rs1 funct3 imm[4:1] imm[11] opcode
        1       6         5    5   3      4        1       7
        ```
        """
        rs1 = ic['rs1']
        rs2 = ic['rs2']
        imm = ic['imm13']
        funct3 = ic['funct3']
        match funct3:
            case 0x00: # 000 BEQ
                # print("Executando BEQ...")
                self.pc = self.instruction_set.beq(rs1, rs2, imm, self.pc)
            case 0x01: # 001 BNE
                # print(f"Executando BNE...")
                self.pc = self.instruction_set.bne(rs1, rs2, imm, self.pc)
            case 0x04: # 100 BLT
                # print(f"Executando BLT...")
                self.pc = self.instruction_set.blt(rs1, rs2, imm, self.pc)
            case 0x05: # 101 BGE
                # print(f"Executando BGE...")
                self.pc = self.instruction_set.bge(rs1, rs2, imm, self.pc)
            case 0x06: # 110 BLTU
                # print(f"Executando BLTU...")
                self.pc = self.instruction_set.bltu(rs1, rs2, imm, self.pc)
            case 0x07: # 111 BGEU
                # print(f"Executando BGEU...")
                self.pc = self.instruction_set.bgeu(rs1, rs2, imm, self.pc)
            case _:
                raise ValueError(f"funct3 não reconhecido: {funct3}")

    def execute_u(self, ic):
        """
        Executa instruções do formato U - Upper.\n
        ```
        imm[31:12] rd  opcode
        20         5   7
        ```
        """
        rd = ic['rd']
        imm = ic['imm20_u']
        opcode = ic['opcode']
        match opcode:
            case 0x17: # 0010111 AUIPC
                # print("Executando AUIPC...")
                self.instruction_set.auipc(rd, imm, self.pc)
            case 0x37: # 0110111 LUI
                # print("Executando LUI...")
                self.instruction_set.lui(rd, imm)

    def execute_j(self, ic):
        """
        Executa instruções do formato J - Jump.\n
        ```
        imm[20] imm[10:1] imm[11] imm[19:12] rd  opcode
        1       10        1       8          5   7
        ```
        """
        opcode = ic['opcode']
        imm = ic['imm21']
        rd = ic['rd']
        rs1 = ic['rs1']
        match opcode:
            case 0x6F: # 1101111 JAL
                # print("Executando JAL...")
                self.pc = self.instruction_set.jal(rd, imm, self.pc)
            case _:
                raise ValueError(f"opcode não reconhecido: {opcode}")
