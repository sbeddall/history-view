import argparse
import os
import sys
import atexit

from .renderer import HistoryRenderer

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

# https://stackoverflow.com/questions/24072790/detect-key-press-in-python
def render_frame(data, offset, window_size=5):
    frame_data = get_frame(data, offset, window_size)

    # suffix = "\033[F" * ((len(frame_data) - 1) or 1)

    rendering_string = "\r" + "\n".join(frame_data)  # + suffix

    sys.stdout.write(rendering_string)
    sys.stdout.flush()


def console_loop(renderer):
    """
    This loop is the primary driver of the UI experience. Its primary purpose is to 
    provide the input <-> renderer interaction loop.
    """
    renderer.render_current_frame()


def console_entry():
    data = get_console_history()
    renderer = HistoryRenderer(data)
    console_loop(renderer)
