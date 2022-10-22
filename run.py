import sys

from src.parser import Parser

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("No file provided.")

    parser = Parser(sys.argv[1])

    result = parser.parse()

    # Temp output (each frame as a dict interpolated with 2 line returns)
    with open("wirewhale_output.txt", "w") as output:
        output.write(result)
