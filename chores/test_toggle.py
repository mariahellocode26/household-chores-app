from django.test import TestCase

from chores.models import TaskCompletion


class ToggleTaskTests(TestCase):
    def setUp(self):
        self.client.get("/")  # ensures the current week (and its completions) exist
        self.completion = TaskCompletion.objects.first()

    def test_toggle_marks_incomplete_task_as_completed(self):
        self.assertFalse(self.completion.completed)

        response = self.client.post(f"/tasks/{self.completion.id}/toggle/")

        self.assertEqual(response.status_code, 200)
        self.completion.refresh_from_db()
        self.assertTrue(self.completion.completed)
        self.assertContains(response, "checked")
        self.assertContains(response, "1 / 9 tasks completed")

    def test_toggle_again_marks_it_incomplete(self):
        self.client.post(f"/tasks/{self.completion.id}/toggle/")
        response = self.client.post(f"/tasks/{self.completion.id}/toggle/")

        self.completion.refresh_from_db()
        self.assertFalse(self.completion.completed)
        self.assertContains(response, "0 / 9 tasks completed")

    def test_toggle_requires_post(self):
        response = self.client.get(f"/tasks/{self.completion.id}/toggle/")
        self.assertEqual(response.status_code, 405)
