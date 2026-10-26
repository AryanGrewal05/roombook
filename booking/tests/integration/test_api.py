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

    def test_zero_length_booking_is_refused(self):
        self.assertEqual(self.post("09:00", "09:00").status_code, 400)

    def test_reversed_booking_is_refused(self):
        self.assertEqual(self.post("10:00", "09:00").status_code, 400)

    def test_exactly_two_hours_is_allowed(self):
        self.assertEqual(self.post("09:00", "11:00").status_code, 201)

    def test_more_than_two_hours_is_refused(self):
        self.assertEqual(self.post("09:00", "11:00:01").status_code, 400)

    def test_invalid_datetime_is_refused(self):
        self.assertEqual(self.post("invalid", "10:00").status_code, 400)

    def test_missing_fields_are_refused(self):
        response = self.client.post(
            "/api/bookings/", {}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_different_rooms_can_overlap(self):
        self.assertEqual(self.post("09:00", "10:00").status_code, 201)
        response = self.client.post("/api/bookings/", {
            "room": "L-205", "start": "2026-10-20T09:00Z",
            "end": "2026-10-20T10:00Z"}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_home_reports_running(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "running")
