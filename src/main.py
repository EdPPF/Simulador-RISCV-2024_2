from core.cpu import CPU, ProgramCounterOverflowError

def main():
    code_path = 'src/tests/files/test1_text.txt' # 'src/tests/files/code.txt'
    data_path = 'src/tests/files/test1_data.txt' # 'src/tests/files/data.txt'
    cpu = CPU(code_path, data_path)
    try:
        cpu.run()
    except ProgramCounterOverflowError as e:
        print(e)

if __name__ == "__main__":
    main()
