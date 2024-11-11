from core.instruction_set import InstructionSet
import numpy as np

class TestInstructionSet:
    """Testes para o conjunto de instruções RV32I."""
    instructions = InstructionSet(np.zeros(32, dtype=np.uint32))

    def test_add(self):
        rd = 0
        rs1 = 1
        rs2 = 2
        self.instructions.xregs[rs1] = np.int32(0x00000001)
        self.instructions.xregs[rs2] = np.int32(0x00000002)
        self.instructions.add(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0x00000003

    def test_addi(self):
        rd = 0
        rs1 = 1
        imm = 0x002
        self.instructions.xregs[rs1] = np.int32(0x00000001)
        self.instructions.addi(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0x00000003

    def test_and(self):
        rd = 0
        rs1 = 1
        rs2 = 2
        self.instructions.xregs[rs1] = np.int32(0b10101010) # 0xAA
        self.instructions.xregs[rs2] = np.int32(0b11001100) # 0xCC
        self.instructions.and_(rd, rs1, rs2)
        assert self.instructions.xregs[rd] == 0b10001000

    def test_andi(self):
        rd = 0
        rs1 = 1
        imm = 0x002
        self.instructions.xregs[rs1] = np.int32(0b10101010) # 0xAA
        self.instructions.andi(rd, rs1, imm)
        assert self.instructions.xregs[rd] == 0b00000010

    def test_auipc(self):
        rd = 0
        imm = 0x002
        self.instructions.auipc(rd, imm)
        assert self.instructions.xregs[rd] == 0x00000002
