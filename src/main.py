from core.cpu import CPU, ProgramCounterOverflowError

def main():
    program_path = 'test/test.txt'
    cpu = CPU(program_path)
    try:
        cpu.run()
    except ProgramCounterOverflowError as e:
        print(e)

if __name__ == "__main__":
    main()
