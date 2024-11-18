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

Execute o simulador:

```bash
python src/main.py
```

## Como Rodar Testes

Para rodar os testes escritos por meio da biblioteca `pytest`, rode o comando abaixo a partir da raiz do repositório:

```bash
pytest src/tests/test_<arquivo.py> -vv -W ignore
```

`<arquivo.py>` se refere ao módulo de teste que quer testar. A flag `-vv` do pytest serve para dar mais detalhes dos resultados dos testes, enquanto a flag `-W ignore` serve para ignorar avisos. Como exemplo de comando, este serve para testar a classe `InstructionSet`:

```bash
pytest src/tests/test_instructions.py -vv
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
│   ├── tests/                 # Utilitários e funções auxiliares
│   │   ├── __init__.py
│   │   ├── test_cpu.py
│   │   ├── test_decoder.py
│   │   ├── test_executor.py
│   │   ├── test_instructions.py
│   │   └── test_memory.py
│   └── main.py                # Ponto de entrada do simulador
├── .gitignore
├── requirements.txt
└── README.md
```
