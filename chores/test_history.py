from django.test import TestCase

from chores.models import TaskCompletion, WeekAssignment


class HistoryListViewTests(TestCase):
    def test_lists_the_current_week_once_it_exists(self):
        self.client.get("/")  # dashboard creates the current week

        response = self.client.get("/history/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "History")
        self.assertContains(response, "/history/")

    def test_shows_a_message_when_no_weeks_exist_yet(self):
        response = self.client.get("/history/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No weeks recorded yet")


class HistoryDetailViewTests(TestCase):
    def setUp(self):
        self.client.get("/")  # creates the current week
        week_start = WeekAssignment.objects.first().week_start
        self.week_start = week_start
        self.url = f"/history/{week_start.isoformat()}/"
        self.completion = TaskCompletion.objects.first()
        self.completion.completed = True
        self.completion.save()

    def test_shows_assignments_and_completion_status(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        for name in ("A", "B", "C"):
            self.assertContains(response, name)
        self.assertContains(response, self.completion.task.name)
        self.assertContains(response, "checked")

    def test_checkboxes_are_not_interactive(self):
        response = self.client.get(self.url)
        self.assertContains(response, "disabled")
        self.assertNotContains(response, "hx-post")

    def test_does_not_show_timestamps_who_completed_or_fairness_scores(self):
        response = self.client.get(self.url)
        content = response.content.decode().lower()
        for forbidden in ("completed at", "completed by", "fairness"):
            self.assertNotIn(forbidden, content)

    def test_404_for_a_week_with_no_data(self):
        response = self.client.get("/history/2000-01-03/")
        self.assertEqual(response.status_code, 404)

    def test_404_for_a_malformed_week(self):
        response = self.client.get("/history/not-a-date/")
        self.assertEqual(response.status_code, 404)
