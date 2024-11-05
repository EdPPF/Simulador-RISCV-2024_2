# from collections import defaultdict # Para usar o dict dispatch pattern
from instruction_set import InstructionSet
from decoder import Decoder
from cpu import xregs


class Executor:
    """
    Função execute(): executa a instrução que foi lida pela função `fetch()` e decodificada por `Decoder.decode()`.
    """
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

    def execute(self, ic: dict[str]):
        '''
        Executa a instrução de acordo com o formato.\n
        `ic` é a instrução decodificada, que contém os campos da instrução e seu formato.
        '''

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

        match ic['ins_format']:
            case 'R_FORMAT':
                self.execute_r(ic)
            case 'I_FORMAT':
                self.execute_i(ic)
            case 'S_FORMAT':
                self.execute_s(ic)
            case 'B_FORMAT':
                self.execute_b(ic)
            case 'U_FORMAT':
                self.execute_u(ic)
            case 'J_FORMAT':
                self.execute_j(ic)
            case _:
                raise ValueError(f"Formato de instrução não reconhecido: {ic['ins_format']}")

    def step(self):
        '''Executa um ciclo de instrução'''
        instruction = self.fetch()            # Lê a instrução da memória
        ic = self.decoder.decode(instruction) # Retorna os campos da instrução e seu formato
        self.execute(ic)                      # Executa a instrução

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
        rs1 = self.xregs[ic['rs1']]
        rs2 = self.xregs[ic['rs2']]
        rd = ic['rd']
        funct3 = ic['funct3']
        funct7 = ic['funct7']
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
        ECALL:
        ```
        funct12 rs1 funct3 rd opcode
        12      5   3      5  7
        ECALL   0   PRIV   0  SYSTEM
        ```
        """
        rs1 = self.xregs[ic['rs1']]
        rd = ic['rd']
        imm = ic['imm12_i']
        funct3 = ic['funct3']
        funct7 = ic['funct7']
        opcode = ic['opcode']

        if opcode == 0x73: # System opcode for ECALL
            if imm == 0x00:
                InstructionSet().ecall()
            else:
                raise ValueError(f"Imediato não reconhecido: {imm}")
            return

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
        rs1 = self.xregs[ic['rs1']]
        rs2 = self.xregs[ic['rs2']]
        imm = ic['imm12_s']
        funct3 = ic['funct3']
        match funct3:
            case 0x00: # 000 SB
                self.memory.sb(rs1, imm, rs2)
            case 0x01: # 001 SH
                raise NotImplementedError("Instrução SH não implementada neste projeto!")
            case 0x02: # 010 SW
                self.memory.sw(rs1, imm, rs2)
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
        rs1 = self.xregs[ic['rs1']]
        rs2 = self.xregs[ic['rs2']]
        imm = ic['imm13']
        funct3 = ic['funct3']
        match funct3:
            case 0x00: # 000 BEQ
                InstructionSet().beq(rs1, rs2, imm)
            case 0x01: # 001 BNE
                InstructionSet().bne(rs1, rs2, imm)
            case 0x04: # 100 BLT
                InstructionSet().blt(rs1, rs2, imm)
            case 0x05: # 101 BGE
                InstructionSet().bge(rs1, rs2, imm)
            case 0x06: # 110 BLTU
                InstructionSet().bltu(rs1, rs2, imm)
            case 0x07: # 111 BGEU
                InstructionSet().bgeu(rs1, rs2, imm)
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
                InstructionSet().auipc(rd, imm)
            case 0x37: # 0110111 LUI
                InstructionSet().lui(rd, imm)

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
                InstructionSet().jal(rd, imm)
            case 0x67: # 1100111 JALR
                InstructionSet().jalr(rd, rs1, imm)
            case _:
                raise ValueError(f"opcode não reconhecido: {opcode}")
