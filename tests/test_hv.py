from hv import HistoryRenderer
import pdb

TEST_DATA = [
    "sentence - 10 - index 0 - latest in history, aka the first result if you pressed up.",
    "sentence - 9  - index 1",
    "sentence - 8  - index 2",
    "sentence - 7  - index 3",
    "sentence - 6  - index 4",
    "sentence - 5  - index 5",
    "sentence - 4  - index 6",
    "sentence - 3  - index 7",
    "sentence - 2  - index 8",
    "sentence - 1  - index 9 - earliest in history",
]


def get_test_data():
    return TEST_DATA[:]


def test_hv_basic_import():
    from hv import console_entry


def test_rdr_no_bad_increment():
    pass


def test_rdr_good_increment():
    pass


def test_rdr_stuck_increment():
    pass


def test_rdr_stuck_decrement():
    pass


def test_rdr_good_decrement():
    pass


def test_rdr_no_bad_decrement():
    pass


def test_rdr_output_short_frame():
    test_rdr = HistoryRenderer(get_test_data(), frame_size=5)

    input_frame = test_rdr.get_frame()
    output_text = test_rdr.render_frame(input_frame)
    lines_in_data = output_text.splitlines()

    assert len(lines_in_data) == 13

    for line in input_frame:
        assert line in output_text


def test_rdr_output_long_frame():
    pass
