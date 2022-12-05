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
        print('\n\n' + "Please input the (relative/absolute) path to the trace file".center(dim.columns) + '\n')
        input_filename = input(' ' * (dim.columns // 2) + ">>> ")
    else:
        input_filename = sys.argv[1]


    print('\n\n' + "What display mode do you want to run?".center(dim.columns))
    print("1: Fancy mode (recommended), 2: Safe mode (only if your terminal fails to display Specials)".center(dim.columns))
    safe_mode = input(' ' * (dim.columns // 2) + ">>> ")

    try:
        # Checking UNICODE compatibility
        char = '▔'
        arl, arr = '◀', '▶'
        char.encode(sys.stdout.encoding)
        arl.encode(sys.stdout.encoding)
        arr.encode(sys.stdout.encoding)

    except UnicodeEncodeError as err:
        # Verification failed, rolling back to ASCII characters
        char = "-"
        arl, arr = '<', '>'


    # Preparing interface
    utils.clear_screen()
    utils.print_logo(dim)


    # Cleaning data and parsing
    parser = Parser(input_filename)
    frames = parser.clean_data()
    result = parser.parse(frames)


    # Filtering frames with the user's choice
    print('\n' + f" => {len(result)} readable and compatible (Ethernet & IPv4) frames found.".center(dim.columns))
    result = utils.filter_frames(result, dim)

    print("\n")


    # Print something in case there is nothing to show
    if not result:
        print("No valid frame to print.".center(dim.columns), '\n')
        exit()

    abstract = utils.to_text(result, safe_mode=="2")

    # If the abstract is too wide for the terminal ask for resizing
    while abstract == '':
        input("Terminal does not have enough rows, please decrease font size or dezoom terminal (press enter to retry)")
        abstract = utils.to_text(result)
        dim = os.get_terminal_size()

    # Show abstract
    print("\n\n" + abstract)

    # Getting output file name from the original
    filename = input_filename.replace("\\", "/").split("/")[-1].rsplit(".", 1)[0]

    # Writing output in a file
    with open(filename + "_wirewhale_output.txt", "wb") as output:
        output.write(abstract.encode("utf-8"))


    input("Press enter to exit...".center(dim.columns) + '\n')

    # Final screen clearing before exit
    utils.clear_screen()
