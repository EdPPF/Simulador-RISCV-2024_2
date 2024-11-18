from core.cpu import CPU, ProgramCounterOverflowError

def main():
    code_path = 'test/code.bin'
    data_path = 'test/data.bin'
    cpu = CPU(code_path, data_path)
    try:
        cpu.run()
    except ProgramCounterOverflowError as e:
        print(e)

if __name__ == "__main__":
    main()
