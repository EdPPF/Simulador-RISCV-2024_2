from core.cpu import CPU, ProgramCounterOverflowError

def main():
    code_path1 = 'src/tests/files/test1_text.txt'
    data_path1 = 'src/tests/files/test1_data.txt'
    cpu1 = CPU(code_path1, data_path1)

    code_path2 = 'src/tests/files/test2_text.txt'
    data_path2 = 'src/tests/files/test2_data.txt'
    cpu2 = CPU(code_path2, data_path2)


    try:
        cpu1.run()
    except ProgramCounterOverflowError as e:
        print(e)

if __name__ == "__main__":
    main()
