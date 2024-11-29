*Universidade de Brasília*

Instituto de Ciências Exatas - Departamento de Ciência da Computação

**CIC099 - Organização e Arquitetura de Computadores**

# Simulador RISC-V

Este trabalho consiste na implementação de um simulador da arquitetura RV32I.

Nem todas as instruções serão implementadas!

## Instruções Implementadas

```bash
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

## Bibliotecas Externas Utilizadas

- `Numpy`;
- `pytest` - verifique requirements.txt para a lista completa de dependências dessa biblioteca.

# Como Rodar o Programa

Clone o repositório e navegue até ele:

```bash
git clone https://github.com/EdPPF/Simulador-RISCV-2024_2.git
cd Simulador-RISCV-2024_2
```

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

Coloque arquivos de texto com as instruções (podem estar em binário, como nos arquivos de teste deste repositório) em algum lugar do repositório - um para a área de código (`.text` do RISCV) e outra para dados (`.data`).

Em `main.py`, carrege os arquivos na instância de CPU:

```python
# src/main.py
def main():
    code_path = 'caminho/para/seu/arquivo/text.txt'
    data_path = 'caminho/para/seu/arquivo/data.txt'
    cpu = CPU(code_path, data_path)
```

Execute o simulador:

```bash
python src/main.py
```

## Como Rodar Testes

Para rodar todos os testes escritos com a biblioteca `pytest`, rode o comando abaixo a partir da raiz do repositório:

```bash
pytest src/tests -vv -W ignore
```

A flag `-vv` do pytest serve para dar mais detalhes dos resultados dos testes, enquanto a flag `-W ignore` serve para ignorar avisos.

Para rodar algum arquivo de teste específico, basta adicionar o caminho até ele no comando acima:

```bash
pytest src/tests/test_<arquivo.py> -vv -W ignore
```

`<arquivo.py>` se refere ao módulo de teste que quer testar. Como exemplo de comando, este serve para testar a classe `InstructionSet`:

```bash
pytest src/tests/test_instructions.py -vv
```

Além dos testes de `pytest`, ou seja, todos os arquivos do tipo `test_*.py`, o arquivo `tests/test_completo.py` pode ser executado para verificar testes diversos das instruções sem utilizar alguma biblioteca específica para isso. Ele possui várias instâncias de `CPU` e as executa em diferentes threads por meio da bilbioteca padrão `multiprocessing`. Os resultados são impressos no terminal.

Esse arquivo pode ser executado de duas formas: Utilizando a instância `cpui` ou utilizando a `cpu`. Seja lá qual for escolhida, basta comentar e descomentar o código como abaixo:

- `cpui` - Roda e paralelo todas as 22 instâncias de `CPU` no arquivo, cada uma contendo um teste isolado.

    ```python
    ...
    def main(cpui=None):
        try:
            cpui.run()
        except ProgramCounterOverflowError as e:
            print(f"Pirijonga -> {e}")
        except SystemExit as e:
            print(f"Jiriponga -> {e}")

    if __name__ == "__main__":
        cpu_instances = [
            cpu41, cpu42, cpu43, cpu44, cpu45, cpu46, cpu47, cpu48, cpu49,
            cpu51, cpu52, cpu53, cpu54, cpu55, cpu56, cpu57, cpu58, cpu59,
            cpu61, cpu62, cpu63, cpu64
        ]
    ...
    ```

- `cpu` - Executa o arquivo com todos os 22 testes de um única vez, num teste maior.

    ```python
    ...
    def main(cpui=None):
        try:
            cpu.run() # ultraT
        except ProgramCounterOverflowError as e:
            print(f"Pirijonga -> {e}")
        except SystemExit as e:
            print(f"Jiriponga -> {e}")

    if __name__ == "__main__":
        cpu_instances = [
            cpu
        ]
    ...
    ```

# Estrutura do Repositório

```bash
rv32i-simulator/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── cpu.py             # Implementação da CPU (registradores, ciclo de execução)
│   │   ├── decoder.py         # Função decode() para extrair os campos da instrução
│   │   ├── executor.py        # Função execute() para executar instruções
│   │   ├── instruction_set.py # Conjunto de instruções RV32I
│   │   └── memory.py          # Implementação da memória (load/store)
│   ├── tests/                 # Testes
│   │   ├── files/
│   │   ├── __init__.py
│   │   ├── test_cpu.py
│   │   ├── test_decoder.py
│   │   ├── test_executor.py
│   │   ├── test_instructions.py
│   │   └── test_memory.py
│   ├── main.py                # Ponto de entrada do simulador
│   └── teste_completo.py      # Arquivo de teste que não utiliza `pytest`
├── .gitignore
├── requirements.txt
└── README.md
```
