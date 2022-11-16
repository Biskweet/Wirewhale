import os
import sys

import colorama

# Custom imports
from src.parser import Parser
from src import utils
from gui import app


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("No file provided.")

    parser = Parser(sys.argv[1])

    result = parser.parse()

    abstract = utils.to_text(result)

    while abstract == '':
        print("===================")
        input("TERMINAL DOES NOT HAVE ENOUGH ROWS, PLEASE DECREASE FONT SIZE (press enter to retry)")
        abstract = utils.to_text(result)

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    utils.print_logo()
    print(abstract)

    # Temp output (each frame is a dict & separated with 2 \n)
    with open(sys.argv[1].rsplit(".", 1)[0] + "_output.txt", "wb") as output:
        output.write(abstract.encode("utf-8"))

