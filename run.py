import sys
import threading

# Custom imports
from src.parser import Parser
from src import utils
from gui import app

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("No file provided.")

    parser = Parser(sys.argv[1])

    result = parser.parse()

    # Temp output (each frame is a dict & separated with 2 \n)
    # with open("wirewhale_output.txt", "w") as output:
    #     output.write(result)

    threading.Timer(1, utils.open_browser, ("http://0.0.0.0:5000")).run()
    app.run(host="0.0.0.0", port=5000)
