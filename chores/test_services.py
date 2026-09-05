import datetime

from django.test import TestCase

from chores.models import Roommate, TaskCompletion, WeekAssignment
from chores.services import ensure_week


class EnsureWeekTests(TestCase):
    """Household data (roommates/areas/tasks/rotation) comes from the
    0004_seed_household data migration, which runs for the test DB too.
    """

    def setUp(self):
        self.week_start = datetime.date(2024, 1, 1)

    def test_creates_assignments_and_completions_when_missing(self):
        self.assertEqual(WeekAssignment.objects.count(), 0)

        created = ensure_week(self.week_start)

        self.assertEqual(len(created), Roommate.objects.count())
        assignments = WeekAssignment.objects.filter(week_start=self.week_start)
        self.assertEqual(assignments.count(), Roommate.objects.count())

        # Every task in each assigned area got a (not-yet-completed) TaskCompletion.
        for assignment in assignments:
            expected_task_count = assignment.area.tasks.count()
            completions = TaskCompletion.objects.filter(week_assignment=assignment)
            self.assertEqual(completions.count(), expected_task_count)
            self.assertTrue(all(not c.completed for c in completions))

    def test_does_nothing_when_week_already_exists(self):
        ensure_week(self.week_start)
        first_pass_ids = set(WeekAssignment.objects.values_list("id", flat=True))

        ensure_week(self.week_start)
        second_pass_ids = set(WeekAssignment.objects.values_list("id", flat=True))

        self.assertEqual(first_pass_ids, second_pass_ids)
        self.assertEqual(WeekAssignment.objects.filter(week_start=self.week_start).count(), Roommate.objects.count())

    def test_defaults_to_the_current_week(self):
        created = ensure_week()
        self.assertTrue(all(wa.week_start == created[0].week_start for wa in created))
