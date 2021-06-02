from jinja2 import Template
import shutil
import pdb

from .globals import *

# fmt: off
# template expects data dictionary with arguments of
#  data list[str]
#  terminal_size int
#  history_length int
DISPLAY_TEMPLATE = Template(
"""🐐🐐 Command History:
There are {{ history_length }} items(s) to observe. Rendering tWidth at {{ terminal_size }}. 

{{ top_line }}

{% for cmd in data -%}   -->  {{ cmd }}
{% endfor %}
{{ bottom_line }}
""")

DOWN_ARROW="\\/"
UP_ARROW="/\\"

EMPTY_DATA_TEMPLATE = Template(
"""
{{ ("-" * terminal_size ) }}
Well that's unfortunate.

I can't find your seach history. I looked here:

I'd `ctrl-c` to exit if I were you. 
{{ ("-" * terminal_size ) }}
""")
# fmt: on


class InvalidConfigurationException(BaseException):
    pass


class HistoryRenderer:
    def __init__(self, data, **kwargs):
        self.data = [cmd.strip() for cmd in data]

        self.frame_size = kwargs.get("frame_size", DEFAULT_FRAME_SIZE)
        self.template = kwargs.get("template", DISPLAY_TEMPLATE)
        self.current_frame = kwargs.get("start_frame", 0)
        self.previous_frame = None

        if not data:
            raise InvalidConfigurationException(
                "The data passed to the renderer needs to be populated. Renderer saw {} items in data array.".format(
                    len(self.data)
                )
            )

        if self.frame_size > len(data):
            raise InvalidConfigurationException(
                "Frame size of {} is bigger than the size of the data array {}!".format(
                    self.frame_size, len(self.data)
                )
            )

    def t_size(self):
        return shutil.get_terminal_size()

    def __rows_preceeding(self, index=None):
        return (index or self.current_frame) > 0

    def __rows_proceeding(self, index=None):
        begin_idx = index or self.current_frame
        end_idx = begin_idx + self.frame_size

        return any(self.data[end_idx:])

    def __calculate_line(self, direction):
        terminal_size = self.t_size().columns

        if direction == UP_ARROW:
            if not self.__rows_proceeding():
                direction = "=="

        if direction == DOWN_ARROW:
            if not self.__rows_preceeding():
                direction = "=="

        result = "--" + direction + ("-" * (terminal_size - 8)) + direction + "--"
        return result

    def __calculate_prefix(self, input):
        if input:
            return "\033[{}F".format(len(input.split("\n")) + 1) 
        else:
            return input

    def render_current_frame(self, enable_overwrite = True):
        return self.render_frame(reversed(self.get_frame()), enable_overwrite)

    def render_frame(self, frame, enable_overwrite = True):
        """
        Renders a frame to text. Leaves the value output set in class variable
        `previous_frame`. This will allow the next render to overwrite the previous output
        appropriately.

        """
        rendered_frame = self.template.render(
            data=frame,
            terminal_size=self.t_size().columns,
            bottom_line=self.__calculate_line(DOWN_ARROW),
            top_line=self.__calculate_line(UP_ARROW),
            history_length=len(self.data),
        )
        prefix = ""
        if enable_overwrite and self.previous_frame:
            prefix = self.__calculate_prefix(self.previous_frame)

        self.previous_frame = rendered_frame
        return prefix + rendered_frame

    # previously written reference for writing to the same "frame"
    # # https://stackoverflow.com/questions/24072790/detect-key-press-in-python
    # def render_frame(data, offset, window_size=5):
    #     frame_data = get_frame(data, offset, window_size)

    #     # suffix = "\033[F" * ((len(frame_data) - 1) or 1)

    #     rendering_string = "\r" + "\n".join(frame_data)  # + suffix

    #     

    def get_frame(self):
        """
        Gets a frame at current index.

        See get_frame_at_index for details.
        """
        return self.get_frame_at_index(self.current_frame)

    def get_frame_at_index(self, index):
        """
        Gets a frame at current index.

        Array Slice Access method:
            [<--->---------]
             i + f

            i: target index
            f: target index + frame_size

            [i:i+frame_size]
        """
        begin = index
        end = begin + self.frame_size

        return self.data[begin:end]

    def increment_frame(self):
        """
        Advances the frame in the positive direction. Moving first element of viewable frame towards the end.
        Never moves beyond safe bound.

        Given a basic array of data, it would looks like...

        < in frame >
        [<--->---------] --> [-<--->--------]
         0                    01
        """
        if not self.current_frame >= (len(self.data) - self.frame_size):
            self.current_frame += 1

    def decrement_frame(self):
        """
        Retreats the frame in the negaive direction, bringing the first element in frame closer to 0.
        Never moves beyond safe bound.

        Given a basic array of data, it would looks like...

        < in frame >
        [-<--->--------] --> [<--->---------]
         01                   0
        """
        if self.current_frame > 0:
            self.current_frame -= 1
