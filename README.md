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

## Estrutura do Repositório:

```bash
rv32i-simulator/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── cpu.py             # Implementação da CPU (registradores, ciclo de execução)
│   │   ├── memory.py          # Implementação da memória (load/store)
│   │   ├── instruction_set.py # Conjunto de instruções RV32I
│   │   └── executor.py        # Função execute() para executar instruções
│   ├── utils/                 # Utilitários e funções auxiliares
│   │   ├── __init__.py
│   │   └── binary_utils.py    # Funções para conversão e manipulação de binários
│   └── main.py                # Ponto de entrada do simulador
├── tests/
│   └── TODO
├── .gitignore
├── requirements.txt
└── README.md
```
