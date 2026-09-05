import datetime
from types import SimpleNamespace

from django.test import SimpleTestCase

from chores.rotation import compute_assignments, week_start_for


class WeekStartForTests(SimpleTestCase):
    def test_monday_returns_itself(self):
        monday = datetime.date(2024, 1, 1)
        self.assertEqual(week_start_for(monday), monday)

    def test_midweek_returns_that_weeks_monday(self):
        wednesday = datetime.date(2024, 1, 3)
        self.assertEqual(week_start_for(wednesday), datetime.date(2024, 1, 1))

    def test_sunday_returns_that_weeks_monday(self):
        sunday = datetime.date(2024, 1, 7)
        self.assertEqual(week_start_for(sunday), datetime.date(2024, 1, 1))

    def test_date_crossing_year_boundary(self):
        # Jan 1, 2023 was a Sunday; its week started the previous December.
        sunday = datetime.date(2023, 1, 1)
        self.assertEqual(week_start_for(sunday), datetime.date(2022, 12, 26))


def _roommates():
    return [SimpleNamespace(name=name, order=order) for order, name in enumerate(["A", "B", "C"])]


def _rotation_slots():
    # Order matters (it's what compute_assignments indexes into); the
    # specific area labels are arbitrary for this test.
    return [SimpleNamespace(area=area) for area in ["Kitchen", "Bathroom", "Common Area"]]


class ComputeAssignmentsTests(SimpleTestCase):
    def setUp(self):
        self.roommates = _roommates()
        self.slots = _rotation_slots()
        self.week0 = datetime.date(2024, 1, 1)  # any Monday works as a starting point

    def _assignments_by_name(self, week_start):
        pairs = compute_assignments(week_start, self.roommates, self.slots)
        return {roommate.name: area for roommate, area in pairs}

    def test_each_week_assigns_every_area_exactly_once(self):
        for offset in (0, 7, 14, 21):
            week_start = self.week0 + datetime.timedelta(days=offset)
            areas = sorted(self._assignments_by_name(week_start).values())
            self.assertEqual(areas, ["Bathroom", "Common Area", "Kitchen"])

    def test_rotates_every_week_for_a_full_three_week_cycle(self):
        week1 = self._assignments_by_name(self.week0)
        week2 = self._assignments_by_name(self.week0 + datetime.timedelta(days=7))
        week3 = self._assignments_by_name(self.week0 + datetime.timedelta(days=14))

        # No roommate keeps the same area two weeks running.
        for name in ("A", "B", "C"):
            self.assertNotEqual(week1[name], week2[name])
            self.assertNotEqual(week2[name], week3[name])

        # All three weeks in the cycle are distinct from each other.
        self.assertNotEqual(week1, week2)
        self.assertNotEqual(week2, week3)
        self.assertNotEqual(week1, week3)

    def test_cycle_repeats_after_three_weeks(self):
        week1 = self._assignments_by_name(self.week0)
        week4 = self._assignments_by_name(self.week0 + datetime.timedelta(days=21))
        self.assertEqual(week1, week4)
