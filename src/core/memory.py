# Implementação da memória (load/store)

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


    def store(self, address, value: int):
        """
        Armazena uma palavra de 32 bits (4 bytes) em um endereço específico.\n
        - address: Endereço da memória\n
        - value: Valor de 32 bits a ser armazenado
        """
        self.MEM[address:address+4] = value.to_bytes(4, byteorder='little')

    def load_mem(self, file_path):
        """
        Carrega o conteúdo de um arquivo montado pelo RARS para a memória.
        """
        with open(file_path, 'r') as f:
            address = 0x0  # Endereço inicial onde os dados serão carregados
            for line in f:
                # Supondo que o arquivo contenha linhas de instruções em hexadecimal
                instruction = int(line.strip(), 16)
                self.store(address, instruction)
                address += 4  # Cada instrução ocupa 4 bytes
