import os
import sys

# Custom imports
from src.parser import Parser
from src import utils


if __name__ == "__main__":
    dim = os.get_terminal_size()
    utils.clear_screen()

    # Querying the input file in case it wasn't provided
    if len(sys.argv) < 2:
        print('\n\n', "Please input the (relative) path to the trace file".center(dim.columns), '\n')
        input_filename = input(' ' * (dim.columns // 2) + ">>> ")
    else:
        input_filename = sys.argv[1]

    # Cleaning data and parsing
    parser = Parser(input_filename)
    frames = parser.clean_data()
    result = parser.parse(frames)


    # Preparing interface
    utils.clear_screen()
    utils.print_logo(dim)


    # Filtering frames with the user's choice
    print(f"{len(result)} readable frames found.".center(dim.columns))
    result = utils.filter_frames(result, dim)

    print("\n")


    # Print something in case there is nothing to show
    if not result:
        print("No valid frame to print.".center(dim.columns), '\n')
        exit()

    abstract = utils.to_text(result)

    # If the abstract is too wide for the terminal
    while abstract == '':
        input("Terminal does not have enough rows, please decrease font size (press enter to retry)")
        abstract = utils.to_text(result)

    print("\n\n")


    print(abstract)

    # Getting output file name from the original
    filename = input_filename.replace("\\", "/").split("/")[-1].rsplit(".", 1)[0]

    # Writing output in a file
    with open(filename + "_wirewhale_output.txt", "wb") as output:
        output.write(abstract.encode("utf-8"))


    input("Press enter to exit...".center(dim.columns) + '\n')

    # Final screen clearing before exiting
    utils.clear_screen()
