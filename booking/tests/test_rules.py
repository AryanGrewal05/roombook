from datetime import datetime as dt
from booking.rules import duration, overlaps

T = lambda h, m=0: dt(2026, 10, 20, h, m)


def test_duration_of_ninety_minutes():
    assert duration(T(9), T(10, 30)) == 1.5


def test_back_to_back_is_allowed():
    assert not overlaps(T(9), T(10), T(10), T(11))


def test_partial_overlap_is_rejected():
    assert overlaps(T(9), T(10, 30), T(10), T(11))
