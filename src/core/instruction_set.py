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
! Diferente de outro projeto, onde os parâmetros das instruções são `i32`, e o banco de regs é passado
! apenas na chamada da instrução, aqui estou acessando o banco diretamente nas funções de instrução.
"""

import numpy as np
class InstructionSet:
    """Conjunto de instruções RV32I."""
    def __init__(self, regs, pc) -> None:
        self.xregs = regs
        """Banco de registradores. Definido em `cpu.py` como uma lista de inteiros de 32 bits sem sinal."""
        self.pc = pc
        """Program Counter. Definido em `cpu.py` como um inteiro de 32 bits sem sinal."""

    def _gera_imm(self, ri):
        """Estende o sinal do imediato de 12 bits para 32 bits."""
        imm = ri & 0xFFF           # Extrai os 12 bits menos significativos
        if imm & 0x800:            # Se o bit de sinal (bit 11) estiver definido
            imm |=  0xFFFFF000 # Extensão de sinal
        return np.uint32(imm)

    def add(self, rd, rs1, rs2):
        """Adição de inteiros de 32 bits."""
        self.xregs[rd] = self.xregs[rs1] + self.xregs[rs2]

    def addi(self, rd, rs1, imm):
        """*Add Immediate*. Adição de um inteiro de 32 bits com um imediato de 12 bits."""
        imm = self._gera_imm(imm)
        self.xregs[rd] = self.xregs[rs1] + imm

    def and_(self, rd, rs1, rs2):
        """Operação lógica AND.\n O nome foi escolhido para evitar conflito com a palavra reservada and."""
        self.xregs[rd] = self.xregs[rs1] & self.xregs[rs2]

    def andi(self, rd, rs1, imm):
        """*AND Immediate*. Operação lógica AND com um imediato de 12 bits."""
        imm = self._gera_imm(imm)
        self.xregs[rd] = self.xregs[rs1] & imm

    def auipc(self, rd, imm):
        """*Add Upper Immediate*. Adiciona o imediato de 20 bits ao PC e armazena o resultado em rd."""
        # imm = imm << 12
        imm = self._gera_imm(imm)
        self.xregs[rd] = self.pc + imm


    def beq(self, rs1, rs2, imm):
        """*Branch Equal*. Se rs1 == rs2, PC = PC + imm."""
        imm = self._gera_imm(imm)
        if self.xregs[rs1] == self.xregs[rs2]:
            self.pc += imm
        else:
            self.pc += 4

    def bne(self, rs1, rs2, imm):
        """*Branch Not Equal*. Se rs1 != rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {imm} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        if self.xregs[rs1] != self.xregs[rs2]:
            self.pc += imm
        else:
            self.pc += 4

    def bge(self, rs1, rs2, imm):
        """*Branch Greater or Equal*. Se rs1 >= rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {imm} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        # Conversão para signed int32. Necessário?
        # rs1_val = np.int32(self.xregs[rs1])
        # rs2_val = np.int32(self.xregs[rs2])
        if self.xregs[rs1] >= self.xregs[rs2]:
            self.pc += imm
        else:
            self.pc += 4

    def bgeu(self, rs1, rs2, imm):
        """*Branch Greater or Equal Unsigned*. Se rs1 >= rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {imm} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        # Conversão para unsigned int32. Necessário?
        # rs1_val = np.uint32(self.xregs[rs1])
        # rs2_val = np.uint32(self.xregs[rs2])
        if self.xregs[rs1] >= self.xregs[rs2]:
            self.pc += imm
        else:
            self.pc += 4

    def blt(self, rs1, rs2, imm):
        """*Branch Less Than*. Se rs1 < rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {imm} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        # Conversão para signed int32. Necessário?
        # rs1_val = np.int32(self.xregs[rs1])
        # rs2_val = np.int32(self.xregs[rs2])
        if self.xregs[rs1] < self.xregs[rs2]:
            self.pc += imm
        else:
            self.pc += 4

    def bltu(self, rs1, rs2, imm):
        """*Branch Less Than Unsigned*. Se rs1 < rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {imm} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        # Conversão para unsigned int32. Necessário?
        # rs1_val = np.uint32(self.xregs[rs1])
        # rs2_val = np.uint32(self.xregs[rs2])
        if self.xregs[rs1] < self.xregs[rs2]:
            self.pc += imm
        else:
            self.pc += 4

    def jal(self, rd, imm):
        """*Jump and Link*. PC = PC + imm; rd = PC + 4."""
        imm = self._gera_imm(imm)
        self.xregs[rd] = self.pc + 4
        self.pc += imm

    def jalr(self, rd, rs1, imm):
        """*Jump and Link Register*. PC = (x[rs1] + sext(imm[11:0])) & ~1; rd = PC + 4."""
        imm = self._gera_imm(imm)
        temp = self.pc + 4  # PC + 4
        self.pc = (self.xregs[rs1] + imm) & ~1  # (x[rs1] + sext(imm[11:0])) & ~1
        self.xregs[rd] = temp  # x[rd] = t

    def or_(self, rd, rs1, rs2):
        """Operação lógica OR.\n O nome sor foi escolhido para evitar conflito com a palavra reservada `or`."""
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
        a0 = self.xregs[10]          # Registrador a0
        syscall_num = self.xregs[17] # Registrador a7

        match syscall_num:
            case 1: # imprimir inteiro
                print(a0)
            case 4: # imprimir string
                address = a0
                string = ""
                while self.memory.MEM[address] != 0:
                    string += chr(self.memory.MEM[address])
                    address += 1
                print(string)
            case 10: # encerrar programa
                print("Programa encerrado com sucesso.\n  Código de saída: 0")
                exit(0)
            case _:
                raise ValueError(f"Syscall não reconhecida: {syscall_num}")
