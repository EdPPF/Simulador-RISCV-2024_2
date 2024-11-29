from core.instruction_set import InstructionSet
import numpy as np
import pytest
# Imports para capturar a impressão de string e int
from io import StringIO
import sys

class MemoryMock:
    """Mock para a memória."""
    def __init__(self) -> None:
        self.MEM = np.zeros(16384, dtype=np.uint8)
        self.text_base = 0x0000  # Endereço base do segmento .text
        self.data_base = 0x2000  # Endereço base do segmento .data


class TestInstructionSet:
    """Testes para o conjunto de instruções RV32I."""
    memory = MemoryMock()
    instructions = InstructionSet(np.zeros(32, dtype=np.uint32), memory)

    def test_add(self):
        rd = 10
        rs1 = 1
        rs2 = 2
        self.instructions.xregs[rs1] = np.int32(0x00000001)
        self.instructions.xregs[rs2] = np.int32(0x00000002)
        self.instructions.add(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0x00000003

    def test_addi(self):
        rd = 10
        rs1 = 1
        imm = 0x002
        self.instructions.xregs[rs1] = np.int32(0x00000001)
        self.instructions.addi(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0x00000003

    def test_and(self):
        rd = 10
        rs1 = 1
        rs2 = 2
        self.instructions.xregs[rs1] = np.int32(0b10101010) # 0xAA
        self.instructions.xregs[rs2] = np.int32(0b11001100) # 0xCC
        self.instructions.and_(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0b10001000

    def test_andi(self):
        rd = 10
        rs1 = 1
        imm = 0x002
        self.instructions.xregs[rs1] = np.int32(0b10101010) # 0xAA
        self.instructions.andi(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0b00000010

    def test_auipc(self):
        rd = 10
        imm = 0x002
        self.instructions.auipc(rd, imm, 0x00000004)
        assert self.instructions.xregs[rd] == 0x00002000

    def test_beq(self):
        rs1  = 1
        rs2  = 2
        imm = 0x008
        pc = np.uint32(0)
        pc += 4 # Levando em conta a função fetch()
        self.instructions.xregs[rs1] = np.int32(0x00000001)
        # Se rs1 == rs2, PC = PC + imm
        self.instructions.xregs[rs2] = np.int32(0x00000001)
        pc = self.instructions.beq(rs1, rs2, imm, pc)
        assert pc == 0x00000008
        pc = np.uint32(0) + 4
        # Se rs1 != rs2, PC = PC + 4
        self.instructions.xregs[rs2] = np.int32(0x00000003)
        pc = self.instructions.beq(rs1, rs2, imm, pc)
        assert pc == 0x00000004
        # Imm não alinhado em 4 bytes
        imm = 0x003
        with pytest.raises(ValueError):
            pc = self.instructions.beq(rs1, rs2, imm, pc)
        pc = np.uint32(0)

    def test_bne(self):
        rs1  = 1
        rs2  = 2
        imm = 0x008
        pc = np.uint32(0)
        pc += 4 # Levando em conta a função fetch()
        self.instructions.xregs[rs1] = np.int32(0x00000001)
        # Se rs1 != rs2, PC = PC + imm
        self.instructions.xregs[rs2] = np.int32(0x00000003)
        pc = self.instructions.bne(rs1, rs2, imm, pc)
        assert pc == 0x00000008
        pc = np.uint32(0) + 4
        # Se rs1 == rs2, PC = PC + 4
        self.instructions.xregs[rs2] = np.int32(0x00000001)
        pc = self.instructions.bne(rs1, rs2, imm, pc)
        assert pc == 0x00000004
        imm = 0x003
        with pytest.raises(ValueError):
            pc = self.instructions.bne(rs1, rs2, imm, pc)
        pc = np.uint32(0)

    def test_bge(self):
        rs1  = 1
        rs2  = 2
        imm = 0x008
        pc = np.uint32(0)
        pc += 4
        self.instructions.xregs[rs1] = np.int32(0x00000003)
        self.instructions.xregs[rs2] = np.int32(0x00000001)
        # Se rs1 >= rs2, PC = PC + imm
        pc = self.instructions.bge(rs1, rs2, imm, pc)
        assert pc == 0x00000008
        pc = np.uint32(0) + 4
        # Se rs1 < rs2, PC = PC + 4
        self.instructions.xregs[rs2] = np.int32(0x00000004)
        pc = self.instructions.bge(rs1, rs2, imm, pc)
        assert pc == 0x00000004
        imm = 0x003
        with pytest.raises(ValueError):
            pc = self.instructions.bge(rs1, rs2, imm, pc)
        pc = np.uint32(0)

    def test_bgeu(self):
        rs1  = 1
        rs2  = 2
        imm = 0x008
        pc = np.uint32(0)
        pc += 4
        self.instructions.xregs[rs1] = np.uint32(0x00000003)
        self.instructions.xregs[rs2] = np.uint32(0x00000001)
        # Se rs1 >= rs2, PC = PC + imm
        pc = self.instructions.bgeu(rs1, rs2, imm, pc)
        assert pc == 0x00000008
        pc = np.uint32(0) + 4
        # Se rs1 < rs2, PC = PC + 4
        self.instructions.xregs[rs2] = np.uint32(0x00000004)
        pc = self.instructions.bgeu(rs1, rs2, imm, pc)
        assert pc == 0x00000004
        imm = 0x003
        with pytest.raises(ValueError):
            pc = self.instructions.bgeu(rs1, rs2, imm, pc)
        pc = np.uint32(0)

    def test_blt(self):
        rs1  = 1
        rs2  = 2
        imm = 0x008
        pc = np.uint32(0)
        pc += 4
        self.instructions.xregs[rs1] = np.int32(0x00000001)
        self.instructions.xregs[rs2] = np.int32(0x00000003)
        # Se rs1 < rs2, PC = PC + imm
        pc = self.instructions.blt(rs1, rs2, imm, pc)
        assert pc == 0x00000008
        pc = np.uint32(0) + 4
        # Se rs1 >= rs2, PC = PC + 4
        self.instructions.xregs[rs2] = np.int32(0x00000001)
        pc = self.instructions.blt(rs1, rs2, imm, pc)
        assert pc == 0x00000004
        imm = 0x003
        with pytest.raises(ValueError):
            pc = self.instructions.blt(rs1, rs2, imm, pc)
        pc = np.uint32(0)

    def test_bltu(self):
        rs1  = 1
        rs2  = 2
        imm = 0x008
        pc = np.uint32(0)
        pc += 4
        self.instructions.xregs[rs1] = np.uint32(0x00000001)
        self.instructions.xregs[rs2] = np.uint32(0x00000003)
        # Se rs1 < rs2, PC = PC + imm
        pc = self.instructions.bltu(rs1, rs2, imm, pc)
        assert pc == 0x00000008
        pc = np.uint32(0) + 4
        # Se rs1 >= rs2, PC = PC + 4
        self.instructions.xregs[rs2] = np.uint32(0x00000001)
        pc = self.instructions.bltu(rs1, rs2, imm, pc)
        assert pc == 0x00000004
        imm = 0x003
        with pytest.raises(ValueError):
            pc = self.instructions.bltu(rs1, rs2, imm, pc)
        pc = np.uint32(0)

    def test_jal(self):
        rd = 1
        imm = 0x008
        pc = np.uint32(0)
        pc += 4
        pc = self.instructions.jal(rd, imm, pc)
        assert self.instructions.xregs[rd] == 0x00000004 # PC + 4 == 0x00000000 + 4
        assert pc == 0x00000008
        pc = np.uint32(0)
        imm = 0x003
        with pytest.raises(ValueError):
            pc = self.instructions.jal(rd, imm, pc)

    def test_jalr(self):
        rd = 1
        rs1 = 2
        imm = 0x008
        pc = np.uint32(0)
        pc += 4
        self.instructions.xregs[rs1] = np.uint32(0x00000001)
        pc = self.instructions.jalr(rd, rs1, imm, pc)
        assert self.instructions.xregs[rd] == 0x00000004
        assert pc == 0x00000008
        pc = np.uint32(0)
        imm = 0x003
        with pytest.raises(ValueError):
            pc = self.instructions.jalr(rd, rs1, imm, pc)

    def test_or(self):
        rd = 1
        rs1 = 2
        rs2 = 3
        self.instructions.xregs[rs1] = np.uint32(0x10101010)
        self.instructions.xregs[rs2] = np.uint32(0x11001100)
        self.instructions.or_(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0x11101110
        self.instructions.xregs[rs1] = np.uint32(0xc0ffe111)
        self.instructions.xregs[rs2] = np.uint32(0xdefecada)
        self.instructions.or_(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0xdeffebdb

    def test_lui(self):
        rd = 1
        imm = 0x001
        self.instructions.lui(rd, imm)
        assert self.instructions.xregs[rd] == 0x00001000
        imm = 0x003
        self.instructions.lui(rd, imm)
        assert self.instructions.xregs[rd] == 0x00003000
        imm = 0x100
        self.instructions.lui(rd, imm)
        assert self.instructions.xregs[rd] == 0x00100000
        imm = -1
        with pytest.raises(ValueError):
            self.instructions.lui(rd, imm)

    def test_slt(self):
        rd = 1
        rs1 = 2
        rs2 = 3
        # Teste com valores positivos
        self.instructions.xregs[rs1] = np.uint32(1)
        self.instructions.xregs[rs2] = np.uint32(2)
        self.instructions.slt(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 1
        # Teste com valores iguais
        self.instructions.xregs[rs2] = np.uint32(1)
        self.instructions.slt(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0
        # Teste com valores negativos
        self.instructions.xregs[rs1] = np.uint32(-1 & 0xFFFFFFFF)  # Armazena -1 como uint32
        self.instructions.xregs[rs2] = np.uint32(-2 & 0xFFFFFFFF)  # Armazena -2 como uint32
        self.instructions.slt(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0
        # Teste com rs1 negativo e rs2 positivo
        self.instructions.xregs[rs1] = np.uint32(-2 & 0xFFFFFFFF)  # Armazena -2 como uint32
        self.instructions.xregs[rs2] = 1
        self.instructions.slt(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 1

    def test_sltu(self):
        rd = 1
        rs1 = 2
        rs2 = 3
        self.instructions.xregs[rs1] = np.uint32(1)
        self.instructions.xregs[rs2] = np.uint32(2)
        self.instructions.sltu(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 1
        self.instructions.xregs[rs2] = np.uint32(1)
        self.instructions.sltu(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0

    def test_ori(self):
        rd = 1
        rs1 = 2
        imm = 0x001
        self.instructions.xregs[rs1] = np.uint32(0x10101010)
        self.instructions.ori(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0x10101011
        imm = 0x00f
        self.instructions.ori(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0x1010101f
        imm = 0x100
        self.instructions.ori(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0x10101110

    def test_slli(self):
        rd = 1
        rs1 = 2
        imm = 0x001
        self.instructions.xregs[rs1] = np.uint32(0x10101010)
        self.instructions.slli(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0x20202020

    def test_srai(self):
        rd = 1
        rs1 = 2
        imm = 0x002
        self.instructions.xregs[rs1] = np.uint32(0x0000002a)
        self.instructions.srai(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0x0000000a
        self.instructions.xregs[rs1] = np.uint32(0xffffffd6)
        self.instructions.srai(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0xfffffff5

    def test_srli(self):
        rd = 1
        rs1 = 2
        imm = 0x002
        self.instructions.xregs[rs1] = np.uint32(0x0000002a)
        self.instructions.srli(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0x0000000a
        self.instructions.xregs[rs1] = np.uint32(0xffffffd6)
        self.instructions.srli(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0x3ffffff5

    def test_sub(self):
        rd = 1
        rs1 = 2
        rs2 = 3
        self.instructions.xregs[rs1] = np.uint32(0x00000003)
        self.instructions.xregs[rs2] = np.uint32(0x00000001)
        self.instructions.sub(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0x00000002
        self.instructions.xregs[rs1] = np.uint32(0x00000001)
        self.instructions.sub(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0x00000000

    def test_xor(self):
        rd = 1
        rs1 = 2
        rs2 = 3
        self.instructions.xregs[rs1] = np.uint32(0x10101010)
        self.instructions.xregs[rs2] = np.uint32(0x11001100)
        self.instructions.xor(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0x01100110
        self.instructions.xregs[rs1] = np.uint32(0xc0ffe111)
        self.instructions.xregs[rs2] = np.uint32(0xdefecada)
        self.instructions.xor(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0x1e012bcb

    def test_ecall(self):
        # Imprimir inteiro
        self.instructions.xregs[10] = np.uint32(0x00010f2c)
        self.instructions.xregs[17] = np.uint32(0x00000001)
        captured_output = StringIO()
        sys.stdout = captured_output
        self.instructions.ecall()
        sys.stdout = sys.__stdout__
        assert captured_output.getvalue() == "69420"

        # Imprimir string
        string = "OAC 2024.2"
        self.instructions.xregs[10] = np.uint32(0x00002001)
        a0 = self.instructions.xregs[10]
        for i in range(len(string)):
            self.instructions.memory.MEM[a0 + i] = np.uint8(ord(string[i]))
        self.instructions.memory.MEM[a0 + len(string)] = 0 # null terminated
        self.instructions.xregs[17] = np.uint32(0x00000004)
        captured_output = StringIO()
        sys.stdout = captured_output
        self.instructions.ecall()
        sys.stdout = sys.__stdout__
        assert captured_output.getvalue() == string

        # Encerrar programa
        self.instructions.xregs[17] = np.uint32(0x0000000a)
        with pytest.raises(SystemExit):
            self.instructions.ecall()

        # Teste exceção
        self.instructions.xregs[17] = np.uint32(0x0000000b)
        with pytest.raises(ValueError):
            self.instructions.ecall()
