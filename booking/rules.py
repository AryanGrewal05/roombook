"""Booking rules for campus study rooms. Pure Python: no database."""


def duration(start, end):
    """Length of a booking, in whole minutes."""
    return int((end - start).total_seconds() // 60)


def overlaps(a_start, a_end, b_start, b_end):
    """True if two bookings of the same room collide.
    Back-to-back bookings (one ends at 10:00, next starts at 10:00) do not."""
    return a_start < b_end and b_start < a_end


MAX_MINUTES = 120


def exceeds_limit(start, end):
    """Bookings longer than MAX_MINUTES are refused."""
    return duration(start, end) > MAX_MINUTES
