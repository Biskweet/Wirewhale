import os
import sys

# Custom imports
from src.parser import Parser
from src import utils


if __name__ == "__main__":
    dim = os.get_terminal_size()

    utils.clear_screen()

    if len(sys.argv) < 2:
        print('\n\n', "Please input the (relative) path to the trace file".center(dim.columns), '\n')
        input_filename = input(' ' * (dim.columns // 2) + ">>> ")
    else:
        input_filename = sys.argv[1]


    parser = Parser(input_filename)

    frames = parser.clean_data()


    # Preparing interface
    utils.clear_screen()
    utils.print_logo(dim)


    # Filtering frames by the user's choice
    print(f"{len(frames)} readable frames found.".center(dim.columns))
    print(f"Please input the index of the frame to analyze (0 < i <= {len(frames)}, anything else = all frames).".center(dim.columns), '\n')
    user_input = input(' ' * (dim.columns // 2 - 5) + ">>> ")


    print("\n")


    if user_input.isdigit() and 0 < int(user_input) <= len(frames):
        result = parser.parse([frames[int(user_input) - 1]])

    else:
        result = parser.parse(frames)

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
