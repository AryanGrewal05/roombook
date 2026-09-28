"""Booking rules for campus study rooms. Pure Python: no database."""


def duration(start, end):
    """Length of a booking, in hours."""
    return (end - start).total_seconds() / 3600


def overlaps(a_start, a_end, b_start, b_end):
    """True if two bookings of the same room collide.
    Back-to-back bookings (one ends at 10:00, next starts at 10:00) do not."""
    return a_start < b_end and b_start < a_end


MAX_HOURS = 2


def exceeds_limit(start, end):
    """Bookings longer than MAX_HOURS are refused."""
    return duration(start, end) > MAX_HOURS
