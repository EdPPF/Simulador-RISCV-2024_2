from core.decoder import Decoder
import numpy as np
import pytest

class TestDecoder:
    """Testes para a classe Decoder."""
    dec = Decoder()

    def test_decode_r(self):
        """Testando instrução do tipo R"""
        instr = 0b00000000011100110000010100110011
        decoded = self.dec.decode(instr)
        assert decoded == {
            'opcode': 0b0110011,
            'funct7': 0,
            'rs2': 0b00111,
            'rs1': 0b00110,
            'funct3': 0b000,
            'rd': 0b01010,
            'ins_format': 'R_FORMAT',
        }

    def test_decode_i(self):
        """Testando instrução do tipo I"""
        instr = 0b00000000011000110100010100010011
        decoded = self.dec.decode(instr)
        assert decoded == {
            'opcode': 0b0010011,
            'funct7': 0,
            'imm12_i': 0b000000000110,
            'rs1': 0b00110,
            'funct3': 0b100,
            'rd': 0b01010,
            'ins_format': 'I_FORMAT',
        }

    def test_decode_s(self):
        """Testando instrução do tipo S"""
        instr = 0b00000000011101010010000100100011
        decoded = self.dec.decode(instr)
        assert decoded == {
            'opcode': 0b0100011,
            'imm12_s': 0b000000000010,
            'rs2': 0b00111,
            'rs1': 0b01010,
            'funct3': 0b010,
            'ins_format': 'S_FORMAT',
        }

    def test_decode_b(self):
        """Testando instrução do tipo B"""
        instr = 0b00000000110101100000001001100011
        decoded = self.dec.decode(instr)
        assert decoded == {
            'opcode': 0b1100011,
            'imm13': 0b0000000000100,
            'rs2': 0b01101,
            'rs1': 0b01100,
            'funct3': 0b000,
            'ins_format': 'B_FORMAT',
        }

    def test_decode_u(self):
        """Testando instrução do tipo U"""
        instr = 0b11111111111111111110010110010111
        decoded = self.dec.decode(instr)
        assert decoded == {
            'opcode': 0b0010111,
            'imm20_u': 0b11111111111111111110,
            'rd': 0b01011,
            'ins_format': 'U_FORMAT',
        }
        instr = 0b00000000000000000010010110010111
        decoded = self.dec.decode(instr)
        assert decoded == {
            'opcode': 0b0010111,
            'imm20_u': 0b00000000000000000010,
            'rd': 0b01011,
            'ins_format': 'U_FORMAT',
        }

    def test_decode_j(self):
        """Testando instrução do tipo J"""
        instr = 0b00000001100000000000010111101111
        decoded = self.dec.decode(instr)
        assert decoded == {
            'opcode': 0b1101111,
            'imm21': 0b00000000000000011000,
            'rd': 0b01011,
            'ins_format': 'J_FORMAT',
        }

    def test_decode_invalid(self):
        """Testando instrução inválida"""
        instr = 0b00000001100000000000010111101110
        with pytest.raises(ValueError):
            self.dec.decode(instr)
