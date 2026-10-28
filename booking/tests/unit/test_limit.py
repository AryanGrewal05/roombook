from datetime import datetime as dt
from datetime import timedelta

from booking.rules import exceeds_limit


def T(h, m=0):
    return dt(2026, 10, 20, h, m)


def test_three_hours_is_refused():
    assert exceeds_limit(T(9), T(12))


def test_one_hour_is_fine():
    assert not exceeds_limit(T(9), T(10))


def test_exactly_two_hours_is_allowed():
    assert not exceeds_limit(T(9), T(11))


def test_two_hours_and_one_second_is_refused():
    assert exceeds_limit(T(9), T(11) + timedelta(seconds=1))
