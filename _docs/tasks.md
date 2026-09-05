# Shared Household Chores Tool — MVP Backlog

Stack: Django (Python 3.14), PostgreSQL 18, server-rendered Django templates + HTMX for interactivity. Weekly assignments are generated lazily (on the first dashboard load of a new week) rather than via a scheduler.

Each task below is scoped to be completable in one sitting and self-contained: it references the [MVP plan](plan.md) directly rather than other tasks, so it can be picked up without reading the rest of this backlog.

---

## 1. Empty project with a passing test
Goal: Prove the development environment works end-to-end before any app code exists.
Description: Initialize a Django project targeting Python 3.14, with a PostgreSQL 18 database connection configured (even if no models exist yet). Add a single trivial test — e.g. a sanity check or a test that a health-check/home route returns HTTP 200 — and confirm it passes via the standard test runner.

## 2. Local development setup & README
Goal: Let any developer get the project running locally without prior context.
Description: Add environment-based configuration for secrets and DB connection details (e.g. via a `.env` file pattern), and write a README documenting how to create the database, install dependencies, run migrations, and start the dev server. Someone with no other context should be able to follow it and reach a running app.

## 3. Household structure models: Roommate, Area, Task
Goal: Represent the fixed household structure in the database.
Description: Add Django models for `Roommate`, `Area`, and `Task`, where each `Area` has many `Task`s, matching the structure described in the "Household Structure" section of the [MVP plan](plan.md) (3 roommates, 3 areas, each area with several tasks). Include and apply migrations; no admin registration or views are needed yet.

## 4. Rotation order configuration
Goal: Represent the fixed weekly rotation order that determines which roommate gets which area.
Description: Add a model or fixed data structure capturing the rotation order shown in the plan's "Weekly Rotation" section (e.g. a `RotationSlot` model linking a position in the cycle to a roommate/area pairing, or an equivalent ordered structure). This task only needs to store the configuration — it does not need to generate any weekly assignments itself.

## 5. Weekly assignment & task completion models
Goal: Represent a specific week's assignments and the completion status of its tasks.
Description: Add a `WeekAssignment` model (linking a roommate to an area for a specific, identifiable week) and a `TaskCompletion` model (linking a task to a completed/incomplete boolean, scoped to a week assignment). Include and apply migrations. These are the models that make weekly history persistent, per the plan's "Data Storage" section.

## 6. Seed the predefined household
Goal: Populate the database with the exact fixed MVP household on setup.
Description: Write a data migration or a `manage.py` management command that creates the 3 roommates, 3 areas (Kitchen, Bathroom, Common Area), their example tasks, and the rotation order exactly as listed in the plan's "Household Structure" and "Weekly Rotation" sections. Running it more than once should not create duplicates.

## 7. Week-boundary calculation utility
Goal: Determine which calendar week (Monday–Sunday) any given date falls in.
Description: Write a small, pure utility function that takes a date and returns an identifier for its week (e.g. the date of that week's Monday). Cover it with unit tests for edge cases such as a Sunday input, a Monday input, and a date crossing a month/year boundary. This will later be used to detect whether a new week needs to be generated.

## 8. Rotation logic to compute a week's assignments
Goal: Given a week number, compute which area each roommate is assigned that week.
Description: Write a pure function that takes the rotation configuration and a week index, and returns the roommate-to-area mapping for that week, cycling through the fixed order shown in the plan's rotation example table. Add unit tests confirming the mapping is correct across at least 4 consecutive weeks (enough to see the cycle repeat).

## 9. Lazy "ensure current week exists" logic
Goal: Guarantee the current week's assignments exist in the database, creating them exactly once if missing.
Description: Write a service function that checks (using the week-boundary utility) whether a `WeekAssignment` already exists for the current week; if not, it creates the week's assignments and their `TaskCompletion` rows using the rotation logic. Add tests for both the "already exists" case and the "needs creation" case, confirming a second call never creates a duplicate week.

## 10. Dashboard view (read-only)
Goal: Show the current week's assignments and task checklists on the app's home page.
Description: Add a Django view and template that ensures the current week exists (per task 9's logic) and renders each roommate's assigned area along with its task checklist, matching the table layout in the plan's "Dashboard" section. Checkboxes should reflect current completion state but do not need to be clickable yet.

## 11. Overall progress summary on the dashboard
Goal: Show total completed vs. total tasks for the current week.
Description: Extend the dashboard view and template to compute and display a summary such as "7 / 12 tasks completed", based on the current week's `TaskCompletion` records, as described in the plan's "Dashboard" section.

## 12. Task check/uncheck interactivity
Goal: Let any roommate toggle a task's completed status without a full page reload.
Description: Add an HTMX-powered endpoint that flips a single `TaskCompletion`'s status when its checkbox is clicked, and returns the updated checkbox (and progress summary) as an HTML fragment. Wire the dashboard template's checkboxes to call this endpoint, satisfying the plan's rule that any roommate can check or uncheck any task during the current week.

## 13. History list page
Goal: Let users see a list of all past weeks.
Description: Add a view and template for a "History" page listing every past week (each with a date range or week label) with a link to that week's detail page, satisfying the plan's requirement for history to be reachable via a separate page from the dashboard.

## 14. History detail page
Goal: Show one past week's assignments and completion status, read-only.
Description: Add a view and template that, given a week identifier, displays that week's roommate-to-area assignments and each task's completed/incomplete status. Per the plan's "History" section, do not display completion timestamps, who completed each task, or any fairness score.

## 15. Shared styling and layout polish
Goal: Make the dashboard and history pages clear and presentable.
Description: Add minimal shared CSS covering layout, table/checklist readability, and checkbox styling across the dashboard and history templates. No JS framework or design system should be introduced — plain CSS is sufficient for the MVP.

## 16. End-to-end smoke test of the core flow
Goal: Verify the full MVP user flow works together, not just in isolated pieces.
Description: Write an integration test that loads the dashboard (triggering week creation), toggles a task via the HTMX endpoint, confirms the progress summary updates accordingly, and confirms that week's data now appears correctly on the History pages. This is the test that proves the "Definition of Done" in the plan is actually met end-to-end.
