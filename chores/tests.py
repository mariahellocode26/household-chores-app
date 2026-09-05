from django.test import TestCase


class HomeViewTests(TestCase):
    """Sanity check that the project is wired up end-to-end (task 1)."""

    def test_home_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
