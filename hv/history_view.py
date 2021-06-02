import argparse
import os
import sys
import atexit

from .renderer import HistoryRenderer
from .interactions import HistoryInteractor, InteractionResult

# abstraction layer where console detection needs to kick in and return a list of the console history
# prototype only supports powershell
#  - most recent first
#  - all of it
def get_console_history():
    with open(
        "{userhome}/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadline/ConsoleHost_history.txt".format(
            userhome=os.environ["USERPROFILE"]
        ),
        "r",
        encoding="utf-8",
    ) as history:
        data = history.readlines()
        data.reverse()

        return data

def console_loop(renderer):
    """
    This loop is the primary driver of the UI experience. Its primary purpose is to
    provide the input <-> renderer interaction loop.

    Currently hacked for initial ease of testing.
    """
    i_handler = HistoryInteractor()

    # while True:
    # output = renderer.render_current_frame()
    #     # result = i_handler.wait_for_input()
    # sys.stdout.write(output)
    # sys.stdout.flush()
    renderer.increment_frame()

    input("<- CURSOR_HERE")

    output = renderer.render_current_frame()
    sys.stdout.write(output)
    sys.stdout.flush()

    # switch on the different cases of interaction

        


def console_entry():
    data = get_console_history()
    renderer = HistoryRenderer(data)
    console_loop(renderer)
