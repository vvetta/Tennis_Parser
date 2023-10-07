from parser_logic import parser
from storage_logic import save_file


def main():
    try:
        save_file(parser())
    except Exception as ex:
        print(ex)
    finally:
        print("\nПрограмма отработала!\n")


if __name__ == "__main__":
    main()