from core.cpu import CPU, ProgramCounterOverflowError
import multiprocessing

code_path = 'src/tests/files/ultraT_text.txt'
data_path = 'src/tests/files/ultraT_data.txt'
cpu = CPU(code_path, data_path)

# ADD
code_path41 = 'src/tests/files/test4-1_text.txt'
data_path41 = 'src/tests/files/test4-1_data.txt'
cpu41 = CPU(code_path41, data_path41)

# ADDi
code_path42 = 'src/tests/files/test4-2_text.txt'
data_path42 = 'src/tests/files/test4-2_data.txt'
cpu42 = CPU(code_path42, data_path42)

# AND
code_path43 = 'src/tests/files/test4-3_text.txt'
data_path43 = 'src/tests/files/test4-3_data.txt'
cpu43 = CPU(code_path43, data_path43)

# ANDi
code_path44 = 'src/tests/files/test4-4_text.txt'
data_path44 = 'src/tests/files/test4-4_data.txt'
cpu44 = CPU(code_path44, data_path44)

# AUIPC
code_path45 = 'src/tests/files/test4-5_text.txt'
data_path45 = 'src/tests/files/test4-5_data.txt'
cpu45 = CPU(code_path45, data_path45)

# BEQ e BNE
code_path46 = 'src/tests/files/test4-6_text.txt'
data_path46 = 'src/tests/files/test4-6_data.txt'
cpu46 = CPU(code_path46, data_path46)

# BGE e BGEU
code_path47 = 'src/tests/files/test4-7_text.txt'
data_path47 = 'src/tests/files/test4-7_data.txt'
cpu47 = CPU(code_path47, data_path47)

# Lê paavra da memória com LW e compara com constante
code_path48 = 'src/tests/files/test4-8_text.txt'
data_path48 = 'src/tests/files/test4-8_data.txt'
cpu48 = CPU(code_path48, data_path48)

# Le byte da memoria com LB e compara com constante
code_path49 = 'src/tests/files/test4-9_text.txt'
data_path49 = 'src/tests/files/test4-9_data.txt'
cpu49 = CPU(code_path49, data_path49)

# Le byte da memoria com LBU e compara com constante
code_path51 = 'src/tests/files/test5-1_text.txt'
data_path51 = 'src/tests/files/test5-1_data.txt'
cpu51 = CPU(code_path51, data_path51)

# Testando LUI e SLLi
code_path52 = 'src/tests/files/test5-2_text.txt'
data_path52 = 'src/tests/files/test5-2_data.txt'
cpu52 = CPU(code_path52, data_path52)

# Altera valor na memoria, testa SW
code_path53 = 'src/tests/files/test5-3_text.txt'
data_path53 = 'src/tests/files/test5-3_data.txt'
cpu53 = CPU(code_path53, data_path53)

# Altera o primeiro byte na palavra, testa SB
code_path54 = 'src/tests/files/test5-4_text.txt'
data_path54 = 'src/tests/files/test5-4_data.txt'
cpu54 = CPU(code_path54, data_path54)

# Testa OR
code_path55 = 'src/tests/files/test5-5_text.txt'
data_path55 = 'src/tests/files/test5-5_data.txt'
cpu55 = CPU(code_path55, data_path55)

# Testa ORi
code_path56 = 'src/tests/files/test5-6_text.txt'
data_path56 = 'src/tests/files/test5-6_data.txt'
cpu56 = CPU(code_path56, data_path56)

# Testa XOR
code_path57 = 'src/tests/files/test5-7_text.txt'
data_path57 = 'src/tests/files/test5-7_data.txt'
cpu57 = CPU(code_path57, data_path57)

# Testa SUB
code_path58 = 'src/tests/files/test5-8_text.txt'
data_path58 = 'src/tests/files/test5-8_data.txt'
cpu58 = CPU(code_path58, data_path58)

# Testa JAL e JALR
code_path59 = 'src/tests/files/test5-9_text.txt'
data_path59 = 'src/tests/files/test5-9_data.txt'
cpu59 = CPU(code_path59, data_path59)

# Testa SLT
code_path61 = 'src/tests/files/test6-1_text.txt'
data_path61 = 'src/tests/files/test6-1_data.txt'
cpu61 = CPU(code_path61, data_path61)

# Testa SRA
code_path62 = 'src/tests/files/test6-2_text.txt'
data_path62 = 'src/tests/files/test6-2_data.txt'
cpu62 = CPU(code_path62, data_path62)

# Testa SRL
code_path63 = 'src/tests/files/test6-3_text.txt'
data_path63 = 'src/tests/files/test6-3_data.txt'
cpu63 = CPU(code_path63, data_path63)

# Testa BLT e BLTU
code_path64 = 'src/tests/files/test6-4_text.txt'
data_path64 = 'src/tests/files/test6-4_data.txt'
cpu64 = CPU(code_path64, data_path64)

def main(cpui=None):
    try:
        # cpui.run()
        cpu.run()     # UltraT
    except ProgramCounterOverflowError as e:
        print(f"Pirijonga -> {e}")
    except SystemExit as e:
        print(f"Jiriponga -> {e}")

if __name__ == "__main__":
    cpu_instances = [
        cpu
        # cpu41, cpu42, cpu43, cpu44, cpu45, cpu46, cpu47, cpu48, cpu49,
        # cpu51, cpu52, cpu53, cpu54, cpu55, cpu56, cpu57, cpu58, cpu59,
        # cpu61, cpu62, cpu63, cpu64
    ]
    processes = []

    for cpu in cpu_instances:
        process = multiprocessing.Process(target=main, args=(cpu,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    print("\nFim das execuções!")
