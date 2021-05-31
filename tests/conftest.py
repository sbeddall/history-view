import pytest

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


@pytest.fixture
def test_data():
    return TEST_DATA[:]
