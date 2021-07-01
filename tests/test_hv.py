from hv import HistoryRenderer, InvalidConfigurationException
import pytest
import re
import pdb

# TODO: Add additional tests for interaction. split into different test file. The bulk of this file
# actually tests rendering, so probably should be moved into a test_renderer file instead of leaving it
# here.


def test_hv_basic_import():
    from hv import console_entry


def test_rdr_good_increment_cases(test_data):
    very_edge = HistoryRenderer(test_data, frame_size=5, start_frame=4)
    very_edge.increment_frame()
    assert very_edge.current_frame == 4

    standard = HistoryRenderer(test_data, frame_size=5, start_frame=0)
    standard.increment_frame()
    assert standard.current_frame == 0


def test_rdr_bad_increment_cases(test_data):
    very_edge = HistoryRenderer(test_data, frame_size=5, start_frame=5)
    very_edge.increment_frame()
    assert very_edge.current_frame == 4

    outside_bounds = HistoryRenderer(test_data, frame_size=5, start_frame=10)
    outside_bounds.increment_frame()
    assert outside_bounds.current_frame == 9


def test_rdr_good_decrement_cases(test_data):
    standard = HistoryRenderer(test_data, frame_size=5, start_frame=9)
    standard.decrement_frame()
    assert standard.current_frame == 8

    outside_bounds = HistoryRenderer(test_data, frame_size=5, start_frame=10)
    outside_bounds.decrement_frame()
    assert outside_bounds.current_frame == 9

    very_edge = HistoryRenderer(test_data, frame_size=5, start_frame=1)
    very_edge.decrement_frame()
    assert very_edge.current_frame == 0


def test_rdr_bad_decrement_cases(test_data):
    over_edge = HistoryRenderer(test_data, frame_size=5, start_frame=0)
    over_edge.decrement_frame()
    assert over_edge.current_frame == 0


def test_rows_proceeding_true_cases(test_data):
    edge_of_acceptable = HistoryRenderer(test_data, frame_size=5, start_frame=4)
    standard_start = HistoryRenderer(test_data, frame_size=5)

    assert edge_of_acceptable._HistoryRenderer__rows_proceeding()
    assert standard_start._HistoryRenderer__rows_proceeding()


def test_rows_proceeding_false_cases(test_data):
    frame_bigger_than_content = HistoryRenderer(test_data, frame_size=10, start_frame=5)
    start_out_of_scope = HistoryRenderer(test_data, frame_size=5, start_frame=11)
    edge_of_bad = HistoryRenderer(test_data, frame_size=5, start_frame=6)

    assert not frame_bigger_than_content._HistoryRenderer__rows_proceeding()
    assert not start_out_of_scope._HistoryRenderer__rows_proceeding()
    assert not edge_of_bad._HistoryRenderer__rows_proceeding()


def test_rows_preceeding_true_case(test_data):
    easy_check = HistoryRenderer(test_data, frame_size=5, start_frame=2)
    edge_check = HistoryRenderer(test_data, frame_size=5, start_frame=1)

    assert easy_check._HistoryRenderer__rows_preceeding()
    assert edge_check._HistoryRenderer__rows_preceeding()


def test_rows_preceeding_false_case(test_data):
    easy_check = HistoryRenderer(test_data, frame_size=5)
    out_of_bounds_check = HistoryRenderer(test_data, frame_size=5, start_frame=11)

    assert not easy_check._HistoryRenderer__rows_preceeding()
    assert out_of_bounds_check._HistoryRenderer__rows_preceeding()

def test_rdr_no_data():
    with pytest.raises(InvalidConfigurationException) as exception:
        test_rdr = HistoryRenderer([], frame_size=5)
    assert "needs to be populated" in str(exception)


def test_rdr_output_short_frame(test_data):
    test_rdr = HistoryRenderer(test_data, frame_size=5)

    input_frame = test_rdr.get_frame()
    output_text = test_rdr.render_frame(input_frame, enable_overwrite=False)
    lines_in_data = output_text.splitlines()

    assert len(lines_in_data) == 16

    for line in input_frame:
        assert line[0:10] in output_text


def test_rdr_console_output(test_data):
    test_rdr = HistoryRenderer(test_data, frame_size=5)

    input_frame = test_rdr.get_frame_at_index(1)
    output_text = test_rdr.render_frame(input_frame)

    print(output_text)
    for line in input_frame:
        assert line[0:10] in output_text


def test_rdr_output_long_frame():
    pass
