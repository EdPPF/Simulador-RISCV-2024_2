"""
Módulo que implementa a memória do simulador.\n
Além de inicializar a memória, a classe Memory possui métodos para leitura e escrita de bytes e palavras e o método `load_mem` para carregar o conteúdo de um arquivo montado pelo RARS.
"""

import numpy as np

class Memory:
    '''
    Memória de 16KBytes com elementos de 8 bits sem sinal (uint8).\n
    Valores uint8 podem ser interpretados em complemento de dois:\n
    - Se o valor armazenado no byte estiver entre 0 e 127 (ou seja, se o bit mais significativo for 0), ele será considerado um número positivo.\n
    - Se o valor estiver entre 128 e 255 (ou seja, se o bit mais significativo for 1), ele será interpretado como um número negativo em complemento de dois.
    '''
    def __init__(self) -> None:
        self.MEM = np.zeros(16384, dtype=np.uint8)

    def lb(self, reg: int, kte: int):
        '''Lê um byte da memória e o converte para um inteiro de 32 bits estendendo o sinal do byte. Retorna o inteiro de 32 bits.'''
        address = reg + kte
        byte = int(self.MEM[address])
        # Verifica se o byte deve ser tratado como negativo
        if byte & 0x80:  # Se o bit de sinal (bit 7) estiver definido
            # Extensão de sinal: converte para negativo em complemento de dois
            byte -= 256
        return hex(byte & 0xffffffff)

    def lbu(self, reg: int, kte: int) -> str:
        '''Lê um byte da memória e o converte para um inteiro de 32 bits sem sinal (valor positivo). Retorna o inteiro de 32 bits.'''
        address = reg + kte
        return hex(np.uint32(self.MEM[address]))

    def lw(self, reg: int, kte: int):
        '''Lê uma palavra de 32 bits da memória e retorna o seu valor.'''
        address = reg + kte
        if address % 4 != 0:
            raise ValueError(f"{reg} + {kte} não retorna um múltiplo de 4.")

        byte0 = np.uint32(self.MEM[address+0])
        byte1 = np.uint32(self.MEM[address+1])
        byte2 = np.uint32(self.MEM[address+2])
        byte3 = np.uint32(self.MEM[address+3])
        word = (byte3 << 24) | (byte2 << 16) | (byte1 << 8) | byte0
        return hex(word)

    def sb(self, reg: int, kte: int, byte):
        '''Escreve o byte passado como parâmetro na memória.'''
        address = reg + kte
        np.put(self.MEM, address, byte)

    def sw(self, reg: int, kte: int, word):
        '''Escreve os 4 bytes de word na memória, colocando o menos significativo no endereço especificado e os outros nos endereços de byte seguintes.'''
        if (reg + kte) % 4 != 0:
            raise ValueError(f"{reg} + {kte} não retorna um múltiplo de 4.")

        byte0 = word         & 0xFF # Byte menos significativo (bits 0 a 7)
        byte1 = (word >> 8)  & 0xFF # Próximo byte (bits 8 a 15)
        byte2 = (word >> 16) & 0xFF # Próximo byte (bits 16 a 23)
        byte3 = (word >> 24) & 0xFF # Byte mais significativo (bits 24 a 31)
        self.sb(reg, kte, byte0)
        self.sb(reg, kte+1, byte1)
        self.sb(reg, kte+2, byte2)
        self.sb(reg, kte+3, byte3)


    def _store(self, address, value: int):
        """
        Armazena uma palavra de 32 bits (4 bytes) em um endereço específico.\n
        - address: Endereço da memória\n
        - value: Valor de 32 bits a ser armazenado
        """
        byte0 = value & 0xFF # Byte menos significativo (bits 0 a 7)
        byte1 = (value >>  8) & 0xFF
        byte2 = (value >> 16) & 0xFF
        byte3 = (value >> 24) & 0xFF
        self.MEM[address]     = byte0
        self.MEM[address + 1] = byte1
        self.MEM[address + 2] = byte2
        self.MEM[address + 3] = byte3

    def load_mem(self, code_path, data_path):
        """
        Carrega o conteúdo de um arquivo montado pelo RARS para a memória.\n
        Dos arquivos montados pelo RARS, o segmento .text está no intervalo [0x00000000; 0x00000054].\n
        O segmento .data está em [0x00002000; 0x00002ffc].\n
        Os arquivos lidos estão salvos em binário (strings) como `code.txt` e `data.txt`.
        """
        # Carregar o segmento de código:
        with open(code_path, 'r') as f:
            address = 0x0
            for line in f:
                if address > 0x54:
                    raise ValueError("Endereço de código excedeu o limite de 0x54.")
                instruction = int(line.strip(), 2)
                self._store(address, instruction)
                address += 4
        # Carregar o segmento de dados:
        with open(data_path, 'r') as f:
            address = 0x2000
            for line in f:
                if address > 0x2ffc:
                    raise ValueError("Endereço de dados excedeu o limite de 0x2ffc.")
                data = int(line.strip(), 2)
                self._store(address, data)
                address += 4
