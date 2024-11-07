from core.memory import Memory
import pytest

class TestMemory:
    """Módulo de testes para a classe Memory."""

    def test_init(self):
        mem = Memory()
        assert len(mem.MEM) == 16384
        assert mem.MEM[0] == 0

    def test_sb(self):
        mem = Memory()
        mem.sb(0, 0, 0b11111010) # 0xFA
        mem.sb(0, 4, 0b11001010) # 0xCA
        assert mem.MEM[0] == 0xFA
        assert mem.MEM[4] == 0xCA

    def test_sw(self):
        mem = Memory()
        mem.sw(0, 0, 0b11111010110010101100101011111110) # 0xFACACAFE
        assert mem.MEM[0] == 0xFE
        assert mem.MEM[1] == 0xCA
        assert mem.MEM[2] == 0xCA
        assert mem.MEM[3] == 0xFA
        # Endereço inválido:
        with pytest.raises(ValueError):
            mem.sw(1, 0, 0b11111010110010101100101011111110)

    def test_lb(self):
        mem = Memory()
        mem.sb(0, 0, 0b11101101) # 0xED
        assert mem.lb(0, 0) == '0xffffffed'

    def test_lbu(self):
        mem = Memory()
        mem.sb(0, 0, 0b11101101)
        assert mem.lbu(0, 0) == '0xed'

    def test_lw(self):
        mem = Memory()
        mem.sw(0, 0, 0b11011110111111101100101011011010) # 0xDEFECADA
        assert mem.lw(0, 0) == '0xdefecada'
        # Endereço inválido:
        with pytest.raises(ValueError):
            mem.lw(1, 0)

    def test_load_mem(self):
        pass
        # mem = Memory()
        # mem.load_mem('tests/test_mem.txt')
