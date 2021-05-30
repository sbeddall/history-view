from jinja2 import Template
import shutil
import pdb

from .globals import *

# fmt: off
# template expects data dictionary with arguments of
#  data list[str]
#  terminal_size int 
DISPLAY_TEMPLATE = Template(
"""
{{ ("-" * terminal_size ) }}
Command History:
Width is {{ terminal_size }}

{% for cmd in data -%}
    {{ cmd }}
{% endfor %}

{{ ("-" * terminal_size ) }}
""")

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
        self.data = data
        self.current_frame = 0

        self.frame_size = kwargs.get("frame_size", DEFAULT_FRAME_SIZE)
        self.template = kwargs.get("template", DISPLAY_TEMPLATE)

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

    def render_current_frame(self):
        return self.render_frame(frame=self.get_frame())

    def render_frame(self, frame):
        return self.template.render(data=frame, terminal_size=self.t_size().columns)

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

        Given a basic array of data, it would looks like...

        < in frame >
        [<--->---------] --> [-<--->--------]
         0                    01
        """
        if not current_frame > (len(self.data) - self.frame_size):
            self.current_frame += 1

    def decrement_frame(self):
        """
        Retreats the frame in the negaive direction, bringing the first element in frame closer to 0.

        Given a basic array of data, it would looks like...

        < in frame >
        [-<--->--------] --> [<--->---------]
         01                   0
        """
        if self.current_frame > 0:
            self.current_frame -= 1
