from parser_logic import parser
from storage_logic import save_file


def main():
    save_file(parser())


if __name__ == "__main__":
    main()