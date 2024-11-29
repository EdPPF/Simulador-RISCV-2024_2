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

import numpy as np
class InstructionSet:
    """Conjunto de instruções RV32I."""
    def __init__(self, regs, memory): #pc, memory) -> None:
        self.xregs = regs
        """Banco de registradores. Definido em `cpu.py` como uma lista de inteiros de 32 bits sem sinal."""
        self.memory = memory
        """Memória do sistema. Definida em `memory.py` como um array de inteiros de 8 bits sem sinal."""

    def _gera_imm(self, ri):
        """Estende o sinal do imediato de 12 bits para 32 bits."""
        # imm = ri & 0xFFF               # Extrai os 12 bits menos significativos
        if ri & 0x800:                   # Se o bit de sinal (bit 11) estiver definido
            return np.int32(ri) | ~0xfff # Extensão de sinal
        return np.int32(ri)

    def _to_signed32(self, value: int):
        value = int(value) # Às vezes, trabalhar com numpy é bem chato
        value = value & 0xffffffff
        return (value ^ 0x80000000) - 0x80000000 # value | (-(value & 0x80000000))

    def _write_reg(self, rd, value):
        """Escreve o valor `value` no registrador `rd`, garantindo que `xregs[0]` seja sempre 0."""
        if rd != 0:
            self.xregs[rd] = value


    def lb(self, rd, rs1, imm):
        """*Load Byte*. Carrega um inteiro de 32 bits da memória."""
        imm = self._gera_imm(imm)
        address = self.xregs[rs1] + imm
        self._write_reg(
            rd,
            self.memory.lb(address)
        )

    def lbu(self, rd, rs1, imm):
        """*Load Byte Unsigned*. Carrega um inteiro de 32 bits sem sinal da memória."""
        imm = self._gera_imm(imm)
        address = self.xregs[rs1] + imm
        self._write_reg(
            rd,
            self.memory.lbu(address)
        )

    def lw(self, rd, rs1, imm):
        """*Load Word*. Carrega um inteiro de 32 bits da memória."""
        imm = self._gera_imm(imm)
        address = self.xregs[rs1] + imm
        if address < 0x2000:
            address += 0x2000 - 2 # 0x2000 é o endereço base do segmento .data
        self._write_reg(
            rd,
            self.memory.lw(address)
        )

    def sb(self, rs1, imm, rs2):
        """*Store Byte*. Armazena um byte na memória."""
        imm = self._gera_imm(imm)
        address = self.xregs[rs1] + imm
        self.memory.sb(address, self.xregs[rs2])

    def sw(self, rs1, imm, rs2):
        """*Store Word*. Armazena um inteiro de 32 bits na memória."""
        imm = self._gera_imm(imm)
        address = self.xregs[rs1] + imm
        self.memory.sw(address, self.xregs[rs2])


    def add(self, rd, rs1, rs2):
        """Adição de inteiros de 32 bits."""
        self._write_reg(
            rd,
            self.xregs[rs1] + self.xregs[rs2]
        )

    def addi(self, rd, rs1, imm):
        """*Add Immediate*. Adição de um inteiro de 32 bits com um imediato de 12 bits."""
        imm = self._gera_imm(imm)
        self._write_reg(
            rd,
            self.xregs[rs1] + imm
        )

    def and_(self, rd, rs1, rs2):
        """Operação lógica AND.\n O nome foi escolhido para evitar conflito com a palavra reservada `and`."""
        self._write_reg(
            rd,
            self.xregs[rs1] & self.xregs[rs2]
        )

    def andi(self, rd, rs1, imm):
        """*AND Immediate*. Operação lógica AND com um imediato de 12 bits."""
        imm = self._gera_imm(imm)
        self._write_reg(
            rd,
            self.xregs[rs1] & imm
        )

    def auipc(self, rd, imm, pc):
        """*Add Upper Immediate*. Adiciona o imediato de 20 bits ao PC e armazena o resultado em rd."""
        pc -= 4 # Retirando o +4 que o fetch() faz prematuramente
        imm = self._gera_imm(imm)
        imm = imm << 12
        self._write_reg(
            rd,
            pc + imm
        )


    def beq(self, rs1, rs2, imm, pc):
        """*Branch Equal*. Se rs1 == rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {hex(imm)} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        pc -= 4 if pc > 0 else 0 # Retirando o +4 que o fetch() faz prematuramente
        if self.xregs[rs1] == self.xregs[rs2]:
            pc += imm
        else:
            pc += 4
        return pc

    def bne(self, rs1, rs2, imm, pc):
        """*Branch Not Equal*. Se rs1 != rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {hex(imm)} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        pc -= 4 # Retirando o +4 que o fetch() faz prematuramente
        if self.xregs[rs1] != self.xregs[rs2]:
            pc += imm
        else:
            pc += 4
        return pc

    def bge(self, rs1, rs2, imm, pc):
        """*Branch Greater or Equal*. Se rs1 >= rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {hex(imm)} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        pc -= 4 # Retirando o +4 que o fetch() faz prematuramente
        rs1_val = self._to_signed32(self.xregs[rs1])
        rs2_val = self._to_signed32(self.xregs[rs2])
        if rs1_val >= rs2_val:
            pc += imm
        else:
            pc += 4
        return pc

    def bgeu(self, rs1, rs2, imm, pc):
        """*Branch Greater or Equal Unsigned*. Se rs1 >= rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {hex(imm)} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        pc -= 4 # Retirando o +4 que o fetch() faz prematuramente
        if self.xregs[rs1] >= self.xregs[rs2]:
            pc += imm
        else:
            pc += 4
        return pc

    def blt(self, rs1, rs2, imm, pc):
        """*Branch Less Than*. Se rs1 < rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {hex(imm)} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        pc -= 4 # Retirando o +4 que o fetch() faz prematuramente
        if self.xregs[rs1] < self.xregs[rs2]:
            pc += imm
        else:
            pc += 4
        return pc

    def bltu(self, rs1, rs2, imm, pc):
        """*Branch Less Than Unsigned*. Se rs1 < rs2, PC = PC + imm."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {hex(imm)} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        pc -= 4 # Retirando o +4 que o fetch() faz prematuramente
        if self.xregs[rs1] < self.xregs[rs2]:
            pc += imm
        else:
            pc += 4
        return pc

    def jal(self, rd, imm, pc):
        """*Jump and Link*. PC = PC + imm; rd = PC + 4."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {hex(imm)} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        pc -= 4                     # Retirando o +4 que o fetch() faz prematuramente
        self._write_reg(rd, pc + 4) # self.xregs[rd] = pc + 4
        pc += imm
        return pc

    def jalr(self, rd, rs1, imm, pc):
        """*Jump and Link Register*. PC = (x[rs1] + sext(imm[11:0])) & ~1; rd = PC + 4."""
        if imm % 4 != 0:
            raise ValueError(f"Endereço de destino {hex(imm)} não está alinhado em 4 bytes.")
        imm = self._gera_imm(imm)
        pc -= 4                            # Retirando o +4 que o fetch() faz prematuramente
        temp = pc + 4  # PC + 4
        pc = (self.xregs[rs1] + imm) & ~1  # (x[rs1] + sext(imm[11:0])) & ~1
        self._write_reg(rd, temp)
        return pc

    def or_(self, rd, rs1, rs2):
        """Operação lógica OR.\n O nome foi escolhido para evitar conflito com a palavra reservada `or`."""
        self._write_reg(
            rd,
            self.xregs[rs1] | self.xregs[rs2]
        )


    def lui(self, rd, imm):
        """*Load Upper Immediate*. Carrega o imediato de 20 bits nos 20 bits mais significativos de rd."""
        if imm not in range(0x00000, 0xfffff + 1):
            raise ValueError(f"Imediato {hex(imm)} fora do intervalo 0x00000..0xFFFFF")
        self._write_reg(
            rd,
            imm << 12
        )

    def slt(self, rd, rs1, rs2):
        """*Set Less Than*. rd = (rs1 < rs2) ? 1 : 0"""
        rs1_val = np.int32(self.xregs[rs1])
        rs2_val = np.int32(self.xregs[rs2])
        self._write_reg(
            rd,
            np.uint32(1 if rs1_val < rs2_val else 0)
        )

    def sltu(self, rd, rs1, rs2):
        """*Set Less Than Unsigned*. rd = (rs1 < rs2) ? 1 : 0"""
        rs1_val = np.uint32(self.xregs[rs1])
        rs2_val = np.uint32(self.xregs[rs2])
        self._write_reg(
            rd,
            np.uint32(1 if rs1_val < rs2_val else 0)
        )

    def ori(self, rd, rs1, imm):
        """*OR Immediate*. rd = rs1 | imm"""
        imm = self._gera_imm(imm)
        self._write_reg(
            rd,
            self.xregs[rs1] | imm
        )

    def slli(self, rd, rs1, imm):
        """*Shift Left Logical Immediate*. rd = rs1 << shamt"""
        shamt = imm & 0x1F
        self._write_reg(
            rd,
            self.xregs[rs1] << shamt
        )

    def srai(self, rd, rs1, imm):
        """*Shift Right Arithmetic Immediate*. rd = rs1 >> shamt"""
        shamt = imm & 0x1F
        self._write_reg(
            rd,
            np.int32(self.xregs[rs1]) >> shamt
        )

    def srli(self, rd, rs1, imm):
        """*Shift Right Logical Immediate*. rd = rs1 >> shamt"""
        shamt = imm & 0x1F
        self._write_reg(
            rd,
            self.xregs[rs1] >> shamt
        )

    def sub(self, rd, rs1, rs2):
        """Subtração de inteiros de 32 bits."""
        self._write_reg(
            rd,
            self.xregs[rs1] - self.xregs[rs2]
        )

    def xor(self, rd, rs1, rs2):
        """Operação lógica XOR."""
        self._write_reg(
            rd,
            self.xregs[rs1] ^ self.xregs[rs2]
        )

    def ecall(self):
        """Implementa as chamadas para
        - imprimir inteiro
        - imprimir string
        - encerrar programa"""
        a0 = self.xregs[10]          # Registrador a0
        syscall_num = self.xregs[17] # Registrador a7

        match syscall_num:
            case 1: # imprimir inteiro
                print(int(a0), end="")
            case 4: # imprimir string
                address = a0
                # Ajusta o endereço relativo com base no segmento de dados
                if address < self.memory.data_base:
                    address += self.memory.data_base - 2
                string = ""
                while self.memory.MEM[address] != 0:
                    string += chr(self.memory.MEM[address])
                    address += 1
                print(string, end="")
            case 10: # encerrar programa
                print("\nPrograma encerrado com sucesso.")
                exit(0)
            case _:
                raise ValueError(f"Syscall não reconhecida: {syscall_num}")
