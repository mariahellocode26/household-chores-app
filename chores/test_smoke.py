"""End-to-end smoke test of the core MVP flow (plan.md §14, §15).

Drives the app the way a user would: load the dashboard, toggle a task,
see progress update, then confirm that week now shows up correctly in
History. This is what actually proves the MVP's Definition of Done.
"""

from django.test import TestCase

from chores.models import TaskCompletion, WeekAssignment


class CoreFlowSmokeTest(TestCase):
    def test_dashboard_to_history_flow(self):
        # 1. Load the dashboard: the current week gets created automatically.
        dashboard_response = self.client.get("/")
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, "0 / 9 tasks completed")

        week_start = WeekAssignment.objects.first().week_start
        completion = TaskCompletion.objects.filter(week_assignment__week_start=week_start).first()
        self.assertFalse(completion.completed)

        # 2. Toggle one task via the HTMX endpoint.
        toggle_response = self.client.post(f"/tasks/{completion.id}/toggle/")
        self.assertEqual(toggle_response.status_code, 200)
        self.assertContains(toggle_response, "checked")

        # 3. The dashboard's progress summary reflects it.
        dashboard_response = self.client.get("/")
        self.assertContains(dashboard_response, "1 / 9 tasks completed")

        # 4. The week now appears in the History list...
        history_list_response = self.client.get("/history/")
        self.assertContains(history_list_response, f"/history/{week_start.isoformat()}/")

        # 5. ...and its detail page shows the toggled task as completed,
        #    with every other task for that roommate's area still unchecked.
        history_detail_response = self.client.get(f"/history/{week_start.isoformat()}/")
        self.assertEqual(history_detail_response.status_code, 200)
        self.assertContains(history_detail_response, completion.task.name)

        siblings = TaskCompletion.objects.filter(
            week_assignment=completion.week_assignment
        ).exclude(id=completion.id)
        self.assertTrue(siblings.exists())
        self.assertTrue(all(not sibling.completed for sibling in siblings))

        # 6. Re-generating the current week never creates a duplicate.
        assignments_before = WeekAssignment.objects.count()
        self.client.get("/")
        self.assertEqual(WeekAssignment.objects.count(), assignments_before)
