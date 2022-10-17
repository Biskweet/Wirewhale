import sys

from src.parser import Parser

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("No file provided.")

    parser = Parser(sys.argv[1])
    result = parser.parse()

    print(result)
