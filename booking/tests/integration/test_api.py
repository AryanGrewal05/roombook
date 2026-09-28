from django.test import TestCase


class BookingApiTests(TestCase):
    """Integration: HTTP -> DRF view -> Django ORM -> MongoDB."""

    def post(self, start, end):
        return self.client.post("/api/bookings/", {
            "room": "L-204", "start": f"2026-10-20T{start}Z",
            "end": f"2026-10-20T{end}Z"}, content_type="application/json")

    def test_second_overlapping_booking_is_refused(self):
        self.assertEqual(self.post("09:00", "10:30").status_code, 201)
        self.assertEqual(self.post("10:00", "11:00").status_code, 409)

    def test_back_to_back_bookings_both_succeed(self):
        self.assertEqual(self.post("09:00", "10:00").status_code, 201)
        self.assertEqual(self.post("10:00", "11:00").status_code, 201)
