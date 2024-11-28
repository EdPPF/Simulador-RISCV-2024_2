from core.cpu import CPU
import numpy as np
import pytest

class MemoryMock:
    """Mock para a memória."""
    def __init__(self) -> None:
        self.MEM = np.zeros(16384, dtype=np.uint8)
        self.text_base = 0x0000  # Endereço base do segmento .text
        self.data_base = 0x2000  # Endereço base do segmento .data

    def lw(self, address):#rd: int, kte: int):
        '''Lê uma palavra de 32 bits da memória e retorna o seu valor.'''
        # address = rd + kte
        if address != 0x2000 and address % 4 != 0:
            raise ValueError(f"Endereço {hex(address)} não retorna um múltiplo de 4.")

        byte0 = np.uint32(self.MEM[address+0])
        byte1 = np.uint32(self.MEM[address+1])
        byte2 = np.uint32(self.MEM[address+2])
        byte3 = np.uint32(self.MEM[address+3])
        word = (byte3 << 24) | (byte2 << 16) | (byte1 << 8) | byte0
        return (word)

    def sw(self, address, word):
        pass


class DecoderMock:
    """Mock para o decodificador."""
    def decode(self, instruction):
        if instruction == 0x730533:
            return {
                'opcode': 0b0110011,
                'funct7': 0,
                'rs2': 0b00111,
                'rs1': 0b00110,
                'funct3': 0b000,
                'rd': 0b01010,
                'ins_format': 'R_FORMAT',
            }
        elif instruction == 0x636513:
            return {
                'opcode': 0b0010011,
                'funct7': 0,
                'imm12_i': 0b000000000110,
                'rs1': 0b00110,
                'funct3': 0b110,
                'rd': 0b01010,
                'ins_format': 'I_FORMAT',
            }
        elif instruction == 0x752123:
            return {
                'opcode': 0b0100011,
                'imm12_s': 0b000000000010,
                'rs2': 0b00111,
                'rs1': 0b01010,
                'funct3': 0b010,
                'ins_format': 'S_FORMAT',
            }
        elif instruction == 0xd60263:
            return {
                'opcode': 0b1100011,
                'imm13': 0b0000000000100,
                'rs2': 0b01101,
                'rs1': 0b01100,
                'funct3': 0b000,
                'ins_format': 'B_FORMAT',
            }
        elif instruction == 0xffffe597:
            return {
                'opcode': 0b0010111,
                'imm20_u': 0b11111111111111111110,
                'rd': 0b01011,
                'ins_format': 'U_FORMAT',
            }
        elif instruction == 0x18005ef:
            return {
                'opcode': 0b1101111,
                'imm21': 0b00000000000000011000,
                'rs1': 0b00101,
                'rd': 0b01011,
                'ins_format': 'J_FORMAT',
            }
        else:
            return {
                'opcode': 0,
                'funct7': 0,
                'rs2': 0,
                'rs1': 0,
                'funct3': 0,
                'rd': 0,
                'ins_format': 'INVALID',
            }


class InstructionSetMock:
    def __init__(self, xregs, pc, memory) -> None:
        self.xregs = xregs
        self.pc = pc
        self.memory = memory

    def addi(self):
        pass

    def add(self):
        pass

    def and_(self):
        pass

    def andi(self):
        pass

    def auipc(self):
        pass

    def beq(self):
        pass

    def bne(self):
        pass

    def bge(self):
        pass

    def bgeu(self):
        pass

    def blt(self):
        pass

    def bltu(self):
        pass

    def jal(self):
        pass

    def jalr(self):
        pass

    def or_(self):
        pass

    def lui(self):
        pass

    def slt(self):
        pass

    def sltu(self):
        pass

    def ori(self):
        pass

    def slli(self):
        pass

    def srai(self):
        pass

    def srli(self):
        pass

    def sub(self):
        pass

    def xor(self):
        pass

    def ecall(self):
        pass


class ExecutorMock:
    # xregs = xregs
    # memory = memory
    # pc = pc

    def execute(self):
        pass

class TestCPU():
    code_path = "src/tests/files/test4-1_text.txt"
    data_path = "src/tests/files/test4-1_data.txt"
    CPU = CPU(code_path, data_path)

    def test_init(self):
        assert self.CPU.PC == np.uint32(0)
        assert self.CPU.xregs.all() == np.zeros(32, dtype=np.uint32).all()
        assert self.CPU.memory.MEM.all() == np.zeros(16384, dtype=np.uint8).all()
