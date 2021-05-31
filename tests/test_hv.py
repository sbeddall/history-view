from hv import HistoryRenderer, InvalidConfigurationException
import pytest
import re
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


def test_rows_proceeding_true_case():
    pass


def test_rows_proceeding_false_case():
    pass


def test_rows_preceeding_true_case():
    pass


def test_rows_preceeding_false_case():
    pass


def test_rdr_bad_frame():
    t_data = get_test_data()
    with pytest.raises(InvalidConfigurationException) as exception:
        test_rdr = HistoryRenderer(t_data, frame_size=11)
    assert "is bigger than the size of the data array" in str(exception)


def test_rdr_no_data():
    with pytest.raises(InvalidConfigurationException) as exception:
        test_rdr = HistoryRenderer([], frame_size=5)
    assert "needs to be populated" in str(exception)


def test_rdr_output_short_frame():
    test_rdr = HistoryRenderer(get_test_data(), frame_size=5)

    input_frame = test_rdr.get_frame()
    output_text = test_rdr.render_frame(input_frame)
    lines_in_data = output_text.splitlines()

    assert len(lines_in_data) == 14

    for line in input_frame:
        assert line in output_text


def test_rdr_console_output():
    test_rdr = HistoryRenderer(get_test_data(), frame_size=5, terminal_size="")
    expected_output = """-->  sentence - 9  - index 1
-->  sentence - 8  - index 2
-->  sentence - 7  - index 3
-->  sentence - 6  - index 4
-->  sentence - 5  - index 5"""

    input_frame = test_rdr.get_frame_at_index(1)
    output_text = test_rdr.render_frame(input_frame)

    print(output_text)
    assert expected_output in output_text


def test_rdr_output_long_frame():
    pass
