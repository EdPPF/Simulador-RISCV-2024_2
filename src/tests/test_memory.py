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
        # Valores de memória gerados pelo montador RARS para o programa específico sendo testado:
        text_values = [
            0x00002297, # auipc x5, 2
            0x00028293, # addi x5, x5, 0
            0x00002317, # auipc x6, 2
            0x01830313, # addi x6, x6, 24
            0x00032303, # lw x6, 0(x6)
            0x00400893, # addi x17, x0, 4
            0x00002517, # auipc x10, 2
            0x00c50513, # addi x10, x10, 12
            0x00000073, # ecall
            0x02030663, # beq x6, x0, 0x0000002c
            0x00100893, # addi x17, x0, 1
            0x0002a503, # lw x10, 0(x5)
            0x00000073, # ecall
            0x00400893, # addi x17, x0, 4
            0x00002517, # auipc x10, 2
            0x01450513, # addi x10, x10, 20
            0x00000073, # ecall
            0x00428293, # addi x10, x10, 4
            0xfff30313, # addi x6, x6, 0xffffffff
            0xfd9ff06f, # jal x0, 0xffffffd8
            0x00a00893, # addi x17, x0, 10
            0x00000073, # ecall
        ]

        data_values = [
            0x00000001, 0x00000003, 0x00000005, 0x00000007, 0x0000000b, 0x0000000d, 0x00000011, 0x00000013, # 0x2000 - 0x201c
            0x00000008, 0x6f20734f, 0x206f7469, 0x6d697270, 0x6f726965, 0x756e2073, 0x6f72656d, 0x72702073, # 0x2020 - 0x203c
            0x736f6d69, 0x6f617320, 0x00203a20, 0x00000020, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x2040 - 0x205c
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x2060 - 0x207c
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x2080 - 0x209c
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x20a0 - 0x20bc
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x20c0 - 0x20dc
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x20e0 - 0x20fc
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x2100 - 0x211c
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x2120 - 0x213c
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x2140 - 0x215c
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x2160 - 0x217c
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x2180 - 0x219c
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x21a0 - 0x21bc
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x21c0 - 0x21dc
            0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, # 0x21e0 - 0x21fc
        ]

        code_path = 'src/tests/files/code.txt'
        data_path = 'src/tests/files/data.txt'
        mem = Memory()
        mem.load_mem(code_path, data_path)
        # Checando endereços de 0x00 a 0x54 de acordo com o montador RARS:
        for i in range(0, len(text_values)):
            # Checando byte a byte:
            for j in range(4):
                assert mem.MEM[i*4+j] == (text_values[i] >> (j * 8)) & 0xFF
        # Checando endereços de 0x2000 a 0x2ffc:
        for i in range(0, len(data_values)):
            # Chechando byte a byte:
            for j in range(4):
                assert mem.MEM[i*4+j+8192] == (data_values[i] >> (j * 8)) & 0xFF
