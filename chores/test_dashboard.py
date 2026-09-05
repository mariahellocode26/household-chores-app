from django.test import TestCase

from chores.models import TaskCompletion


class DashboardViewTests(TestCase):
    def test_shows_current_week_assignments_and_zero_progress(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "0 / 9 tasks completed")
        # Every roommate and area from the seeded household should appear.
        for name in ("A", "B", "C"):
            self.assertContains(response, name)
        for area in ("Kitchen", "Bathroom", "Common Area"):
            self.assertContains(response, area)

    def test_progress_reflects_completed_tasks(self):
        self.client.get("/")  # ensures the current week exists
        completion = TaskCompletion.objects.first()
        completion.completed = True
        completion.save()

        response = self.client.get("/")

        self.assertContains(response, "1 / 9 tasks completed")
