"""
Conjunto de instruções RV32I\n
Instruções implementadas:\n
    ```
    add, addi, and, andi, auipc,
    beq, bne, bge, bgeu, blt,
    bltu, jal, jalr, lb, or,
    lbu, lw, lui, slt, sltu,
    ori, sb, slli, srai, srli,
    sub, sw, xor, ecall
    ```
Syscall:
- imprimir inteiro
- imprimir string
- encerrar programa
"""

"""
! Diferente do projeto do CPeluti, onde os parâmetros das instruções são `i32`, e o banco de regs é passado
! apenas na chamada da instrução, aqui estou acessando o banco diretamente nas funções de instrução.
"""

import numpy as np
class InstructionSet:
    """Conjunto de instruções RV32I."""
    def __init__(self, regs) -> None:
        self.xregs = regs

    def _gera_imm(self, ri):
        '''Estende o sinal do imediato de 12 bits para 32 bits.'''
        imm = np.uint32(ri) >> 20
        if imm & 0x800:
            imm = imm | 0xFFFFF000
        return imm

    def add(self, rd, rs1, rs2):
        """Adição de inteiros de 32 bits."""
        self.xregs[rd] = self.xregs[rs1] + self.xregs[rs2]

    def addi(self, rd, rs1, imm):
        """*Add Immediate*. Adição de um inteiro de 32 bits com um imediato de 12 bits."""
        imm = self._gera_imm(imm)
        self.xregs[rd] = self.xregs[rs1] + imm

    def sand(self, rd, rs1, rs2):
        """Operação lógica AND.\n O nome sand foi escolhido para evitar conflito com a palavra reservada and."""
        self.xregs[rd] = self.xregs[rs1] & self.xregs[rs2]

    def andi(self, rd, rs1, imm):
        """*AND Immediate*. Operação lógica AND com um imediato de 12 bits."""
        imm = self._gera_imm(imm)
        self.xregs[rd] = self.xregs[rs1] & imm

    def auipc(self, rd, imm):
        """*Add Upper Immediate*. Adiciona o imediato de 20 bits ao PC e armazena o resultado em rd."""
        imm = imm << 12
        self.xregs[rd] = self.xregs[32] + imm # PC = xregs[32]


    def beq(self, rs1, rs2, imm):
        """*Branch Equal*. Se rs1 == rs2, PC = PC + imm."""
        imm = self._gera_imm(imm)
        if self.xregs[rs1] == self.xregs[rs2]:
            self.xregs[32] = self.xregs[32] + imm
        else:
            self.xregs[32] = self.xregs[32] + 4

    def bne(self, rs1, rs2, imm):
        """*Branch Not Equal*. Se rs1 != rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {imm} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        if self.xregs[rs1] != self.xregs[rs2]:
            self.xregs[32] = self.xregs[32] + imm
        else:
            self.xregs[32] = self.xregs[32] + 4

    def bge(self, rs1, rs2, imm):
        """*Branch Greater or Equal*. Se rs1 >= rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {imm} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        # Conversão para signed int32. Necessário?
        # rs1_val = np.int32(self.xregs[rs1])
        # rs2_val = np.int32(self.xregs[rs2])
        if self.xregs[rs1] >= self.xregs[rs2]:
            self.xregs[32] = self.xregs[32] + imm
        else:
            self.xregs[32] = self.xregs[32] + 4

    def bgeu(self, rs1, rs2, imm):
        """*Branch Greater or Equal Unsigned*. Se rs1 >= rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {imm} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        # Conversão para unsigned int32. Necessário?
        # rs1_val = np.uint32(self.xregs[rs1])
        # rs2_val = np.uint32(self.xregs[rs2])
        if self.xregs[rs1] >= self.xregs[rs2]:
            self.xregs[32] = self.xregs[32] + imm
        else:
            self.xregs[32] = self.xregs[32] + 4

    def blt(self, rs1, rs2, imm):
        """*Branch Less Than*. Se rs1 < rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {imm} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        # Conversão para signed int32. Necessário?
        # rs1_val = np.int32(self.xregs[rs1])
        # rs2_val = np.int32(self.xregs[rs2])
        if self.xregs[rs1] < self.xregs[rs2]:
            self.xregs[32] = self.xregs[32] + imm
        else:
            self.xregs[32] = self.xregs[32] + 4

    def bltu(self, rs1, rs2, imm):
        """*Branch Less Than Unsigned*. Se rs1 < rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {imm} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        # Conversão para unsigned int32. Necessário?
        # rs1_val = np.uint32(self.xregs[rs1])
        # rs2_val = np.uint32(self.xregs[rs2])
        if self.xregs[rs1] < self.xregs[rs2]:
            self.xregs[32] = self.xregs[32] + imm
        else:
            self.xregs[32] = self.xregs[32] + 4

    def jal(self, rd, imm):
        """*Jump and Link*. PC = PC + imm; rd = PC + 4."""
        imm = self._gera_imm(imm)
        self.xregs[rd] = self.xregs[32] + 4
        self.xregs[32] = self.xregs[32] + imm

    def jalr(self, rd, rs1, imm):
        """*Jump and Link Register*. PC = (x[rs1] + sext(imm[11:0])) & ~1; rd = PC + 4."""
        imm = self._gera_imm(imm)
        temp = self.xregs[32] + 4  # PC + 4
        self.xregs[32] = (self.xregs[rs1] + imm) & ~1  # (x[rs1] + sext(imm[11:0])) & ~1
        self.xregs[rd] = temp  # x[rd] = t

    def sor(self, rd, rs1, rs2):
        """Operação lógica OR.\n O nome sor foi escolhido para evitar conflito com a palavra reservada or."""
        self.xregs[rd] = self.xregs[rs1] | self.xregs[rs2]


    def lui(self, rd, imm):
        """*Load Upper Immediate*. Carrega o imediato de 20 bits nos 12 bits mais significativos de rd."""
        imm = imm << 12
        self.xregs[rd] = imm

    def slt(self, rd, rs1, rs2):
        """*Set Less Than*. rd = (rs1 < rs2) ? 1 : 0"""
        # Conversão para signed int32. Necessário?
        # rs1_val = np.int32(self.xregs[rs1])
        # rs2_val = np.int32(self.xregs[rs2])
        self.xregs[rd] = 1 if self.xregs[rs1] < self.xregs[rs2] else 0

    def sltu(self, rd, rs1, rs2):
        """*Set Less Than Unsigned*. rd = (rs1 < rs2) ? 1 : 0"""
        # Conversão para unsigned int32. Necessário?
        # rs1_val = np.uint32(self.xregs[rs1])
        # rs2_val = np.uint32(self.xregs[rs2])
        self.xregs[rd] = 1 if self.xregs[rs1] < self.xregs[rs2] else 0

    def ori(self, rd, rs1, imm):
        """*OR Immediate*. rd = rs1 | imm"""
        imm = self._gera_imm(imm)
        self.xregs[rd] = self.xregs[rs1] | imm

    def slli(self, rd, rs1, imm):
        """*Shift Left Logical Immediate*. rd = rs1 << shamt"""
        shamt = imm & 0x1F
        self.xregs[rd] = self.xregs[rs1] << shamt

    def srai(self, rd, rs1, imm):
        """*Shift Right Arithmetic Immediate*. rd = rs1 >> shamt"""
        shamt = imm & 0x1F
        self.xregs[rd] = np.int32(self.xregs[rs1]) >> shamt

    def srli(self, rd, rs1, imm):
        """*Shift Right Logical Immediate*. rd = rs1 >> shamt"""
        shamt = imm & 0x1F
        self.xregs[rd] = self.xregs[rs1] >> shamt

    def sub(self, rd, rs1, rs2):
        """Subtração de inteiros de 32 bits."""
        self.xregs[rd] = self.xregs[rs1] - self.xregs[rs2]

    def xor(self, rd, rs1, rs2):
        """Operação lógica XOR."""
        self.xregs[rd] = self.xregs[rs1] ^ self.xregs[rs2]

    def ecall(self):
        """Implementa as chamadas para
        - imprimir inteiro
        - imprimir string
        - encerrar programa"""
        # imprimir inteiro. xregs[17] é o registrador a7
        if self.xregs[17] == 1:
            print(self.xregs[10])
        # imprimir string:
        elif self.xregs[17] == 4:
            address = self.xregs[10]
            while True:
                byte = self.xregs[0].MEM[address] # self.xregs[0] é o objeto Memory???
                if byte == 0:
                    break
                print(chr(byte), end='')
                address += 1
        # encerrar programa:
        elif self.xregs[17] == 10:
            exit(0)
