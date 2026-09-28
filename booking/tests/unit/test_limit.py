from datetime import datetime as dt

from booking.rules import exceeds_limit


def T(h, m=0):
    return dt(2026, 10, 20, h, m)


def test_three_hours_is_refused():
    assert exceeds_limit(T(9), T(12))


def test_one_hour_is_fine():
    assert not exceeds_limit(T(9), T(10))
